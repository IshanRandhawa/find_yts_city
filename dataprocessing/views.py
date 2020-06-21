
from django.shortcuts import render , HttpResponse, redirect
from .forms import userinput
from apiclient.discovery import build 

from django.http import JsonResponse , HttpResponseRedirect
from .models import channel
import pickle
from .app_logic import logic
from django.db.models import Q
from django.template import loader



global qouta
qouta = 0
global js 
js = 1
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


with open("Indian_city_location.txt", "rb") as fp:
    city_list_location= pickle.load(fp)
with open("qouta.txt", "rb") as fp: #importing current Qouta value
    qouta = pickle.load(fp)

def home_view(request):
    context ={} 
    # create object of form 
    form = userinput(request.POST or None, request.FILES or None) 
    # check if form data is valid 
    if form.is_valid(): 
        query = form.cleaned_data['query']
        city = form.cleaned_data['city']
        max_results = form.cleaned_data['number_queries'] 
        query = str(query)
        querydata = [query]
        locationdata = [city_list_location[city]]
        loc_value = locationdata[0][0]
        qouta = logic(querydata,locationdata,max_results)
        params={
            'query': query,
            'city': loc_value,
            'max_results': max_results,
        }
        filtereddata = channel.objects.filter(Q(Channel_query= params['query']) & Q(Channel_city = params['city']))
        context = {'filtereddata':filtereddata,
                    'qouta': qouta,
                    'query': query,
                    'city': loc_value,
             }
        context['Remaining_qouta'] = 490000 - qouta
        context['records'] = len(filtereddata)

        return render(request, 'list.html' , context) 
    else:
        with open("qouta.txt", "rb") as fp: #importing current Qouta value
            qouta = pickle.load(fp)
        context['form']= form 
        context['qouta'] = qouta
        context['Remaining_qouta'] = 490000 - qouta
        data = channel.objects.all()
        context['records'] = len(data)

        return render(request, "index.html", context) 

def table(request):
    context = {}
    context['qouta'] = qouta
    context['Remaining_qouta'] = 490000 - qouta
    data = channel.objects.all()
    context['data'] = data
    context['records'] = len(data)
    return render(request, 'database.html', context)


def subtable(request, context):
    query=request.GET.get('query')
    city=request.GET.get('city')
    locationdata = [city_list_location[city]]
    loc_value = locationdata[0][0]
    params={
    'query': query,
    'city': loc_value,
        }
    filtereddata = channel.objects.filter(Q(Channel_query= params['query']) & Q(Channel_city = params['city']))
    context = {'filtereddata':filtereddata,
             }
    context['Remaining_qouta'] = 490000 - qouta
    return render(request, 'list.html', context)
