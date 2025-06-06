"""
URL configuration for Coverquick_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from Analysis.views.Contry_wise import Country_wise
from Analysis.views.DashboardApi import dashboard
from Analysis.views.ResumeAPI import score_candidate
from Analysis.views.abc import abc
from Analysis.views.age_range_view import candidate_graph
from Analysis.views.majority_industries_views import display_graph_top_industries


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    # path('display_graph_top_industries/', display_graph_top_industries, name='display_graph_top_industries'),
    path('score_candidate/', score_candidate, name='score_candidate'),
    # path('candidate_graph/', candidate_graph, name='candidate_graph'),
    path('country_wise/', Country_wise, name='country_wise'),
    # path('country/', Country_wise, name='display_graph'),
    path('industry/', display_graph_top_industries, name='display_graph'),
    path('age-data/', candidate_graph, name='get_age_data'),
    path('abc/', abc, name='score_candidate'),
]

