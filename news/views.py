from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User, New, Category, Message
from datetime import date
from django.core.paginator import Paginator



import requests

today = date.today()
categories = Category.objects.all()

response_temp = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=-32.03&lon=-60.31&appid=969c8c1c061df85848b351e72bf74e51")
geodata = response_temp.json()

response_covid = requests.get('https://api.covid19api.com/dayone/country/argentina/status/confirmed')
covid = response_covid.json()


temp = int(geodata['main']['temp'] - 273.15)
img = geodata['weather'][0]['icon']
description = geodata['weather'][0]['description']

total_covid = covid[len(covid) - 1]['Cases']

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class': "input form-control col-lg-8 col-sm-12 col-xs-12"}))

# Create your views here.
def index(request):
    if request.method == 'GET':
        news = New.objects.filter(primary=False).exclude(category=3).order_by('id').reverse()[0:5]
        last = New.objects.filter(primary=True).order_by('id').reverse()[:1]
        second = New.objects.filter(primary=True).order_by('id').reverse()[1:3]
        word = New.objects.filter(category=3).order_by('id').reverse()[0:3]

        context = {
            'page_obj': news,
            'categories': categories,
            'last': last,
            'today': today,
            'geodata': geodata,
            'temp': temp,
            'img': img,
            'description': description,
            'total_covid': total_covid,
            'second': second,
            'opinion': word,
            'form': Search()
        }

        return render(request, "news/index.html", context)
    else:
        news = New.objects.all().order_by('id').reverse()
        searched = []
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for new in news:
                if item in news:
                    page = New.objects.filter(title=item)

                    context = {
                        'news': page,
                        'today': today,
                        'form': Search()
                    }

                    return render(request, "newspaper/new.html", context)
                if item.lower() in new.title.lower():
                    searched.append(new)
            if searched == []:
                return render(request, "news/search.html", {'message': 'No match to your search', 'today': today, "form":Search()})
            return render(request, "news/search.html", {'page_obj': searched, 'today': today, "form":Search()})
        else:
            return render(request, "news/index.html", {"form": form})


def category(request, category):
    news = New.objects.filter(category=category).order_by('id').reverse()
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not news:

        context = {
            'message': "OOPS! It looks like we don't have news to this category",
            'categories': categories,
            'today': today,
            'geodata': geodata,
            'temp': temp,
            'img': img,
            'description': description,
            'form': Search()
        }

        return render(request, "news/error.html", context)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'today': today,
        'geodata': geodata,
        'temp': temp,
        'img': img,
        'description': description,
        'form': Search()
    }

    return render(request, "news/category.html", context)

def new(request, new):

    required_new = New.objects.filter(title=new)
    related_new = New.objects.all().order_by('id').reverse()[0:2]
    for new in required_new:
        related_new = New.objects.filter(category= new.category).order_by('id').reverse()[0:2]
        if new in related_new:
            related_new = New.objects.filter(category= new.category).order_by('id').reverse()[2:4]

    context = {
        'required_new': required_new,
        'today': today,
        'categories': categories,
        'geodata': geodata,
        'temp': temp,
        'img': img,
        'description': description,
        'related_new': related_new,
        'form': Search()
    }

    return render(request, "news/new.html", context)

def news(request):
    news = New.objects.all().order_by('id').reverse()
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'today': today,
        'form': Search()
    }

    return render(request, "news/news.html", context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']

        message = Message.objects.create(first_name=first_name, last_name=last_name, email=email, message=message)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/contact.html", {"today": today})
