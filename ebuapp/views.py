from django.shortcuts import render
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import os
import sys
import datetime
import time
import json
import math
import xmltodict
import requests

dicdat ={}

def get_request_url(url):
    
    req = urllib.request.Request(url)
    
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def home(request):#버스 번호 입력하여 노선ID 반환
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"
    
    parameters = "?ServiceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&busRouteId=" + "100100112"
    url = end_point + parameters
    
    retData = get_request_url(url)
    
    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)

    dicdat ={1: 5, 2: 3}

    return render(request, 'ebuapp/home.html', {'ID_list': data, 'dicdat':dicdat})

###########################################################
# 버스 번호로 검색하기

#dictData_1 = {}
#dictData_2 = {}
#station_No_List=[]

#얘네를 dict로 저장해서 {busId:~~~, stationNo:~~~, staOrd:~~~}이렇게 저장할 수 있나?
#busId=""
#stationNo=""
#staOrd=""

def getBusRouteId(strSrch):#버스 번호 입력하여 노선ID 반환
    
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
    parameters = "?ServiceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&strSrch=" + strSrch
    url = end_point + parameters
    
    retData = get_request_url(url)

    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)

    if (data == None):
        return None
    else:
        return data

def bus_search(request):#검색어와 관련된 버스노선 목록을 출력
    #strSrch = request.GET.get() 검색어는 어떻게 받아올까?
    Nm_list=[]
    dictData_1= getBusRouteId("110")# dictData_1 : 검색어를 포함하는 버스노선 정보 getBusRouteList
    for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
        Nm_list.append(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm'])

    return render(request, 'ebuapp/bus_search.html', {'Nm_list': Nm_list, 'dictData_1':dictData_1})

def getStation_Nm_No(busRouteId):#노선 ID로 정류소ID, 이름을 포함한 dict반환
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"
    
    parameters = "?ServiceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&busRouteId=" + busRouteId
    url = end_point + parameters
    
    retData = get_request_url(url)
    
    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)
    
    if (data == None):
        return None
    else:
        return data

def bus(request):#, BusNm): #bus_search.html에서 받아온 정확한 버스노선번호로 ID를 도출한다.
    station_Nm_List=[]

    ### global로 사용할 것들
    station_No_List=[]
    busId=""
    ###

    BusNm="110A고려대"
    dictData_1 = getBusRouteId("110")
    ###
    # dictData_1를 global로 선언하는 방법? : dictData_1반환 함수를 하나 만들자
    for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
        if str(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm']) == BusNm:
            busId = str(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteId'])

    dictData_2 = getStation_Nm_No(busId)# dictData_2 : 노선ID로 정류장이름, 순번을 포함한 dict. getStaionsByRouteList 
    #정류소 이름을 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_Nm_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['stationNm'])
    #정류소 ID를 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_No_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['station'])
    #return render(request, 'ebuapp/search.html',{'station_Nm_List':dictData_2})
    return render(request, 'ebuapp/bus.html',{'station_Nm_List':station_Nm_List, 'busId':busId})

def get_row_arr(stationId):#정류소 고유번호로 정류소 순번 구하는 함수
    end_point = "http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId"
    
    parameters = "?ServiceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&stId=" + stationId
    url = end_point + parameters
    
    retData = get_request_url(url)
    
    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)

    if (data == None):
        return None
    else:
        return data

def get_busRouteNm(busRouteId):
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getRouteInfo"
    
    parameters = "?ServiceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&busRouteId=" + busRouteId
    url = end_point + parameters
    
    retData = get_request_url(url)
    
    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)

    if (data == None):
        return None
    else:
        return data


#station_No_List, station_Nm_List 둘 다 global해야함
def stop(request):#,stationNm):
    arrive_time_list=[]
    busId_list=[]
    
    ###
    stationNm = "정릉북한산국립공원입구"
    dictData_2 = getStation_Nm_No("100100016")
    ###
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        if stationNm == dictData_2['ServiceResult']['msgBody']['itemList'][i]['stationNm']:
            stationId = str(dictData_2['ServiceResult']['msgBody']['itemList'][i]['station'])
    
    arrive_time_dict = get_row_arr(stationId)
    #각 itemList의 arrmsg1 가져올것
    #그러나 버스노선이름이 없다! busRouteId를 가져와 getBusRouteId호출하여 버스노선이름 다 띄워주자
    for i in range(len(arrive_time_dict['ServiceResult']['msgBody']['itemList'])):
        arrive_time_list.append(arrive_time_dict['ServiceResult']['msgBody']['itemList'][i]['arrmsg1'])

    for i in range(len(arrive_time_dict['ServiceResult']['msgBody']['itemList'])):
        busId_list.append(arrive_time_dict['ServiceResult']['msgBody']['itemList'][i]['busRouteId'])


    arrmsg_busId=[["" for i in range(3)] for j in range(len(arrive_time_dict['ServiceResult']['msgBody']['itemList']))]

    #arrmsg1과 busRouteId를 묶어서 저장
    for i in range(len(arrive_time_dict['ServiceResult']['msgBody']['itemList'])):
        arrmsg_busId[i][0] = arrive_time_list[i]
        arrmsg_busId[i][1] = busId_list[i]

    #busRouteId(노선Id)로 그버스의 busRouteNm(노선이름)을 찾아야함
    for i in range(len(arrmsg_busId)):
        Nm_dict= get_busRouteNm(busId_list[i])
        arrmsg_busId[i][2] =Nm_dict['ServiceResult']['msgBody']['itemList']['busRouteNm']
    # Nm_list=[]
    # dictData_1= getBusRouteId("110")# dictData_1 : 검색어를 포함하는 버스노선 정보 getBusRouteList
    # for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
    #     Nm_list.append(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm'])

    return render(request, 'ebuapp/stop.html',{'arrive_time_list':arrive_time_list,'arrmsg_busId':arrmsg_busId})


#########################################################
#########################################################
def post_list(request):#검색알고리즘 https://wayhome25.github.io/django/2017/05/04/django-queryset-search/
    qs = Post.objects.all()

    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    return render(request, 'blog/post_list.html', {
        'post_list' : qs,
        'q' : q,
    })


def detail(request):
    render(request, 'ebuapp/detail.html')

def bookmark(request):
    render(request, 'ebuapp/bookmark.html')