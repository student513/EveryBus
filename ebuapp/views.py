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

from accounts import models as a_models
from accounts.forms import ProfileRegisterForm 
from django.contrib.auth.models import User


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

def station_nxst(arsId):
    ###정류소 방면 찾는 API
    url_nxst = 'http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D&arsId='
    #arsId = data['ServiceResult']['msgBody']['itemList']['arsId']
    url_nxst += str(arsId)
    retNxst = get_request_url(url_nxst)
    todict_nxst = xmltodict.parse(retNxst)
    json_type_Nxst = json.dumps(todict_nxst)
    data_Nxst = json.loads(json_type_Nxst)
    
    
    ### 맨 처음 nxtStn만 data_Nxst에 저장하고 싶다
    if (data_Nxst == None):
        return None
    else:
        return data_Nxst


def stop_search(request):

    if request.user.is_active == False:
        return render(request, 'ebuapp/stop_search.html')
    
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
        try:
            for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
                stationpair[data['ServiceResult']['msgBody']['itemList'][i]['stId']] = data['ServiceResult']['msgBody']['itemList'][i]['stNm']
        except KeyError : #검색결과가 한개일 경우
            stationpair[data['ServiceResult']['msgBody']['itemList']['stId']] = data['ServiceResult']['msgBody']['itemList']['stNm']
    else: #검색어에 해당하는 정류소가 없는 경우 
        return render(request, 'ebuapp/no_name.html')
    return render(request, 'ebuapp/stop_search.html', {'stationpair' : stationpair})

    # data_Nxst = station_nxst(data['ServiceResult']['msgBody']['itemList'][0]['arsId'])
    # Nxst = data_Nxst['ServiceResult']['msgBody']['itemList'][0]['nxtStn']
    
    # data_Nxst={}
    # Nxst={}
    # if(data['ServiceResult']['msgHeader']['headerMsg'] != '결과가 없습니다.'):  #검색어에 해당하는 정류소가 있는 경우
    #     try:
    #         for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
    #             data_Nxst = station_nxst(data['ServiceResult']['msgBody']['itemList'][i]['arsId'])
    #             #Nxst = data_Nxst['ServiceResult']['msgBody']['itemList'][0]['nxtStn']
    #             print(data_Nxst['ServiceResult']['msgBody']['itemList'][0]['nxtStn'])
    #             stationpair[data['ServiceResult']['msgBody']['itemList'][i]['stId']] = data_Nxst['ServiceResult']['msgBody']['itemList'][0]['nxtStn'] #data['ServiceResult']['msgBody']['itemList'][i]['stNm']
    #     except KeyError : #검색결과가 한개일 경우
    #         data_Nxst = station_nxst(data['ServiceResult']['msgBody']['itemList']['arsId'])
    #         Nxst = data_Nxst['ServiceResult']['msgBody']['itemList']['nxtStn']
    #         stationpair[data['ServiceResult']['msgBody']['itemList']['stId']] = data['ServiceResult']['msgBody']['itemList']['stNm']
    
    
    # else: #검색어에 해당하는 정류소가 없는 경우 
    #     return render(request, 'ebuapp/no_name.html')
    # return render(request, 'ebuapp/stop_search.html', {'stationpair' : stationpair})



    try:
        for i in range(len(dictData_1['ServiceResult']['msgBody']['itemList'])):
            buspair[dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteNm']] = dictData_1['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
    except KeyError :
        buspair[dictData_1['ServiceResult']['msgBody']['itemList']['busRouteNm']] = dictData_1['ServiceResult']['msgBody']['itemList']['busRouteId']
    except TypeError :
        return render(request, 'ebuapp/no_name.html')
    return render(request, 'ebuapp/bus_search.html', {'buspair' : buspair})#'Nm_list': Nm_list, 'dictData_1':dictData_1, 


def stop(request, stationid): #정류소에 접근하는 저상버스 목록
    profile =  ProfileRegisterForm(instance = request.user)
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
        buspair2 = {}
        busset = [[0]*4 for i in range(len(data['ServiceResult']['msgBody']['itemList']))] 
    try:
        staname = data['ServiceResult']['msgBody']['itemList'][0]['stNm']
        staid = data['ServiceResult']['msgBody']['itemList'][0]['stId']

        for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
            busset[i][0] = data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
            busset[i][1] = data['ServiceResult']['msgBody']['itemList'][i]['rtNm']
            busset[i][2] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1']
            busset[i][3] = data['ServiceResult']['msgBody']['itemList'][i]['arrmsg2']
            buspair[data['ServiceResult']['msgBody']['itemList'][i]['rtNm']] = data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']
            buspair2[data['ServiceResult']['msgBody']['itemList'][i]['busRouteId']] = data['ServiceResult']['msgBody']['itemList'][i]['rtNm']

    except KeyError : 
        return render(request, 'ebuapp/no_name.html')
    book=[]
    for key , value in profile.bookmark.items():
        book.append(str(key))
    return render(request, 'ebuapp/stop.html', {'busset' : busset, 'buspair':buspair, 'buspair2':buspair2, 'staname':staname, 'staid':staid, 'bookmark': book})
def getBusRouteId(strSrch):#버스 번호 입력하여 노선ID 반환
    
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
    parameters = "?ServiceKey=" + "O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D"
    
    end_point = end_point + parameters + "&strSrch=" + strSrch
    retData = get_request_url(end_point)
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
    if request.user.is_active == False:
        return render(request, 'ebuapp/bus_search.html')
    
    buspair.clear()

    Nm_list=[]
    word = request.GET.get('q') #입력받은 단어 word 변수에 저장
    c_word = urllib.parse.quote(word)
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

def get_busRoute_Nm(busRouteId):
    end_point = "http://ws.bus.go.kr/api/rest/busRouteInfo/getRouteInfo"
    
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
    profile =  ProfileRegisterForm(instance = request.user)
    station_Nm_List=[]

    ### global로 사용할 것들
    station_No_List=[]
    ###
    busNm_dict=get_busRoute_Nm(busid)
    busNm=busNm_dict['ServiceResult']['msgBody']['itemList']['busRouteNm']

    dictData_2 = getStation_Nm_No(busid)# dictData_2 : 노선ID로 정류장이름, 순번을 포함한 dict. getStaionsByRouteList 

    No_Nm_list={}
    now_location = []

    url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?ServiceKey=O1F7ztluCGyI1rB%2BVXh7Tux83RXDm4x4c5s5Nr1jZOZrD3v7uXF1LZvUHDyPTPm87qeLXFzeeoTN507bf1Ceow%3D%3D&busRouteId='
    url = url + str(busid)
    retData = get_request_url(url)
    todict = xmltodict.parse(retData)
    json_type = json.dumps(todict)
    data = json.loads(json_type)

    for i in range(len(data['ServiceResult']['msgBody']['itemList'])):
        print(type(data['ServiceResult']['msgBody']['itemList'][i]['busType1']))
        if data['ServiceResult']['msgBody']['itemList'][i]['busType1'] == '1':
            print(data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1'])
            if data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1'] == '곧 도착':
                now_location.append(data['ServiceResult']['msgBody']['itemList'][i]['stId'])
            elif '1번째 전' in data['ServiceResult']['msgBody']['itemList'][i]['arrmsg1']:
                now_location.append(data['ServiceResult']['msgBody']['itemList'][i-1]['stId'])

    print(now_location)
    #정류소 이름을 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_Nm_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['stationNm'])
    #정류소 ID를 리스트에 저장
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        station_No_List.append(dictData_2['ServiceResult']['msgBody']['itemList'][i]['station'])
    #return render(request, 'ebuapp/search.html',{'station_Nm_List':dictData_2})
    
    for i in range(len(dictData_2['ServiceResult']['msgBody']['itemList'])):
        No_Nm_list[station_No_List[i]] = station_Nm_List[i]

    stop=[]
    for key , value in profile.stopbookmark.items():
        stop.append(str(key))
    return render(request, 'ebuapp/bus.html',{'No_Nm_list':No_Nm_list , 'busid':busid, 'stop':stop, 'now_location':now_location,'busNm':busNm})


def book_bus(request, stationid, busid, busname):
    profile =  ProfileRegisterForm(instance = request.user)
    if busid in profile.bookkey:
        profile.pop(busid)
    else:
        profile.push(busid, busname)
    if profile.is_valid():
        user = profile.save()
    return redirect('stop', stationid) 

def book_stop(request, busid, stationid, stationname):
    profile = ProfileRegisterForm(instance = request.user)
    if stationid in profile.stopbookkey:
        profile.stoppop(stationid)
    else:
        profile.stoppush(stationid, stationname)
    if profile.is_valid():
        user = profile.save()
    print(profile.stopbookkey)
    return redirect('bus', busid)

def bookmark(request):
    profile = ProfileRegisterForm(instance = request.user)
    # bookmark_bus = []
    # for i in range(len(profile.bookmark)):
    #     bookmark_bus.append(str(profile.bookmark[i]))

    return render(request, 'ebuapp/bookmark.html', {'bookmark_bus':profile.bookmark, 'bookmark_stop':profile.stopbookmark})

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)