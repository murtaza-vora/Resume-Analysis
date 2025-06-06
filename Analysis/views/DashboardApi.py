
import datetime
import re
import string
from collections import Counter

import nltk
import pandas as pd
from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse
from io import BytesIO
import matplotlib.pyplot as plt
import pycountry

from Analysis.models import Candidate
from utils import industry_keywords


def count_action_verbs(text):
    tags = nltk.pos_tag(text.split())
    action_verb_count = sum(1 for word, tag in tags if tag.startswith('VB'))
    return action_verb_count


def has_pronouns(text):
    tags = nltk.pos_tag(text.split())
    pronouns = [word for word, tag in tags if tag == 'PRP']
    return len(pronouns) > 0


def normalize_country(country):
    try:
        country_obj = pycountry.countries.search_fuzzy(country)[0]
        return country_obj.name
    except LookupError:
        return country


def dashboard(request):
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
        if action_verbs_count > 20:
            area_of_improvement.append(f"Action verbs are used: {action_verbs_count + 20} times")

        action_verbs_count = count_action_verbs(' '.join(candidate[field] or "" for field in resume_fields))
        if action_verbs_count > 20:
            score += 1
        else:
            score -= 0.5

        # Adjust score based on pronouns
        has_pronoun = has_pronouns(' '.join(candidate[field] or "" for field in resume_fields))
        if has_pronoun:
            score -= 0.5

        if score >= 8:
            resume_status = "Excellent"
        elif 5 <= score <= 7:
            resume_status = "Average"
        else:
            resume_status = "Bad"

        candidates_data.append({
            'user_id': candidate['user_id'],
            'score': score,
            'resume_status': resume_status,
            'area_of_improvement': area_of_improvement,
        })

    # Total number of users
    total_users = Candidate.objects.count()
    candidate_countries = Candidate.objects.values_list('country', flat=True)

    # Create a set to store unique and correctly spelled country names
    unique_countries = set()

    # Use pycountry to validate and standardize country names
    for country_name in candidate_countries:
        try:
            country = pycountry.countries.lookup(country_name)
            unique_countries.add(country.name)
        except LookupError:
            # Ignore misspelled or incorrect values
            pass

    total_countries = len(unique_countries)

    # Percentage of users with a degree
    total_users_with_degree = Candidate.objects.exclude(education='').count()
    percentage_with_degree = (total_users_with_degree / total_users) * 100 if total_users > 0 else 0

    # Single degree holders and multiple degree holders
    single_degree_holders = Candidate.objects.filter(education__contains='|').count()
    multiple_degree_holders = total_users_with_degree - single_degree_holders

    # Percentage of users with job experience
    total_users_with_experience = Candidate.objects.exclude(job_title='').count()
    percentage_with_experience = (total_users_with_experience / total_users) * 100 if total_users > 0 else 0

    # Total number of users with no previous job
    users_with_no_previous_job = Candidate.objects.filter(previous_organization='').count()
    percentage_with_no_previous_job = (users_with_no_previous_job / total_users) * 100 if total_users > 0 else 0

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
    industry_keyword_counts = {industry: sum(keyword_counts.get(keyword, 0) for keyword in keywords) for
                               industry, keywords in industry_keywords.items()}

    # Sort the industries based on their keyword counts in descending order
    sorted_industries = sorted(industry_keyword_counts.items(), key=lambda x: x[1], reverse=True)

    # Take the top ten industries
    top_industries = sorted_industries[:10]

    industry_names = [industry for industry, count in top_industries]
    industry_counts = [count for industry, count in top_industries]

    # Define age range bins
    age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Retrieve candidates and their age data
    candidates = Candidate.objects.all()
    ages = []

    for candidate in candidates:
        try:
            graduation_dates = candidate.graduation_date.strip("[]").replace("'", "").split(", ")
            if "Education Missing" in graduation_dates or len(graduation_dates) == 0:
                continue  # Skip candidates with missing graduation date

            graduation_years = []

            # Check if the list of graduation dates is not empty
            if graduation_dates:
                for date in graduation_dates:
                    if date.strip():  # Check if the date is not empty
                        if len(date) == 4:
                            graduation_years.append(int(date))
                        else:
                            # Parse the date string to extract the year
                            graduation_years.append(datetime.datetime.strptime(date, "%B %Y").year)

            if len(graduation_years) >= 2:
                # Calculate the difference in years between two dates
                age = graduation_years[-1] - graduation_years[0]
            elif graduation_years:
                # Use the first graduation year
                age = datetime.date.today().year - graduation_years[0]
            else:
                # Handle cases where no graduation year is available
                age = None

            if age is not None:
                ages.append(age)
        except (AttributeError, ValueError):
            pass

    # Retrieve the top 10 countries with the highest candidate count
    country_counts = (
        Candidate.objects
        .values('country')
        .annotate(count=Count('country'))
        .order_by('-count')[:10]
    )
    maximum_country_users = country_counts = (
        Candidate.objects
        .values('country')
        .annotate(count=Count('country'))
        .order_by('-count').exclude(country__isnull=True).exclude(country__exact='')[:1]
    )
    # Normalize country names
    country_counts = [{'country': normalize_country(item['country']), 'count': item['count']}
                      for item in
                      country_counts]


    data = {

        'country_data': country_counts,
        'total_users': total_users,
        'unique_countries': total_countries,
        'percentage_with_degree': percentage_with_degree,
        'single_degree_holders': single_degree_holders,
        'multiple_degree_holders': multiple_degree_holders,
        'percentage_with_experience': percentage_with_experience,
        'users_with_no_previous_job': maximum_country_users.values('country')[0]['country'],
        'percentage_with_no_previous_job': percentage_with_no_previous_job,
        'average_age': max(ages, key=ages.count),
        "candidates": candidates_data
    }

    return render(request, 'admin/dashboard.html', data)
