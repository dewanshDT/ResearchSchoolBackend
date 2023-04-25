from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .scrape import getResearchPapers

# Create your views here.


def index(request):
    searchQuery = request.GET.get('searchQuery')
    papers = []
    if searchQuery:
        papers = getResearchPapers(searchQuery, 0)

    return render(request, 'scholar/index.html', {"searchQuery": searchQuery, 'papers': papers})
