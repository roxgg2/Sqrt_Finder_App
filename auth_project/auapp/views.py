from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from math import sqrt
def uhome(request):
    if request.user.is_authenticated:
        if request.GET.get("num"):
            num = float(request.GET.get("num"))
            if num > 0.0:
                res = sqrt(num)
                res = round(res,2)
                msg = "sqrt = " + str(res)
                return render(request,"home.html",{"msg":msg})
            else:
                msg = "-ve number not allowed"
                return render(request,"home.html",{"msg":msg})
        else:
            return render(request,"home.html")
    else:
        return redirect("ulogin")
    
    
def ulogin(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    elif request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        usr = authenticate(username=un,password=pw)
        if usr is None:
            return render(request,"login.html",{"msg":"invalid login"})
        else:
            login(request,usr)
            return redirect("uhome")
    else:
        return render(request,"login.html")

def usignup(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    elif request.method == "POST":
        un = request.POST.get("un")
        pw1 = request.POST.get("pw1")
        pw2 = request.POST.get("pw2")
        if pw1 == pw2:
            try:
                usr = User.objects.get(username=un)
                return render(request,"signup.html",{"msg":"user already exists"})
            except User.DoesNotExist:
                usr = User.objects.create_user(username=un,password=pw1)
                usr.save()
                return redirect("ulogin")
        else:
            return render(request,"signup.html",{"msg":"passwords do not match"})
    else:
        return render(request,"signup.html")
      
def ulogout(request):
    logout(request)
    return redirect("ulogin")

def ucp(request):
    if not request.user.is_authenticated:
        return redirect("ulogin")
    elif request.method == "POST":
        pw1 = request.POST.get("pw1")
        pw2 = request.POST.get("pw2")
        if pw1 == pw2:
            usr = User.objects.get(username=request.user.username)
            usr.set_password(pw1)
            usr.save()
            return redirect("ulogin")
        else:
            return render(request,"cp.html",{"msg":"password did not match"})
    else:
        return render(request,"cp.html")