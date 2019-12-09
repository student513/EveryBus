from django.shortcuts import render, redirect, get_object_or_404
import os
import sys
import urllib.request
import json
import time
import math
import datetime
import requests
import xmltodict
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus

from django.db.models import Q
from django.shortcuts import render
from django.template.defaulttags import register
def home(request):
    return render(request, 'ebuapp/home.html')

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


def stop_search(request):
    stationpair = {}    #초기화
    url = 'http://ws.bus.go.kr/api/rest/stationinfo/getLowStationByName?ServiceKey=O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D&stSrch='
    word = request.GET.get('q') #입력받은 단어 word 변수에 저장
    c_word = urllib.parse.quote(word)
    url = url + c_word
    retData = get_request_url(url)
    todict = xmltodict.parse(retData)
    json_type = json.dumps(todict)
    data = json.loads(json_type)
    if(data['ServiceResult']['msgHeader']['headerMsg'] != '결과가 없습니다.'):  #검색어에 해당하는 정류소가 있는 경우
        for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
            stationpair[data['ServiceResult']['msgBody']['itemList'][i]['stId']] = data['ServiceResult']['msgBody']['itemList'][i]['stNm']
    else: #검색어에 해당하는 정류소가 없는 경우 
        return render(request, 'ebuapp/no_name.html')
    return render(request, 'ebuapp/stop_search.html', {'stationpair' : stationpair})

# def stop(request, stationid): #정류소에 접근하는 저상버스 목록
#     if request.method == 'GET':
#         url = 'http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey=O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D&stId='
#         url = url + str(stationid)
#         retData = get_request_url(url)
#         todict = xmltodict.parse(retData)
#         json_type = json.dumps(todict)
#         data = json.loads(json_type)
#         #버스 ID - busrouteID
#         #버스 번호 - rtNm
#         #첫번째 도착 예정 버스 메시지 - 'arrmsg1'
#         #두번째 도착 예정 버스 메시지 - 'arrmsg2'
#         busset = [[0]*4 for i in range(len(data['ServiceResult']['msgBody']['itemList']))] 
#         for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
#             busset[i][0] = data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
#             busset[i][1] = data['ServiceResult']['msgBody']['itemList'][i]['rtNm']
#             busset[i][2] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1']
#             busset[i][3] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg2']
#     return render(request, 'ebuapp/stop.html', {'busset' : busset})

def stop(request, stationid): #정류소에 접근하는 저상버스 목록
    if request.method == 'GET':
        url = 'http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey=O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D&stId='
        url = url + str(stationid)
        retData = get_request_url(url)
        todict = xmltodict.parse(retData)
        json_type = json.dumps(todict)
        data = json.loads(json_type)
        #버스 ID - busrouteID
        #버스 번호 - rtNm
        #첫번째 도착 예정 버스 메시지 - 'arrmsg1'
        #두번째 도착 예정 버스 메시지 - 'arrmsg2'
        buspair = {}
        busset = [[0]*4 for i in range(len(data['ServiceResult']['msgBody']['itemList']))] 
        for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
            busset[i][0] = data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
            busset[i][1] = data['ServiceResult']['msgBody']['itemList'][i]['rtNm']
            busset[i][2] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1']
            busset[i][3] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg2']

            buspair[data['ServiceResult']['msgBody']['itemList'][i]['rtNm']] = data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
    return render(request, 'ebuapp/stop.html', {'busset' : busset, 'buspair':buspair})
def getBusRouteId(strSrch):#버스 번호 입력하여 노선ID 반환
    
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
    parameters = "?ServiceKey=" + "O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D"
    
    end_point = end_point + parameters + "&strSrch=" + strSrch
    retData = get_request_url(end_point)
    print(retData)
    todict = xmltodict.parse(retData)
    json_type = json.dumps(todict)
    data = json.loads(json_type)

    if (data == None):
        return None
    else:
        return data

to_use_get_id = ''
buspair = {}

def bus_search(request):#검색어와 관련된 버스노선 목록을 출력
    #strSrch = request.GET.get() 검색어는 어떻게 받아올까?
    buspair.clear()

    Nm_list=[]
    word = request.GET.get('q') #입력받은 단어 word 변수에 저장
    print(word)
    c_word = urllib.parse.quote(word)
    print(c_word)
    to_use_get_id = c_word
    dictData_1= getBusRouteId(c_word) # dictData_1 : 검색어를 포함하는 버스노선 정보 getBusRouteList

    # if len(dictData_1['ServiceResult']['msgBody']['itemList']) == 1 :
    #     buspair[dictData_1['ServiceResult']['msgBody']['itemList']['busRouteNm']] = dictData_1['ServiceResult']['msgBody']['itemList']['busRouteId']

    try:
        for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
            buspair[dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm']] = dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
    except KeyError :
        buspair[dictData_1['ServiceResult']['msgBody']['itemList']['busRouteNm']] = dictData_1['ServiceResult']['msgBody']['itemList']['busRouteId']
    except TypeError :
        return render(request, 'ebuapp/no_name.html')
    return render(request, 'ebuapp/bus_search.html', {'buspair' : buspair})#'Nm_list': Nm_list, 'dictData_1':dictData_1, 

def getStation_Nm_No(busRouteId):#노선 ID로 정류소ID, 이름을 포함한 dict반환
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"
    
    parameters = "?ServiceKey=" + "O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D"
    parameters += "&busRouteId=" + str(busRouteId)
    url = end_point + parameters
    
    retData = get_request_url(url)
    
    asd = xmltodict.parse(retData)
    json_type = json.dumps(asd)
    data = json.loads(json_type)
    
    if (data == None):
        return None
    else:
        return data

def bus(request, busid):#, BusNm): #bus_search.html에서 받아온 정확한 버스노선번호로 ID를 도출한다.
    station_Nm_List=[]

    ### global로 사용할 것들
    station_No_List=[]
    ###

    # dictData_1 = getBusRouteId(to_use_get_id)
    # ###
    # # dictData_1를 global로 선언하는 방법? : dictData_1반환 함수를 하나 만들자
    # for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
    #     if str(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm']) == BusNm:
    #         busId = str(dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteId'])

    dictData_2 = getStation_Nm_No(busid)# dictData_2 : 노선ID로 정류장이름, 순번을 포함한 dict. getStaionsByRouteList 

    No_Nm_list={}

    #정류소 이름을 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_Nm_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['stationNm'])
    #정류소 ID를 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_No_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['station'])
    #return render(request, 'ebuapp/search.html',{'station_Nm_List':dictData_2})
    
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        No_Nm_list[station_No_List[i]] = station_Nm_List[i]
    
    return render(request, 'ebuapp/bus.html',{'No_Nm_list':No_Nm_list})


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)