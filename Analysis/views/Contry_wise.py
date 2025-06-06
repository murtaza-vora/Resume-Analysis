# from io import BytesIO
# import matplotlib.pyplot as plt
# from django.db.models import Count
# from django.http import HttpResponse
# from django.shortcuts import render
#
# from Analytical_app.models import Candidate
#
#
# def Country_wise(request):
#     # Retrieve the top 10 countries with the highest candidate count
#     country_counts = (
#         Candidate.objects
#         .values('country')
#         .annotate(count=Count('country'))
#         .order_by('-count')[:10]
#     )
#     countries = [item['country'] if item['country'] else 'Others' for item in country_counts]
#     counts = [item['count'] for item in country_counts]
#
#     # Set the figure size
#     plt.figure(figsize=(10, 6))
#
#     # Generate the graph
#     plt.bar(countries, counts)
#     plt.xlabel('Country')
#     plt.ylabel('Count')
#     plt.title('Top 10 Countries with Highest Candidate Count')
#     plt.xticks(rotation=30, fontsize=8, ha='right')
#
#     # Save the graph to a buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#
#     # Set the appropriate response headers
#     response = HttpResponse(content_type='image/png')
#     response['Content-Disposition'] = 'inline; filename=graph.png'
#
#     # Send the buffer content as the HTTP response
#     response.write(buffer.getvalue())
#     return response

from io import BytesIO
import matplotlib.pyplot as plt
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
import pycountry

from Analysis.models import Candidate


def normalize_country(country):
    """
    Normalize the country name to consider different variations and short forms.
    """
    try:
        country_obj = pycountry.countries.search_fuzzy(country)[0]
        return country_obj.name
    except LookupError:
        return country


def Country_wise(request):
    # Retrieve the top 10 countries with the highest candidate count
    country_counts = (
        Candidate.objects
        .values('country')
        .annotate(count=Count('country'))
        .order_by('-count')[:10]
    )

    # Normalize country names
    country_counts = [{'country': normalize_country(item['country']), 'count': item['count']} for item in
                      country_counts]

    countries = [item['country'] if item['country'] else 'Others' for item in country_counts]
    counts = [item['count'] for item in country_counts]

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Generate the graph
    plt.bar(countries, counts)
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.title('Top 10 Countries with Highest Candidate Count')
    plt.xticks(rotation=30, fontsize=8, ha='right')

    # Save the graph to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    print(countries)
    print(counts)
    # Set the appropriate response headers
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'inline; filename=graph.png'

    # Send the buffer content as the HTTP response
    response.write(buffer.getvalue())
    return response
