from django.shortcuts import render
import urllib.request
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import os
import sys
import datetime
import time
import json
from config import *
import math

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
###########################################################
# 버스 번호로 검색하기
def getBusRouteId(strSrch):#버스 번호 입력하여 노선ID 반환
    
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
    
    parameters = "?_type=json&serviceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&strSrch=" + strSrch

    url = end_point + parameters
    
    retData = get_request_url(url)
    
    if (retData == None):
        return None
    else:
        return request.get(retData).json()

def parse_RouteId():#노선ID get / 수정사항 : 버스번호로 검색하면 그 번호를 포함한 모든 버스목록 표시, 그중 하나 누르면 그 버스의 노선ID반환
    jsonData = getBusRouteId(strSrch)
    ###
    ###
    return getStation_Nm_No(str(jsonData['ServiceResult']['msgBody']['busRouteId']))

def getStation_Nm_No(busRouteId):#parse_RouteId를 이용해 얻은 노선 ID로 정류소 고유번호, 이름 반환
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"
    
    parameters = "?_type=json&serviceKey=" + "KfsKvr7vCiATWu1bthGHoUmNu0mCeCHwk75nar9Aoti0j5t9RjlY2Uhhcs6v%2Fb5xTB6pf6xLmvVa7QIz5SkTBA%3D%3D"
    parameters += "&busRouteId" + busRouteId

    url = end_point + parameters
    
    retData = get_request_url(url)
    
    if (retData == None):
        return None
    else:
        return request.get(retData).json()

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
def home(request):
    return render(request, 'ebuapp/home.html')

def search(request):
    return render(request, 'ebuapp/search.html')

def detail(request):
    render(request, 'ebuapp/detail.html')

def bookmark(request):
    render(request, 'ebuapp/bookmark.html')

def post_list(request):#검색알고리즘 https://wayhome25.github.io/django/2017/05/04/django-queryset-search/
    qs = Post.objects.all()

    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    return render(request, 'blog/post_list.html', {
        'post_list' : qs,
        'q' : q,
    })