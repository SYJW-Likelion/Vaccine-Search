from django.shortcuts import render
from home.api import *
from .models import Blog

# Create your views here.
# def home(request):
#     return render(request, 'home.html')


def home(request):
    return render(request, 'index.html')

# def vaccine(request):
#     res=get_ill_list()
#     hospitals=res.get('강북삼성병원')
#     context={'hospitals':hospitals}
#     return render(request, 'vaccine_api.html', context)

# # 블로그에서 가져온 식
# def index(request):
#     res = check_air()
#     pm10 = res.get('다사읍')
#     context = {'station': '다사읍', 'pm10': pm10}
#     return render(request, 'dust_checker/dust_main.html', context)

# def index(request):
#     res=search_hospital_list()
#     hospitals=res.get()
#     context={'hospitals':hospitals}
#     return render(request, ''))

def list(request):
    blogs=Blog.objects.all()
    return render(request, 'list.html', {'blogs':blogs})

