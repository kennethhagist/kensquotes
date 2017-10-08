# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render
import re
from .models import User, Quote


def verify_session_user(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

# Create your views here.
def index(request):
    return render(request, 'quotes/index.html')

def login(request):
    errors_or_user = User.objects.validate_login(request.POST)

    if errors_or_user[0]:
        for fail in errors_or_user[0]:
            messages.error(request, fail)
        return redirect('/')
    request.session['id'] = errors_or_user[1].id
    messages.success(request, "Hello, {{ user.name }}")
    return redirect('/dashboard')

def register(request):
    errors_or_user = User.objects.validate_registration(request.POST)

    if errors_or_user[0]:
        for fail in errors_or_user[0]:
            messages.error(request, fail)
        return redirect('/')
    request.session['id'] = errors_or_user[1].id
    messages.success(request, "Hello, {{ user.name }}")
    return redirect('/dashboard')

def logout(request):
    del request.session['id']
    return redirect('/')

def dashboard(request):
    registered_users = User.objects.all()
    current_user = User.objects.get(id = request.session['id']) 
    likes = Quote.objects.filter(likes_user=current_user)
    allquotes = Quote.objects.all().order_by('-id').exclude(id__in=[l.id for l in likes])
    context = {
        "registered_users": registered_users,
        "current_user": current_user,
        "quotes": allquotes,
        "likes" : likes
    }

    return render(request, "quotes/dashboard.html", context)

def create(request):
    if request.method == "GET":
        return redirect ('/')
    if request.method == "POST":
        quote_text = request.POST['quote']
        user_id = request.session['id']
        quoted_by = request.POST['quote_author']
        print quoted_by
        result = Quote.objects.validate_quote(quote_text, user_id, quoted_by)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return redirect ('/dashboard')
        messages.error(request, result['errors'], extra_tags = "create")
        return redirect('/quotes')

def likes(request, user_id, quote_id):
    user_id = request.session['id']
    Quote.objects.likes(current_user_id, quote_id)
    return redirect('/dashboard')

def remove(request, quote_id):
    user_id = request.session['id']
    Quote.objects.remove(current_user_id, quote_id)
    return redirect('/dashboard')

def users(request, user_id):
    author = User.objects.get(id=user_id)
    context = {
        'quotes': Quote.objects.filter(author = author),
        'author': author 
    }
    return render(request, "quotes/users.html", context)

def quotes(request):
    return redirect('/dashboard')
