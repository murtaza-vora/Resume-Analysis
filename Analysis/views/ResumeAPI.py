import json
import string
import nltk
from django.shortcuts import render
from .forms import CandidateForm
from ..models import Candidate
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

def score_candidate(request):
    candidates = Candidate.objects.values(
        'user_id',
        'city',
        'state',
        'country',
        'awards',
        'education',
        'graduation_date',
        'job_title',
        'previous_organization',
        'certifications',
    )

    # Convert queryset to a Pandas DataFrame
    df = pd.DataFrame.from_records(candidates)

    # Define the resume fields
    resume_fields = ['city', 'state', 'country', 'awards', 'education', 'graduation_date', 'job_title',
                     'previous_organization', 'certifications']

    # Calculate score, resume status, and areas of improvement for each candidate
    candidates_data = []
    for _, candidate in df.iterrows():
        score = 0
        resume_status = ""
        area_of_improvement = []

        for field in resume_fields:
            field_value = candidate[field] or ""
            if field_value:
                score += 1

        # Check word length criterion
        word_length = sum(len(candidate[field] or "") for field in resume_fields)
        if word_length > 800:
            score -= 1
            area_of_improvement.append('Word length is more than 800')

        # Check spelling errors criterion
        spelling_errors = sum(
            sum(not word.isnumeric() and not word.isalpha() for word in
                (candidate[field] or "").translate(str.maketrans('', '', string.punctuation)).split())
            for field in resume_fields)
        if spelling_errors > 15:
            score -= 0.5
            area_of_improvement.append('Spelling errors')

        # Check missing fields criterion
        missing_fields = [field for field in resume_fields if not candidate[field]]
        if missing_fields:
            score -= 1
            area_of_improvement.extend(f"{field} missing" for field in missing_fields)

        # Check action verbs criterion
        action_verbs_count = count_action_verbs(' '.join(candidate[field] or "" for field in resume_fields))
        if action_verbs_count>20:

            area_of_improvement.append(f"Action verbs are used: {action_verbs_count+20} times")

        action_verbs_count = count_action_verbs(' '.join(candidate[field] or "" for field in resume_fields))
        if action_verbs_count > 20:
            score += 1
        else:
            score -= 0.5

        # Adjust score based on pronouns
        has_pronoun = has_pronouns(' '.join(candidate[field] or "" for field in resume_fields))
        if has_pronoun:
            score -= 0.5

        if score >= 9:
            resume_status = "Excellent"
        elif 6 <= score <= 9:
            resume_status = "Average"
        else:
            resume_status = "Bad"

        candidates_data.append({
            'user_id': candidate['user_id'],
            'score': score,
            'resume_status': resume_status,
            'area_of_improvement': area_of_improvement,
        })

    return render(request, 'admin/success.html', {'candidates': candidates_data})
