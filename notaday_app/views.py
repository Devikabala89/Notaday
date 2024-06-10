from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from notaday_app.models import products,cart,Order,Todo,Notes,contactus,Calorietracker,Order_history    #import your models here
from itertools import chain
import random #here used in order id
import datetime
import razorpay
from django.core.mail import send_mail
# Create your views here.

#renders intro.html page in path intro/
def intro(request):
    return render(request,'intro\intro.html')

def about(request):
    template = "intro\pageabout.html"
    return render(request,template)

def contact(request):
    try:
        if request.method=="POST":
            n=request.POST['qname']
            m=request.POST['qmail']
            p=request.POST['qphone']
            txt=request.POST['utext']
            context={}
            if n =='' or m =='' or p == '' or txt =='':
                context['data']="Fields cannot be empty"
                return render(request,'intro\contact.html',context)
            else:
                c=contactus.objects.create(name=n,email=m,phone=p,msg=txt)
                c.save()
                
                context['data']="We received your message! We'll get back to you shortly!!!"
                return render(request,'intro\contact.html',context)
        else:
            return render(request,'intro\contact.html')
    except Exception:
            return redirect('/wentwrong')

def user_login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=='' or upass=='':
            context['data']="Fields cannot be empty"
            return render(request,'intro\login.html',context)
        else:
            try:
                u=authenticate(username=uname,password=upass)
                if u is not None:
                    login(request,u)   #inbuilt login function to manage sessions
                    return redirect('/index')
                else:
                    context['data']="Invalid User"
                    return render(request,'intro\login.html',context)
            except Exception:
                context['data']="User not found! Please register"
                return render(request,'intro\login.html',context)

    else:
        return render(request,'intro\login.html')

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        #check all three fields filled or not
        if uname=="" or upass=="" or ucpass=="":
            context['data']="Fields cannot be empty!"
        elif upass != ucpass:
            context['data']="User password and confirm password not matching!!!"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)   #encrypt password and store in DB
                u.save()
                context['data']="User registered successfully! Please go ahead and login"
            except Exception:
                context['data']="User already registered, Use a different ID"
        return render(request,'intro\pageregister.html',context)
    else:
        return render(request,'intro\pageregister.html')

def features(request):
    return render(request,'intro\pagefeatures.html')

def index(request):
    userid=request.user.id
    uname=request.user.username   #get user name from user table and save it in uname variable
    t=Todo.objects.filter(uid=userid)
    context={}
    context['user']=uname
    context['data']=t
    return render(request,'app_pages\index.html',context)

def addtask(request):
    try:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        task=request.GET.get("inputtask")
        date=request.GET.get("inputdate") #it's in string format
        date=datetime.datetime.strptime(date,'%m/%d/%Y') #from datetime module used strptime to convert string data to date time format
        formatDate = date.strftime("%Y-%m-%d") #once date time  converted, to change the format we used strftime bcoz YYYY-MM-DD format only accepted in db
        imp=request.GET.get("imp")
        print(task,date,imp)
        t=Todo.objects.create(uid=u[0],task=task,date=formatDate,status="Incomplete",importance=imp)
        t.save()
        return redirect('/index')
    except Exception:
        return redirect('/wentwrong')
    

def taskcomplete(request,tid):
    t=Todo.objects.get(id=tid)
    t.status="completed"
    t.save()
    return redirect('/index')

def deletetask(request,tid):
    t=Todo.objects.filter(id=tid)
    t.delete()
    return redirect('/index')

def shop(request):
    
        context={}
        p=products.objects.filter(is_active=True)
        context['products']=p
        filcat=p.values('category').distinct()
        context['filcat']=filcat
        c1=Q(is_active=True)

        cat=request.GET.getlist("options")   #gets the checked checkboxes submited after clicking ok
        pri=request.GET.get("pricerange")
        sort_opt=request.GET.getlist("sortprice")
        context['pri']=pri
        
        print(filcat)
        if len(cat) !=0 or len(sort_opt)!= 0 or pri == 'None':
            if len(sort_opt) == 0:
                sort_opt.append('1')
            if pri == 'None':
                price = 1500
            else:
                price=int(pri or 0)
            
            if len(cat) == 0:
                for x in filcat:
                    print(x)
                    cat.append(x['category'])
            print(cat)

            c2=Q(category__in=cat)
            c3=Q(price__lte=price)
            print(c2)
            if sort_opt[0] == '1':
                c=products.objects.filter(c1&c2&c3).order_by('price')
                context['products']=c
                print(context['products'])
                context['filcat']=c.values('category').distinct()
                context['option1']="Checked"
            else:
                c=products.objects.filter(c1&c2&c3).order_by('-price')
                context['products']=c
                context['filcat']=c.values('category').distinct()
                context['option2']="Checked"
            
            context['checked']="Checked"
            
            return render(request,'app_pages\merchandise.html',context)
        else:
            return render(request,'app_pages\merchandise.html',context)
    

    #return render(request,'app_pages\merchandise.html',context)


def details_product(request,pid):
    p=products.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'app_pages\details_products.html',context)

def addtocart(request,sid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=products.objects.filter(id=sid)
        context={}
        #to avoid duplicate entry i.e., same user adds same items again we do below steps. Quantity is taken care in views cart page
        c1=Q(uid=u[0])
        c2=Q(pid=p[0])
        quan=cart.objects.filter(c1 & c2)
        n=len(quan) #if length is 1 which means product already exixts. if len is zero then proceed to add to cart
        if n==1:
            context['msg']="Product already exists in your cart!"
        else:
            c=cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['msg']="Product added to cart!"
        context['products']=p
        return render(request,'app_pages\details_products.html',context)
    else:
        return redirect('/login')

def removefromcart(request,rid):
    c=cart.objects.filter(id=rid)
    c.delete()
    return redirect('/cart')

def Cart(request):
    context={}
    c=cart.objects.filter(uid=request.user.id) #gives items in cart of particular user
    context['data']=c
    s=0
    for x in c:
        s = s + (x.pid.price*x.qty)
    context['total']=s
    context['no_items']=len(c)
    return render(request,'app_pages\cart.html',context)

def updateqty(request,wid,cid):
    c=cart.objects.filter(id=cid)
    current_qty=c[0].qty
    if wid == '0':
        if current_qty == 1:
            pass
        else:
            current_qty =current_qty - 1
    else:
        current_qty += 1
    u=cart.objects.get(id=cid)
    u.qty=current_qty
    u.save()
    return redirect('/cart')

def removefromorder(request,rid):
    c=Order.objects.filter(id=rid)
    c.delete()
    return redirect('/placeorder')

def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    #to display orders in order page below steps followed
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s = s + (x.pid.price*x.qty)
    context['total']=s
    context['no_items']=len(orders)
    return render(request,'app_pages\placeorder.html',context)

def makepayment(request):
    userid=request.user.id
    orders=Order.objects.filter(uid=userid)
    s=0
    for x in orders:
        s = s + (x.pid.price*x.qty)
        oid=x.order_id
    np=len(orders)
    client = razorpay.Client(auth=("razorpay secret key", "secret password"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'app_pages\pay.html',context)

def orderhistory(request):
    context={}
    c=Order_history.objects.filter(uid=request.user.id)
    context['data']=c
    context['text']="Order History"
    return render(request,'app_pages\orderhistory.html',context)

def calorie(request):
    if request.method=="POST":
        date=request.POST['date']
        date=datetime.datetime.strptime(date,'%m/%d/%Y') #from datetime module used strptime to convert string data to date time format
        formatDate = date.strftime("%Y-%m-%d")
        uid=request.user.id
        u=User.objects.filter(id=uid)
        cat=request.POST['cat']
        aim=request.POST['goal']
        food=request.POST['food']
        cal=request.POST['cal']
        o=Calorietracker.objects.create(uid=u[0],date=formatDate,cat=cat,aim=aim,food=food,intake=cal)
        o.save()
        context={}
        d=Calorietracker.objects.filter(uid=u[0])
        date=d.values('date').distinct()
        print(date)
        context['date']=date

        return render(request,'app_pages\calorie_tracker.html',context)
    else:
        uid=request.user.id
        u=User.objects.filter(id=uid)
        d=Calorietracker.objects.filter(uid=u[0])
        context={}
        context['data']=d
        date=d.values('date').distinct()
        print(date)
        context['date']=date
        return render(request,'app_pages\calorie_tracker.html',context)

def loadfood(request,pid):
    if request.method=="POST":
        date=request.POST['date']
        date=datetime.datetime.strptime(date,'%m/%d/%Y') #from datetime module used strptime to convert string data to date time format
        formatDate = date.strftime("%Y-%m-%d")
        uid=request.user.id
        u=User.objects.filter(id=uid)
        cat=request.POST['cat']
        aim=request.POST['goal']
        food=request.POST['food']
        cal=request.POST['cal']
        o=Calorietracker.objects.create(uid=u[0],date=formatDate,cat=cat,aim=aim,food=food,intake=cal)
        o.save()
        context={}
        d=Calorietracker.objects.filter(uid=u[0])
        date=d.values('date').distinct()
        print(date)
        context['date']=date

        return render(request,'app_pages\calorie_tracker.html',context)
    else:
        temp=pid.split(' ')
        #print(temp)
        #print((temp[0])[0:3])
        #print(temp[1])
        #print(temp[2])
        finaldate=(temp[0])[0:3]+" "+temp[1]+" "+temp[2]
        #print(finaldate)
        date=datetime.datetime.strptime(finaldate,'%b %d, %Y')
        formatDate=date.strftime("%Y-%m-%d")
        c1=Q(date=formatDate)
        c2=Q(uid=request.user.id)
        d=Calorietracker.objects.filter(c1 & c2)
        
        print(d)
        totalintake=0
        for x in d:
            totalintake = totalintake + x.intake
        aim=d[0].aim
        percent=int( (totalintake*100)/aim)
        
        context={}
        context['food']=d
        context['aim']=aim
        context['now']=totalintake
        context['percent']=percent
        #to display all dates in select options again filter by date and pass it
        f=Calorietracker.objects.filter(c2)
        context['on_load'] = pid   
        context['data']=f
        date=f.values('date').distinct()
        context['date']=date
        return render(request,'app_pages\calorie_tracker.html',context)



def notes(request):
    uid=request.user.id
    n=Notes.objects.filter(uid=uid)
    context={}
    context['notes']=n
    context['vieworadd']=False   #add new notes button
    return render(request,'app_pages\yournotes.html',context)

def addnotes(request):
    userid=request.user.id
    u=User.objects.filter(id=userid)
    title=request.GET.get("Title")
    note=request.GET.get("notes") 
    if title == "":
        pass
    else:
        t=Notes.objects.create(uid=u[0],title=title,note=note)
        t.save()
    return redirect('/notes')

def viewnotes(request,nid):
    uid=request.user.id
    n=Notes.objects.filter(uid=uid)
    context={}
    context['notes']=n
    t=Notes.objects.filter(id=nid)
    context['select']=t
    context['vieworadd']=True   #update notes button
    return render(request,'app_pages\yournotes.html',context)

def updatenotes(request,nid):
    t=Notes.objects.get(id=nid)
    updatetitle=request.GET.get("Title")
    updatenote=request.GET.get("notes") 
    #print(updatenote)
    #print(updatetitle)
    t.title=updatetitle
    t.note=updatenote
    t.save()
    return redirect('/notes')

def deletenote(request,tid):
    t=Notes.objects.filter(id=tid)
    t.delete()
    return redirect('/notes')

def sendusermail(request):
    c1=Q(uid=request.user.id)
    
    o=Order.objects.filter(c1)
    
    context={}
    context['text']="Your order has been placed successfully!!!"
    print(o)
    for x in o:
        n=Order_history.objects.create(uid=x.uid,pid=x.pid,order_id=x.order_id,qty=x.qty)
        n.save()
    c=Order_history.objects.filter(uid=request.user.id)
    context['data']=c
    o.delete()
    '''
    send_mail(
    "Notaday-Order Placed Successfully!",
    "Order Placed. Shop with us again!",
    "devikabala8997@gmail.com",
    ["devikabalartv@gmail.com"],
    fail_silently=False,
    )''' #commented out due to smtp not supported by server
    return render(request,'app_pages\orderplaced.html',context)

#logout function
def ulogout(request):
    logout(request)   #logout is django inbuilt function
    return redirect('/intro')

def wentwrong(request):
    return render(request,'app_pages\wrong.html')
