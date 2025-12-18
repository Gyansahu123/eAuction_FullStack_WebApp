# from django.http import HttpResponse
# from django.shortcuts import render,redirect

# from . import models 
# import time

# def home(request):
#     return render(request,"home.html")

# def about(request):
#     return render(request,"about.html")

# def contact(request):
#     return render(request,"contact.html")

# def service(request):
#     return render(request,"service.html")

# def register(request):
#     if request.method=="GET":    
#         return render(request,"register.html")
#     else:
        
#         name=request.POST.get("name")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         mobile=request.POST.get("mobile")
#         address=request.POST.get("address")
#         city=request.POST.get("city")
#         gender=request.POST.get("gender")

#         p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())

#         p.save()

#         return render(request,"register.html",{"output":"User register successfylly...."})         

# def login(request):
#     if request.method=="GET":
#         return render(request,"login.html")
#     else:
#         #recieve data for login
#         email=request.POST.get("email")
#         password=request.POST.get("password")

#         user=models.Register.objects.filter(email=email,password=password,status=1)
#         #print(user) 

#         if len(user)>0:

#             #to store user details in session
#             request.session['sunm']=user[0].email
#             request.session['srole']=user[0].role                                                    

#             if user[0].role=="admin":
#                 return redirect("/myadmin/")
#             else:    
#                 return redirect("/user/")    
#         else:
#             return render(request,"login.html",{"output":"Invalid user or verify your account...."})        

                
from django.http import HttpResponse
from django.shortcuts import render,redirect

from . import models 
import time
from . import emailAPI

#for security check
def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
            request.session['sunm']=None
            request.session['srole']=None
            response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":    
        return render(request,"register.html")
    else:
        #recieve data from UI
        #print(request.POST)
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        info=time.asctime()

        p=models.Register(name=name,email=email,password=password,mobile=mobile,address=address,city=city,gender=gender,status=0,role="user",info=info)

        p.save()

        #to send email
        emailAPI.sendMail(email,password)

        return render(request,"register.html",{"output":"User register successfylly...."})         


def verify(request):
    email=request.GET.get("vemail")
    models.Register.objects.filter(email=email).update(status=1)
    return redirect("/login/")


def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        #recieve data for login
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=models.Register.objects.filter(email=email,password=password,status=1)
        print(user) 

        if len(user)>0:

            #to store user details in session
            request.session['sunm']=user[0].email
            request.session['srole']=user[0].role                                                    

            if user[0].role=="admin":
                return redirect("/myadmin/")
            else:    
                return redirect("/user/")    
        else:
            return render(request,"login.html",{"output":"Invalid user or verify your account...."})        

                

         

  
    