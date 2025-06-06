import re
from collections import Counter
from io import BytesIO

import matplotlib.pyplot as plt
from django.http import HttpResponse

from Analysis.models import Candidate
from utils import industry_keywords


def display_graph_top_industries(request):
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
    industry_keyword_counts = {industry: sum(keyword_counts.get(keyword, 0) for keyword in keywords) for industry, keywords in industry_keywords.items()}

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
    ax.set_title('Top Ten Industries based on Job Titles')
    plt.xticks(rotation=30, fontsize=8, ha='right')

    # Save the graph to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Set the appropriate response headers
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'inline; filename=graph.png'
    print(industry_names)
    print(industry_counts)
    # Send the buffer content as the HTTP response
    response.write(buffer.getvalue())
    return response
