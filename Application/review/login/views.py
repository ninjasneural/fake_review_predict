from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.models import Login
# Create your views here.
def login(request):
    if request.method == "POST":
        uname = request.POST.get("user")
        passw = request.POST.get("pass")
        print(uname)
        print(passw)
        obj = Login.objects.filter(username=uname, password=passw)
        print(len(obj))
        tp= ""
        for ob in obj:
            tp = ob.type
            uid = ob.u_id
            if tp == "admin":
                request.session["u_id"] = uid
                return HttpResponseRedirect('/temp/admin/')
            elif tp == "user":
                request.session["u_id"] = uid
                return HttpResponseRedirect('/reviewpost/review/')
        else:
            objlist = "username or password incorrect.... please try again....!"
            context ={
                'msg':objlist,
            }
            return render(request,'login/login.html',context)
    return render(request,'login/login.html')