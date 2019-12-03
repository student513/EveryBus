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

    return render(request, 'ebuapp/home.html', {'ID_list': data})

###########################################################
# 버스 번호로 검색하기
def saveDict(dictData, num):
    if(num==0):
        save = dictData
    elif(num==1):
        return save

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

def show_list(request):#검색어와 관련된 버스노선 목록을 출력
    #strSrch = request.GET.get() 검색어는 어떻게 받아올까?
    Nm_list=[]
    dictData_1 = getBusRouteId("110")# dictData_1 : 검색어를 포함하는 버스노선 정보 getBusRouteList
    for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
        Nm_list.append(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm'])

    return render(request, 'ebuapp/list.html', {'Nm_list': Nm_list})

def getStation_Nm_No(busRouteId):#노선 ID로 정류소 고유번호, 이름을 포함한 dict반환
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

def search(request):#, BusNm): #list.html에서 받아온 정확한 버스노선번호로 ID를 도출한다.
    station_Nm_List=[]
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
    #정류소 순번을 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_No_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['stationNo'])
    #return render(request, 'ebuapp/search.html',{'station_Nm_List':dictData_2})
    return render(request, 'ebuapp/search.html',{'station_Nm_List':station_Nm_List, 'busId':busId})

#dictData를 어떻게 global하게 할까? https://korbillgates.tistory.com/98


def parse_station_Nm_No():#정류소 고유번호, 이름 파싱하고 순번 구하는 함수에 넘겨줌/ 수정사항:정류소 이름목록을 검색결과창에 띄워야함
    jsonData = getStation_Nm_No(busRouteId)
    stationNm = (str(jsonData['ServiceResult']['msgBody']['stationNm']))
    stationNo = (str(jsonData['ServiceResult']['msgBody']['stationNo']))
    arr_Nm_No={stationNm,stationNo}
    return get_station_ord(arr_Nm_No[1])

def get_station_ord(stationNo):#정류소 고유번호로 정류소 순번 구하는 함수
    end_point = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid"
    
    parameters = "?_type=json&serviceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&arsId" + stationNo

    url = end_point + parameters
    
    retData = get_request_url(url)
    
    if (retData == None):
        return None
    else:
        return request.get(retData).json()

def parse_staOrd():#정류소 순번 get
    jsonData = get_station_ord(stationNo)
    staOrd = str(jsonData['ServiceResult']['msgBody']['staOrd'])
    return staOrd
#########################################################
#정류소명으로 검색하기
def get_station_Id_name(stSrch):
    end_point = "http://ws.bus.go.kr/api/rest/stationinfo/getLowStationByName"
    
    parameters = "?_type=json&serviceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&stSrch" + stSrch

    url = end_point + parameters
    
    retData = get_request_url(url)
    
    if (retData == None):
        return None
    else:
        return request.get(retData).json()

#정류소명 검색어로 정류소ID와 정류소명 받아오기
def parse_tId_stNm():
    jsonData = get_station_Id_name(stSrch)
    stationNm = (str(jsonData['ServiceResult']['msgBody']['stationNm']))
    stationNo = (str(jsonData['ServiceResult']['msgBody']['stationNo']))
    arr_tId_stNm={}


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