from django.shortcuts import render
from django.http import FileResponse
from .models import File
from django.contrib import messages
from django.shortcuts import redirect
from .compression import compress_file, decompress_file

# Create your views here.
def upload_file(request):  # sourcery skip: last-if-guard
    if not request.POST or 'file' not in request.FILES:
        return render(request, 'dashboard.html')
    file = request.FILES['file']
    name = file.name
    content_type = file.content_type
    usr = request.user
    # print(usr)
    if not file:
        messages.error(request, 'File not found')
        return redirect('dashboard')
    file = File(name=name, content_type=content_type, file=file, usr=usr)
    file.save()
    print(file.name)
    print(file.file.path)
    # compress_file(file.file.path)
    # print(file.file)
    # file.save()
    print(f"hello {file.file}")
    messages.success(request,'File uploaded successfully')
    return redirect('dashboard')

def open(request, id):
    file = File.objects.get(pk=id)
    # obj = decompress_file(file.file.path, file.name)
    print(file.file)
    # f = open(file.file.path,"rb")
    return FileResponse(file.file, content_type=file.content_type)