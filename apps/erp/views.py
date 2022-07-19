from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
#import requests  # to connect with yash backend
from django.http.response import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from .models import customUser,Events
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return(redirect('/'))
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname') 
        roll_no = request.POST.get('roll')
        year = request.POST.get('year')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        dept = request.POST.get('dept')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        error = 0
        context = {
            'error1': '',
            'error2': '',
        }

        if User.objects.filter(username=roll_no).exists():
            error = 1
            context['error1'] = 'Roll No Exists'
        if((roll_no[: 1].isdigit() == False) or (roll_no[2: 3].isalpha() == False) or (roll_no[4:].isdigit() == False)):
            print(roll_no)
            error = 1
            context['error1'] = 'Invalid Roll No'
        if (password1 != password2):
            error = 1
            context['error2'] = 'Password Did not match'

        if error == 1:
            return render(request, 'register.html', context)

        user = User.objects.create_user(username=roll_no,password=password1,first_name=fname,last_name=lname,email=mail)
        customuser = customUser(user = user,contact = contact,year = year,dept = dept)
        customuser.save()
        messages.success(request, 'Registration successfully done!!!')
        user.save()
        return redirect('/')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser == True:
                auth.login(request, user)
                return redirect('/admin')
            if user.is_staff==True:
                auth.login(request, user)
                return redirect('/teacherDash')
            else:
                userDetails = customUser.objects.get(user = user)
                if userDetails.is_accepted == False:
                    return render(request,'login.html',{'message' : 'Invalid Credential'})
                auth.login(request, user)
                return redirect('/studentDash')
        else:
            return render(request,'login.html',{'message' : 'Invalid Credentials'})
    return render(request,'login.html')


@login_required(login_url='/login')
def studentDash(request):    
    userDetails = customUser.objects.get(user = request.user)
    user = [{'roll' : request.user.username,'name' : request.user.first_name+" "+request.user.last_name, 'mail' : request.user.email, 'contact' : userDetails.contact, 'dept' : userDetails.dept, 'year' : userDetails.year}]
    
    eventDetails = []
    events = Events.objects.all()
    for j in events:
        event = {
            'event' : j.eventName,
            'desc' : j.description,
            'link' : j.link,
        }
        eventDetails.append(event)
    context = {'user' : user,'events' : eventDetails}
    return render(request, 'studentDash.html', context)

@login_required(login_url='/login')
def teacherDash(request):
    UserDetails = customUser.objects.filter(is_accepted = True)
    admitted_students = []
    for i in UserDetails:
        user= User.objects.get(username = i)
        UserDetail = {
            'roll' : user.username,
            'name' : user.first_name + " " + user.last_name,
            'contact' : i.contact,
            'mail' : user.email,
            'dept' : i.dept,
            'year' : i.year,
        }
        admitted_students.append(UserDetail)
    return render(request, 'teacher_dashboard.html', {'students': admitted_students})

def createEvent(request):
    if request.method == 'POST':
        event = request.POST.get('event')
        desc = request.POST.get('desc')
        link = request.POST.get('link')
        event = Events(eventName = event, description = desc, link = link)
        event.save()
        return redirect('/teacherDash')
    return HttpResponse("Failed to create event")

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return(redirect('/'))
