import datetime
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from Analysis.models import Candidate


def candidate_graph_exp(request):
    # Define experience range bins
    experience_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Retrieve candidates and their experience data
    candidates = Candidate.objects.all()
    experiences = []

    for candidate in candidates:
        try:
            graduation_dates = candidate.graduation_date.strip("[]").replace("'", "").split(", ")
            if "Education Missing" in graduation_dates or len(graduation_dates) < 2:
                continue  # Skip candidates with missing or insufficient graduation dates

            graduation_years = []

            for date in graduation_dates:
                if date.strip():  # Check if the date is not empty
                    if len(date) == 4:
                        graduation_years.append(int(date))
                    else:
                        # Parse the date string to extract the year
                        graduation_years.append(datetime.datetime.strptime(date, "%B %Y").year)

            # Calculate the experience in years
            experience = graduation_years[-1] - graduation_years[0]

            if experience > 0:
                experiences.append(experience)
        except (AttributeError, ValueError):
            pass

    # Create histogram for experience ranges
    fig, ax = plt.subplots()
    ax.hist(experiences, bins=experience_bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Experience Range (in years)')
    ax.set_ylabel('Number of Candidates')
    ax.set_title('Distribution of Candidates by Experience Range')
    plt.xticks(experience_bins)
    plt.tight_layout()

    # Render the graph to the canvas
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response
