import re
from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
import requests
import pandas as pd
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    return render(request, "home.html")

def login_user(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST['password']
        user = authenticate(username=uname, password=password)
        if user:
            login(request, user)
            messages.success(request, 'User logged in Successfull')
            return redirect('home')
        else:
            messages.success(request, 'Invalid credentials.')
            return redirect('home')
    return render(request, 'login.html')

def signup_user(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        user = User.objects.create_user(username=uname, password=password, first_name=fname, last_name=lname, email=email)
        register = Registration.objects.create(user=user,  mobile=mobile, address=address)
        messages.success(request, 'Registration Successfull')
        return redirect('login_user')
    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def scrapping(request):
    myalldata = None
    if request.method == "POST":
        url = request.POST['url']
        li = []
        mainli = []
        file11 = open('traffick.txt', 'r')
        comparing_terms = file11.readlines()
        for i in comparing_terms:
            mainli.append(i[:-1]) #removing \n
        dict1 = {'myli':mainli}
        allwords = AllWord.objects.get(id=2)
        
        response = requests.get(url)
        htmlcontent = response.content

        soup = BeautifulSoup(htmlcontent, 'html.parser')
        allobj = TotalMatchWord.objects.filter(user=request.user)
        for j in allobj:
            j.delete()
        print(soup.strings)
        for string in soup.strings:
            for i in eval(allwords.all_word)['myli']:
                if i in string:
                    author, created = TotalMatchWord.objects.get_or_create(user=request.user,words=i)
                    if not created:
                        author.count= int(author.count)+1
                        author.save()
        
        myalldata = TotalMatchWord.objects.filter(user=request.user)
        hisdict = {}
        total_wrd = 0
        for i in myalldata:
            hisdict[i.words] = i.count
            total_wrd += int(i.count)
        myhist = History.objects.create(user=request.user, alldetail=hisdict, your_url=url, total_uword=myalldata.count(), total_word=total_wrd)
    return render(request, 'scrapping.html', {'data':myalldata})


def upload_more_words(request):
    all_word = AllWord.objects.get(id=2)
    if request.method == "POST":
        word = request.POST['word']
        li = word.split(',')
        mydict = eval(all_word.all_word)
        mydict['myli'] = mydict['myli'] + li
        all_word.all_word = mydict
        all_word.save()
        messages.success(request, "Added Successfully")
    return render(request, 'upload_more_words.html')

def showallword(request):
    all_word = AllWord.objects.get(id=2)
    d = {'all_word':eval(all_word.all_word)}
    print(all_word.all_word)
    return render(request, 'showallword.html', d)

def deletehistory(request, pid):
    hist = History.objects.get(id=pid)
    hist.delete()
    messages.success(request, "Deleted")
    return redirect('allhistory')



def showhistory(request):
    history = History.objects.all()
    pagedata = request.GET.get('pagedata', 10)
    paginator = Paginator(history, int(pagedata)) # Show 5 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    d = {'history':history, 'page_obj': page_obj}
    return render(request, 'showhistory.html', d)

def showhistoryuser(request):
    history = History.objects.filter(user=request.user)
    pagedata = request.GET.get('pagedata', 10)
    paginator = Paginator(history, int(pagedata)) # Show 5 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    d = {'history':history, 'page_obj': page_obj}
    return render(request, 'showhistoryuser.html', d)

def change_password(request):
    if request.method == "POST":
        old = request.POST.get('pass-old')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:
            u = authenticate(username=request.user.username, password=old)
            if u:
                pass
            else:
            # u = User.objects.get(username__exact=request.user.username, password=old)
                messages.success(request, 'Wrong old Password')
                return redirect('change_password')
            u.set_password(pass2)
            u.save()
            messages.success(request, 'Password changed successfully')
            return redirect('home')
        else:
            messages.success(request, 'Both password are not matching')
    return render(request, 'settings.html')

def editword(request):
    all = AllWord.objects.get(id=2)
    if request.method == "POST":
        data = request.POST['data']
        try:
            eval(data)
            all.all_word = data
            all.save()
            messages.success(request, 'Updated successfully')
            return redirect('editword')
        except:
            messages.success(request, "Please Maintain format.")
    return render(request, 'edit_word.html', {'all':all})

