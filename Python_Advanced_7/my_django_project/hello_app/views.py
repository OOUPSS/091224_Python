from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    context = {
        'name': 'your_name',  # Имя, которое будет выводиться на странице
    }
    return render(request, 'hello_app/hello.html', context)
