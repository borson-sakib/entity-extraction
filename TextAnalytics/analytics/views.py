from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from  .utils import *

from .models import *

from bs4 import BeautifulSoup
# Create your views here.


def index(request):
    if(request.method == "POST"):
        text = request.POST['texttoentity']
        text_key = request.POST['texttoentity']

        html = naturalLP(text)
        text = naturalLPlist(text)
        # keyext = keyextract(text)
        soup = BeautifulSoup(html, 'html.parser')
        # div = soup.find('div',{'class':'entities'})
        div = soup.find_all('mark')

        # for tag in soup(['mark', 'span']):
        #     tag.decompose()
        # div = soup.find('div')
        arr = []
        for p in div:
            print(p.text)
            arr.append(p.text)
            print(type(p.text))
        
        catagories = group_entities_by_type(arr)
        top_keywords = extract_keywords(text_key, top_n=5)

        print(catagories)

        # print(div)
        # print(type(div))
        # print(text)
        # print(div)
        return render(request,'base.html',{'keywords':top_keywords,'text':catagories})
    
    html = None
    text = None
    # return render(request,'base.html',{'html':html,'text':text})
    # return render(request,'base.html')
