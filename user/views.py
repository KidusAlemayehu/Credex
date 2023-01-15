from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import random
from file.models import File
from file.compression import compress_file, decompress_file


otp = 0
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
                global otp
                otp = random.randrange(10000000, 99999999)
                pwd = make_password(password)
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=pwd)
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
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    username = request.session['username']
    if request.POST:
        otp_code = request.POST.get('otp')
        # otp_code = request.session['otp_code']
        if int(otp) == int(otp_code):
            user = User.objects.get(username=username)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            username = request.user.username
            user = User.objects.get(username=username)
            Session.objects.all().delete()
            return redirect('dashboard')
        else:
            user = User.objects.get(username=username).delete()
            messages.error(request, 'Invalid OTP code')
            return redirect('signup')
    else:
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
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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

@login_required
def dashboard(request):
    try:
        if request.session.keys() == []:
            redirect('signin')
        username = request.user.id
        print(username)
        files = File.objects.filter(usr=username)
        for file in files:
            # decompress_file(file.file.path, file.name)
            print(file.name)
            print(file.content_type)
            print(file.file)
            print(file.created_date)
            print("___________________")
        #  compress_file(file.file.path)
        return render(request, 'dashboard.html', {'username':username, 'files':files})
    except Exception as e:
        return e
    