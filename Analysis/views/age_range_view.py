import datetime
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from Analysis.models import Candidate


def candidate_graph(request):
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
                ages.append(age + 21)
        except (AttributeError, ValueError):
            pass

    # Create histogram for age ranges
    for x in ages:
        if x > 0:
            ages.append(x)
    print(ages)
    fig, ax = plt.subplots()
    ax.hist(ages, bins=age_bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Age Range')
    ax.set_ylabel('Number of Candidates')
    ax.set_title('Distribution of Candidates by Age Range')
    plt.xticks(age_bins)
    plt.tight_layout()

    # Render the graph to the canvas
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response
