from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import random

# Create your views here.
def register(request):
    if request.POST:
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email is already registered.')
                return redirect('signin')
            else:
                otp = random.randrange(10000000, 99999999)
                pwd = make_password(password)
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=pwd)
                request.session['otp_code'] = otp
                request.session['username']=username
                print(otp)
                user.save(force_insert=False)
                data = {'email_subject': 'Verify your account',
                        'email_body': f'Hi {user.username} this is your verification OTP number \n {otp}',
                        'to': [user.email,]}
                email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=data['to'])
                email.send()
                messages.success(request,'you have been registered successfully.')
                return redirect('verify')
        else:
            messages.error(request,"Sorry, Password Don't match")
            return redirect('signup')
    if not request.POST:
        return render(request, 'signup.html')

def verification(request):
    username = request.session['username']
    if request.POST:
        otp = request.POST.get('otp')
        otp_code = request.session['otp_code']
        if int(otp) == int(otp_code):
            user = User.objects.get(username=username)
            Session.objects.all().delete()
            auth.login(request, user)
            username = request.user.username
            # user = User.objects.get(username=username)
            print(username)
            return redirect('dashboard')
        else:
            user = User.objects.get(username=username).delete()
            messages.error(request, 'Invalid OTP code')
            return redirect('signup')
    else:
        otp = request.session['otp_code']
        print(type(otp))
        print(username)
        return render(request, 'verify.html')

@csrf_exempt
def login(request):
    # sourcery skip: last-if-guard, merge-else-if-into-elif, swap-if-else-branches
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user=User.objects.get(username=username)
        if user is not None:
            if check_password(password=password, encoded=make_password(password), setter=None):
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Sorry, your password isn\'t correct')
                return redirect('signin')
        else:
            messages.error(request,'Username doesn\'t exist. Please try again.')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

def logout(request):
    username = request.user.username
    user = User.objects.get(username=username)
    auth.logout(request)
    request.session.clear()
    return redirect('signin')
def dashboard(request):
    if request.session.keys() == []:
        redirect('signin')
    print(request.session.keys())
    username = request.user.username
    print(username)
    return render(request, 'dashboard.html', {'username':username})