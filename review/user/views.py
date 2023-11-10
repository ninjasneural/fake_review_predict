from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.models import Login
from user.models import User
from django.db.models import Q
# Create your views here.
def user(request):
    vv=''
    if request.method=='POST':
        name=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('pass')
        copass=request.POST.get('copass')
        if password!=copass:
            return HttpResponseRedirect('/user/user/')
        print(name)
        print(phone)
        obk = User.objects.filter(Q(username=name)| Q(contact=phone) |Q(username=name)& Q(contact=phone))
        if len(obk)>0:
            vv='fa'
            context={
                'kk':vv
            }
            return render(request,'user/Register.html',context)
        else:
            obb=User()
            obb.username=request.POST.get('user')
            obb.profile = 'default.png'
            obb.contact = phone
            obb.email = request.POST.get('email')
            obb.save()
            print(obb.user_id)
            obj=Login()
            obj.username=obb.email
            obj.password=request.POST.get('pass')
            obj.u_id=obb.user_id
            obj.type="user"
            obj.save()
            vv='ss'
            context={
                'kk':vv
            }
            return HttpResponseRedirect('/reviewpost/review/')
    return render(request,'user/Register.html')