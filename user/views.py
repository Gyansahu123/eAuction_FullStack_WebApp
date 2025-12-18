# from django.shortcuts import render,redirect, get_object_or_404
from eAuction import models as eauction_models 
from . import models

from time import time
from turtle import title
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

MEDIA_URL=settings.MEDIA_URL
from django.shortcuts import render, redirect
from eAuction import models


from myadmin import models as myadmin_models
import time
from django.utils import timezone

#
from .models import Product
from .models import Product, Bid
from myadmin.models import Category, SubCategory
from .models import Funds
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from . import models
import time

from django.utils import timezone

from .models import Funds
from myadmin import models as myadmin_models
from django.core.files.storage import FileSystemStorage
from myadmin.models import Category, SubCategory

from .models import Product
from .models import Product, Bid

from . import models as user_models 



# Create your views here.

#for security perpose
def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path=='/user/' or request.path=='/user/cpuser/' or request.path=='/user/epuser/' or request.path=='/user/searchproduct/' or request.path=='/user/viewsubcategory/':
            if request.session['sunm']==None or request.session['srole']!="user":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware
            
def userhome(request):
    return render(request,"user.html",{"sunm":request.session['sunm']})

def cpuser(request):
    if request.method=="GET":
        return render(request,"cpuser.html",{"sunm":request.session['sunm']})
    else:
        #to recieve data from UI
        opass=request.POST.get("opass")
        npass=request.POST.get("npass")
        cnpass=request.POST.get("cnpass")

        #to check user details
        users=eauction_models.Register.objects.filter(email=request.session["sunm"],password=opass)
        
        if len(users)>0:
            if npass==cnpass:
                eauction_models.Register.objects.filter(email=request.session["sunm"]).update(password=cnpass)
                msg="Password updated successfully please login again...."    
            else:
                msg="New & Confirm new password mismatch , please try again...."        
        else:
            msg="Invalid old password , please try again...."                            

        return render(request,"cpuser.html",{"sunm":request.session['sunm'],"output":msg})        

def epuser(request):
    sunm=request.session["sunm"]
    user=eauction_models.Register.objects.filter(email=sunm)        
    m,f="",""
    if user[0].gender=="male":
        m="checked"
    else:
        f="checked"                
    
    if request.method=="GET":
        return render(request,"epuser.html",{"m":m,"f":f,"user":user[0],"sunm":request.session['sunm']})
    else:
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        
        eauction_models.Register.objects.filter(email=sunm).update(name=name,mobile=mobile,address=address,city=city,gender=gender)
        
        return redirect("/user/epuser/")   


# def makecharity(request):
# 	paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
# 	paypalID="sb-prgyp45067230@business.example.com"
# 	amt=100

      
# 	return render(request,"makecharity.html",{"sunm":request.session['sunm'],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})

def makecharity(request):
    paypalURL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID = "sb-prgyp45067230@business.example.com"
    
    # Default amount if nothing selected yet
    amt = request.GET.get("amt", 100)  # Allow pre-selection via query param
    
    return render(request, "makecharity.html", {
        "sunm": request.session.get('sunm'),
        "paypalURL": paypalURL,
        "paypalID": paypalID,
        "amt": amt
    })


# def payment(request):
# 	uid=request.GET.get("uid")
# 	amt=request.GET.get("amt")
# 	p=models.Funds(uid=uid,amt=int(amt),info=time.asctime())
# 	p.save()
# 	return redirect("/user/success/")

def payment(request):
    uid = request.GET.get("uid")
    amt = request.GET.get("amt")

    # Safety: Validate values
    try:
        amt = int(amt)
        if amt <= 0:
            raise ValueError("Invalid donation amount")
    except (ValueError, TypeError):
        return redirect("/user/cancel/")  # Redirect if invalid amount

    if not uid:
        return redirect("/user/cancel/")  # Redirect if no user ID

    # Save the donation
    p = models.Funds(uid=uid, amt=amt, info=time.asctime())
    p.save()

    # Show success page with details
    return render(request, "success.html", {
        "uid": uid,
        "amt": amt,
		"now": timezone.now().strftime("%d %B %Y, %H:%M:%S")
    })

# def success(request):
# 	  return render(request,"success.html",{"sunm":request.session["sunm"]})
# def cancel(request):
#     return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def success(request):
    uid = request.GET.get("uid", "")
    amt = request.GET.get("amt", "")
    return render(request, "success.html", {
        "uid": uid,
        "amt": amt
    })

def cancel(request):
    return render(request, "cancel.html")


def searchproduct(request):
    clist=myadmin_models.Category.objects.all()
    return render(request,"searchproduct.html",{"clist":clist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})

def viewsubcategory(request):
    cnm=request.GET.get("cnm")
    clist=myadmin_models.Category.objects.all()
    sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)
    return render(request,"viewsubcategory.html",{"sclist":sclist,"clist":clist,"MEDIA_URL":MEDIA_URL,"cnm":cnm,"sunm":request.session["sunm"]})

def addproduct(request):
	sclist=myadmin_models.SubCategory.objects.filter()
	if request.method=="GET":
		return render(request,"addproduct.html",{"sunm":request.session["sunm"],"output":"","sclist":sclist})
	else:
		title=request.POST.get("title")
		subcatname=request.POST.get("subcatname")
		description=request.POST.get("description")
		baseprice=request.POST.get("baseprice")
		picon=request.FILES["picon"]
		fs = FileSystemStorage()
		filename = fs.save(picon.name,picon)
		p=models.Product(title=title,subcatname=subcatname,description=description,baseprice=baseprice,picon=picon,uid=request.session["sunm"],info=time.time())
		p.save()
		return render(request,"addproduct.html",{"sunm":request.session["sunm"],"output":"Product added successfully....","sclist":sclist})

def viewproduct(request):
	cnm=request.GET.get("cnm")
	scnm=request.GET.get("scnm")
	sunm=request.session["sunm"]
	plist=models.Product.objects.filter(~Q(uid=sunm),subcatname=scnm)
	print(plist)
	return render(request,"viewproduct.html",{"plist":plist,"MEDIA_URL":MEDIA_URL,"sunm":sunm,"cnm":cnm,"scnm":scnm})

# def bid(request):
# 	sunm=request.session["sunm"]
# 	if request.method=="GET":
# 		pid=int(request.GET.get("pid"))
# 		pDetails=models.Product.objects.filter(pid=pid)
# 		dtime=time.time()-float(pDetails[0].info)
	
# 		bDetails=models.Bid.objects.filter(pid=pid)
	
# 		l=len(bDetails)
# 		if l==0:
# 			cbprice=pDetails[0].baseprice
# 		else:	
# 			cbprice=bDetails[l-1].bidprice

# 		bstatus=True
# 		if dtime>172800:
# 			bstatus=False

# 		return render(request,"bid.html",{"pDetails":pDetails[0],"MEDIA_URL":MEDIA_URL,"sunm":sunm,"bstatus":bstatus,"cbprice":cbprice})
# 	else:
# 		pid=request.POST.get("pid")
# 		bidprice=request.POST.get("bidprice")
# 		p=models.Bid(pid=int(pid),uid=sunm,bidprice=int(bidprice),info=time.asctime())
# 		p.save()
# 		return redirect("/user/bid/?pid="+pid)	

# def bidlist(request):
# 	pid=int(request.GET.get("pid"))
# 	bidlist=models.Bid.objects.filter(pid=pid)
# 	return render(request,"bidlist.html",{"bidlist":bidlist,"sunm":request.session["sunm"]})


# def viewcategories(request):
#     # Fetch categories from DB
#     categories = []  # Replace with actual query
#     return render(request, 'viewcategories.html', {'categories': categories})

# # View Subcategories
# def viewsubcategories(request):
#     # Fetch subcategories from DB
#     subcategories = []  # Replace with actual query
#     return render(request, 'viewsubcategories.html', {'subcategories': subcategories})










# View all products
def products(request):
    query = request.GET.get("q")  # search term
    sort = request.GET.get("sort")  # sorting option

    products = Product.objects.all()

    # 🔍 Search
    if query:
        products = products.filter(
            title__icontains=query
        ) | products.filter(
            categoryname__icontains=query
        ) | products.filter(
            subcatname__icontains=query
        )

    # 🔽 Sorting
    if sort == "price_low":
        products = products.order_by("baseprice")
    elif sort == "price_high":
        products = products.order_by("-baseprice")
    elif sort == "latest":
        products = products.order_by("-pid")  # newest first

    return render(request, "products.html", {"products": products, "query": query, "sort": sort})


# View product details
def product_detail(request, pid):
    product = get_object_or_404(Product, pid=pid)

    # highest bid
    highest_bid = Bid.objects.filter(product=product).order_by('-bid_amount').first()

    # recent bids (ordered by bid_time, newest first)
    bids = Bid.objects.filter(product=product).order_by('-bid_time')[:5]

    # related products
    related_products = Product.objects.filter(categoryname=product.categoryname).exclude(pid=pid)[:4]

    return render(request, "product_detail.html", {
        "product": product,
        "highest_bid": highest_bid,
        "bids": bids,
        "related_products": related_products,
    })


# Place bid
def bid_product(request, pid):
    product = get_object_or_404(Product, pid=pid)

    if request.method == "POST":
        bid_amount = request.POST.get("bid_amount")
        if not bid_amount:
            messages.error(request, "Please enter a valid bid amount.")
            return redirect("product_detail", pid=product.pid)

        bid_amount = float(bid_amount)

        # ✅ get highest bid or base price
        highest_bid = Bid.objects.filter(product=product).order_by('-bid_amount').first()
        min_bid = highest_bid.bid_amount if highest_bid else product.baseprice

        if bid_amount > min_bid:
            Bid.objects.create(
                product=product,
                bidder_id=request.session.get("snum", "guest"),   # session id
                bidder_name=request.session.get("sname", "Anonymous"),
                bidder_email=request.session.get("semail", "anonymous@example.com"),
                bid_amount=bid_amount
            )
            messages.success(request, "✅ Your bid has been placed!")
        else:
            messages.error(request, f"Bid must be higher than ₹{min_bid}")

    return redirect("product_detail", pid=product.pid)
