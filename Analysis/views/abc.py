import re
from collections import Counter
from io import BytesIO
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from Analysis.models import Candidate
from utils import industry_keywords

import nltk
import string
import pandas as pd

nltk.download('averaged_perceptron_tagger')


def count_action_verbs(text):
    tags = nltk.pos_tag(text.split())
    action_verb_count = sum(1 for word, tag in tags if tag.startswith('VB'))
    return action_verb_count


def has_pronouns(text):
    tags = nltk.pos_tag(text.split())
    pronouns = [word for word, tag in tags if tag == 'PRP']
    return len(pronouns) > 0


def get_resume_status(score):
    if score >= 8:
        return 'Excellent'
    elif 5 <= score <= 7:
        return 'Average'
    else:
        return 'Bad'


def generate_graph_data(industry_names, industry_scores):
    graph_data = []
    for industry in industry_names:
        scores = industry_scores[industry]
        excellent_count = sum(1 for score in scores if score >= 8)
        average_count = sum(1 for score in scores if 5 <= score <= 7)
        bad_count = sum(1 for score in scores if score <= 4)
        graph_data.append({
            'industry': industry,
            'excellent_count': excellent_count,
            'average_count': average_count,
            'bad_count': bad_count
        })
    return graph_data


def abc(request):
    # Retrieve all job titles
    job_titles = Candidate.objects.values_list('job_title', flat=True)

    # Extract keywords from job titles
    keywords = []
    for title in job_titles:
        if title:
            words = re.findall(r'\w+', title.lower())
            keywords.extend(words)

    # Calculate keyword counts
    keyword_counts = dict(Counter(keywords))

    # Calculate industry keyword counts
    industry_keyword_counts = {
        industry: sum(keyword_counts.get(keyword, 0) for keyword in keywords)
        for industry, keywords in industry_keywords.items()
    }

    # Sort the industries based on their keyword counts in descending order
    sorted_industries = sorted(industry_keyword_counts.items(), key=lambda x: x[1], reverse=True)

    # Take the top ten industries
    top_industries = sorted_industries[:10]

    industry_names = [industry for industry, count in top_industries]
    industry_counts = [count for industry, count in top_industries]

    # Set the figure size and margins
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(left=0.2, bottom=0.3)  # Adjust the left and bottom margins

    # Generate the graph
    ax.bar(industry_names, industry_counts)
    ax.set_xlabel('Industry')
    ax.set_ylabel('Keyword Count')
    ax.set_title('Top Ten Industries based on Resume Score')
    plt.xticks(rotation=30, fontsize=8, ha='right')

    # Save the graph to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Calculate the score-based category in each top 10 industry
    industry_scores = {}
    for industry in industry_names:
        candidates = Candidate.objects.filter(job_title__icontains=industry_keywords[industry][0])

        scores = []
        for candidate in candidates:
            resume_fields = [
                'city',
                'state',
                'country',
                'awards',
                'education',
                'graduation_date',
                'job_title',
                'previous_organization',
                'certifications',
            ]

            # Calculate the score for the candidate
            score = 0
            for field in resume_fields:
                field_value = getattr(candidate, field) or ""
                if field_value:
                    score += 1

            # Check word length criterion
            word_length = sum(len(getattr(candidate, field) or "") for field in resume_fields)
            if word_length > 800:
                score -= 1

            # Check spelling errors criterion
            spelling_errors = sum(
                sum(not word.isnumeric() and not word.isalpha() for word in
                    (getattr(candidate, field) or "").translate(str.maketrans('', '', string.punctuation)).split())
                for field in resume_fields)
            if spelling_errors > 15:
                score -= 0.5

            # Check missing fields criterion
            missing_fields = [field for field in resume_fields if not getattr(candidate, field)]
            if missing_fields:
                score -= 1

            # Check action verbs criterion
            action_verbs_count = count_action_verbs(
                ' '.join(getattr(candidate, field) or "" for field in resume_fields))
            if action_verbs_count > 20:
                score += 1
            else:
                score -= 0.5

            # Adjust score based on pronouns
            has_pronoun = has_pronouns(' '.join(getattr(candidate, field) or "" for field in resume_fields))
            if has_pronoun:
                score -= 0.5

            scores.append(score)

        industry_scores[industry] = scores

    # Calculate the graph data for score-based categories
    graph_data = generate_graph_data(industry_names, industry_scores)

    # Render the template with the graph and table data
    return render(request, 'admin/chart1.html', {'graph': buffer.getvalue(), 'graph_data': graph_data})
