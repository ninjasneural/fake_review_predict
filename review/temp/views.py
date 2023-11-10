from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'temp/Home.html')

def user(request):
    return render(request,'temp/user.html')