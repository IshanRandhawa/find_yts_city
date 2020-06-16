
from django.shortcuts import render , HttpResponse
from .forms import userinput
from apiclient.discovery import build 
import pandas as pd
from pandas.io.json import json_normalize
from collections import OrderedDict 
from math import floor







keys = ['AIzaSyBpG9A7ZGHNRZjSinIzf9xuwrA5Q6cZb-U',
        'AIzaSyAo7avr3LCs3SYVDO1N-MJpaqXY8eyAmqs',
        'AIzaSyA6rs5yQ9hGItVCs95hUbAfM81FQKd0aeo',
        'AIzaSyASHwkdbJHCKZpX2YmOXlKL1EIBM7iNO1M',
        'AIzaSyD23mnEOyGuRXA6JeheTHf_pNG9xy8l0jA',
        'AIzaSyBU5G94AVLCgcVLJX0rUImzE-hcVBJNFyo',
        'AIzaSyDZuFK1HIafmBi8tN5YMNmr818SjaPSN_E',
        'AIzaSyC89-z5XYM-fGWHOVBZKP8AY2APmGLJSy4',
        'AIzaSyBzNme1vCHaLaYrnPD9gpWJ01mGKK2qaQs',
        'AIzaSyCuDPtDQdk2V7miBnIGYsfUWFyTDXPCDzE',
        'AIzaSyDbfLXXRrE5701sIzg7kJZ_3nxJA9tJAnE',
        'AIzaSyA5FOiV5a3RPa0YJoUs4dKSdyxzylLAg9o',
        'AIzaSyChXvBe1RmsZlm9tvSHYhg9yQMYOx9zHZA',
        'AIzaSyCmLhFe_CS3OMjWrLtJbSW5_u2zGjXiCp8',
        'AIzaSyD4Ftwh1IOuXuG9iWayZuEq-RH0BLsSf-8']
global qouta
qouta = 0
global js 
js = 1







def home_view(request): 
    context ={} 
  
    # create object of form 
    form = userinput(request.POST or None, request.FILES or None) 
      
    # check if form data is valid 
    if form.is_valid(): 
        query = form.cleaned_data['query']
        city = form.cleaned_data['city']
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        query = str(query)
        querydata = [query]
        locationdata = [['NCR','28.610001,77.230003'], ['Ahmedabad', '23.007950, 72.553757']]
        idlist = [[] for _ in range(10)]

        youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = keys[0])
        global qouta
        global js
        c = 0 #counter for each specific query [game][city] total 54 specific query average results per query = 300 total should be 300*54 == 16,200
        for query in querydata: 
            
            for location in locationdata:
                print(query , location[0])
                token = None
                for i in range(0,2):
                    if qouta > 500:
                        youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = keys[js])
                        print (js , 'key changed')
                        js +=1
                        if js == len(keys):
                            js = 0
                        qouta = 0
                    res = youtube_object.search().list(q = query, 
                                            type ='video', 
                                            part = "snippet",
                                            pageToken = token,
                                            publishedAfter =  '2020-04-01T00:00:00Z',
                                            publishedBefore = '2020-05-01T00:00:00Z',
                                            videoCategoryId="20",                                    
                                            location= location[1],
                                            locationRadius="300km",
                                                maxResults = 50).execute() 
                    qouta+= 100
                    for item in res['items']:
                        idlist[c].append(item['snippet']['channelId'])     #append channelids to a list             
                    try:
                        if res['nextPageToken'] == None:
                            break;   
                    except:
                        break;            
                    token = res['nextPageToken']
                idlist[c].append(query)   #adding game
                idlist[c].append(location[0]) #adding location
                c+=1
            return HttpResponse(idlist)
        form.save()

  
    context['form']= form 
    return render(request, "home.html", context) 

