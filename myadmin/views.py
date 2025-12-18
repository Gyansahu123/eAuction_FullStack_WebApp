from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

from . import models

from eAuction import models as eauction_models 

#
from django.core.files.storage import FileSystemStorage
from . import models

from django.conf import settings
from django.contrib import messages


# Create your views here.

#for middleware security perpose

def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/cpadmin/' or request.path=='/myadmin/epadmin/'  or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/':
            if request.session['sunm']==None or request.session['srole']!="admin":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware

def adminhome(request):
    print(request.session["sunm"])
    return render(request,"adminhome.html",{"sunm":request.session['sunm']})

def manageusers(request):
    users=eauction_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"users":users,"sunm":request.session['sunm']})

def manageuserstatus(request):
    regid=int(request.GET.get("regid"))
    s=request.GET.get("s")

    if s=="block":    
        eauction_models.Register.objects.filter(regid=regid).update(status=0)
    elif s=="verify":
        eauction_models.Register.objects.filter(regid=regid).update(status=1)
    else:
        eauction_models.Register.objects.filter(regid=regid).delete()                
    return redirect("/myadmin/manageusers/")


def cpadmin(request):
    if request.method=="GET":
        return render(request,"cpadmin.html",{"sunm":request.session['sunm']})
    else:
        #to recieve data from UI
        opass=request.POST.get("opass")
        npass=request.POST.get("npass")
        cnpass=request.POST.get("cnpass")
        sunm=request.session["sunm"]

        #to check user details
        users=eauction_models.Register.objects.filter(email=request.session["sunm"],password=opass) #
        
        if len(users)>0:
            if npass==cnpass:
                eauction_models.Register.objects.filter(email=request.session["sunm"]).update(password=cnpass)
                msg="Password updated successfully please login again...."    
            else:
                msg="New & Confirm new password mismatch , please try again...."        
        else:
            msg="Invalid old password , please try again...."                            

        return render(request,"cpadmin.html",{"sunm":request.session['sunm'],"output":msg})        

def epadmin(request):
    sunm=request.session["sunm"]
    user=eauction_models.Register.objects.filter(email=sunm)        
    m,f="",""
    if user[0].gender=="male":
        m="checked"
    else:
        f="checked"                
    
    if request.method=="GET":
        return render(request,"epadmin.html",{"m":m,"f":f,"user":user[0],"sunm":request.session['sunm']})
    else:
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        
        eauction_models.Register.objects.filter(email=sunm).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
        
        return redirect("/myadmin/epadmin/")   
    
def addcategory(request):
 if request.method=="GET":    
  return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
 else:
  catname=request.POST.get("catname")           
  caticon=request.FILES["caticon"]
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  p=models.Category(catname=catname,caticon=filename)  
  p.save()
  return render(request,"addcategory.html",{"output":"Category Added Successfully....","sunm":request.session["sunm"]})       

def addsubcategory(request):
 clist=models.Category.objects.filter()
 if request.method=="GET":    
  return render(request,"addsubcategory.html",{"output":"","clist":clist,"sunm":request.session["sunm"]})
 else:
  catname=request.POST.get("catname")
  subcatname=request.POST.get("subcatname")           
  caticon=request.FILES["caticon"]
  fs = FileSystemStorage()
  filename = fs.save(caticon.name,caticon)
  p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticon=filename)  
  p.save()
  return render(request,"addsubcategory.html",{"output":"SubCategory Added Successfully....","clist":clist,"sunm":request.session["sunm"]})