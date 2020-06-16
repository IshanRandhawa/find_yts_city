from .forms import userinput
from apiclient.discovery import build 
from .models import channel
import pickle




def logic(querydata,locationdata,max_results):
    keys = ['AIzaSyB00zp9PuOd2FjQwroDQAAUswAOsFJbZq0',
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
        'AIzaSyD4Ftwh1IOuXuG9iWayZuEq-RH0BLsSf-8',
        'AIzaSyBpG9A7ZGHNRZjSinIzf9xuwrA5Q6cZb-U']
    global qouta
    qouta = 0
    global js 
    js = 1
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    with open("Indian_city_location.txt", "rb") as fp:
        city_list_location= pickle.load(fp)

        
    youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = keys[0])
    idlist = [[] for _ in range(5)]
    def get_ids_from_location(youtube_object):
        global qouta
        global js
        c = 0 #counter for each specific query [game][city] total 54 specific query average results per query = 300 total should be 300*54 == 16,200
        for query in querydata: 
            for location in locationdata:
                print(query , location[0])
                token = None
                for i in range(0,1):
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
                                            location= location[1],
                                            locationRadius="300km",
                                                maxResults = max_results).execute() 
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
        return idlist , youtube_object
        
    get_ids_from_location(youtube_object)
        
    def numberofids():  #get number of total ids
        c = 0
        for i in idlist:
            c = c + len(i)
        return c
    # numberofids()

    def unique_id(): #maintain order but remove duplicates
        for i in range(len(idlist)):
            idlist[i] = list(dict.fromkeys(idlist[i]))
        return idlist
    
    unique_id()

    def get_channel_statistics(youtube_object):
        check = []
        global qouta
        global js
        ids = idlist
        for tk in range(len(ids)):   #loop for each specific query
            for j in range(len(ids[tk])-2): #loop over unique ids in the query
                print (ids[tk][len(ids[tk])-1],ids[tk][len(ids[tk])-2], ids[tk][j])
                channeldata = youtube_object.channels().list(part="snippet,statistics",id=ids[tk][j])
                response = channeldata.execute()
                qouta += 5
                if qouta > 500:
                    youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = keys[js])
                    print (js , 'key changed')
                    js +=1
                    if js == len(keys):
                        js = 0
                    qouta = 0
                if not response.get('items'):
                    continue
                for item in response['items']:
                    channel_attrs = {
                                "Channel_id": item['id'],
                                "Channel_name": item['snippet']['title'],
                                "Channel_subscribers": item['statistics']['subscriberCount'],
                                "Channel_views": item['statistics']['viewCount'],
                                "Channel_video_count": item['statistics']['videoCount'],                          
                                "Channel_query": str(ids[tk][len(ids[tk])-2]),
                                "Channel_city": str(ids[tk][len(ids[tk])-1])            
                                }
                try:
                    Channel = channel.objects.create(**channel_attrs)
                    Channel.save()
                except:
                    continue
        return qouta, js , youtube_object
    get_channel_statistics(youtube_object)