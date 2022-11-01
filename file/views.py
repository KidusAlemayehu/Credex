from django.shortcuts import render
from .models import File
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
def upload_file(request):  # sourcery skip: last-if-guard
    if not request.POST or 'file' not in request.FILES:
        return render(request, 'dashboard.html')
    file = request.FILES['file']
    name = file.name
    content_type = file.content_type
    usr = request.user
    print(usr)
    if not file:
        messages.error(request, 'File not found')
        return redirect('dashboard')
    print(name)
    print(content_type)
    file = File(name=name, content_type=content_type, file=file, usr=usr)
    file.save()
    messages.success(request,'File uploaded successfully')
    return redirect('dashboard')