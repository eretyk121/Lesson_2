from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from app.settings import BUS_STATION_CSV
import math
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse(bus_stations))

# def bus_stations(request):
#     station_list = []
#     with open(BUS_STATION_CSV, encoding='cp1251') as text:
#         read = csv.DictReader(text)
#         for row in read:
#             station_list.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
#     current_page = request.GET.get('page', 1)
#     current_page = int(current_page)
#     items_per_page = 20
#     total_pages = math.ceil(len(station_list) / items_per_page)
#     if current_page < 1 or \
#             current_page > total_pages:
#             current_page=1
#     articles = station_list[(current_page-1) * items_per_page: \
#             current_page * items_per_page]
#     prev_page, next_page = None, None
#     if current_page > 1:
#         prev_page = urlencode({'page':current_page-1})
#     if current_page * items_per_page < len(station_list):
#         next_page = urlencode({'page':current_page+1})
#     context = {
#         # 'bus_stations': [{'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}],
#         'bus_stations': Name_list,
#         'current_page': current_page,
#         'prev_page_url': None,
#         'next_page_url': next_page,
#     }
#
#     return render_to_response('index.html', context=context)

def bus_stations(request):
    articles = []
    with open(BUS_STATION_CSV, encoding='cp1251') as text:
        read = csv.DictReader(text)
        for row in read:
            articles.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
    paginator = Paginator(articles, 20)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)
    prev_page, next_page = None, None
    if page.has_previous():
        prev_page = page.previous_page_number()
    if page.has_next():
        next_page = page.next_page_number()
    context = {
        'bus_stations': page,
        'current_page': page.number,
        'prev_page_url': f'?page={prev_page}',
        'next_page_url': f'?page={next_page}',
    }

    return render_to_response('index.html', context=context)



# with open(BUS_STATION_CSV, encoding='cp1251') as text:
#     read = csv.DictReader(text)
#     for row in read:
#         print(row)
#         Name_list.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
# for station in Name_list:
#     print(station)
