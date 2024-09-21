
from django.shortcuts import render
import wikipediaapi
import re
import requests
from fuzzywuzzy import process
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache

TMDB_API_KEY = 'your_tmdb_api_key'

def autocomplete_celebrity(request):
    query = request.GET.get('query', '')
    if query:
        url = f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&query={query}"
        response = requests.get(url)
        data = response.json()
        results = [{'name': person['name']} for person in data.get('results', [])]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def extract_details(personal_life_text):
    marital_status = None
    spouse = None
    ex = None
    rumors = None

    marriage_patterns = [r'(married to|marriage to) ([A-Z][a-z]+\s[A-Z][a-z]+)', r'(currently\s+married)']
    ex_patterns = [r'(divorced|separated from|ex-wife|ex-husband) ([A-Z][a-z]+\s[A-Z][a-z]+)']
    rumor_patterns = [r'(rumored to be dating|rumored relationship with|linked to) ([A-Z][a-z]+\s[A-Z][a-z]+)']

    for pattern in marriage_patterns:
        match = re.search(pattern, personal_life_text, re.IGNORECASE)
        if match:
            marital_status = match.group(0)
            spouse = match.group(2) if len(match.groups()) >= 2 else None

    for pattern in ex_patterns:
        match = re.search(pattern, personal_life_text, re.IGNORECASE)
        if match:
            ex = match.group(0)

    for pattern in rumor_patterns:
        match = re.search(pattern, personal_life_text, re.IGNORECASE)
        if match:
            rumors = match.group(0)

    return {
        'marital_status': marital_status or "No marital status info available.",
        'spouse': spouse or "No spouse info available.",
        'ex': ex or "No ex information available.",
        'rumors': rumors or "No rumors available."
    }

def get_celebrity_bio(request):
    if request.method == 'POST':
        celebrity_name = request.POST.get('celebrity_name')
        
        cached_bio = cache.get(celebrity_name)
        if cached_bio:
            return render(request, 'bio.html', {'bio_data': cached_bio})

        wiki_wiki = wikipediaapi.Wikipedia('en')

        page = wiki_wiki.page(celebrity_name)

        if page.exists():
            personal_life_section = ""
            for section in page.sections:
                if "Personal life" in section.title:
                    personal_life_section = section.text
                    break

            if personal_life_section:
                details = extract_details(personal_life_section)
            else:
                details = {
                    'marital_status': "No marital status info found.",
                    'spouse': "No spouse info found.",
                    'ex': "No ex information found.",
                    'rumors': "No rumors found."
                }

            bio_data = {
                'name': celebrity_name,
                'bio': personal_life_section if personal_life_section else "No Personal life info found.",
                **details
            }

            cache.set(celebrity_name, bio_data, timeout=3600)
            return render(request, 'bio.html', {'bio_data': bio_data})
        else:
            all_celebrities = ["Brad Pitt", "Angelina Jolie", "Tom Cruise", "Johnny Depp"]
            closest_match = process.extractOne(celebrity_name, all_celebrities)
            error_message = f"Celebrity not found. Did you mean {closest_match[0]}?"
            return render(request, 'bio.html', {'error_message': error_message})

    return render(request, 'bio.html')
