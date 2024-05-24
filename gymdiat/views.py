import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from pymysql import connections

from gymdiat.models import *


def login1(request):
    return render(request,"loginindex.html")


def logout(request):
    auth.logout(request)
    return render(request,"loginindex.html")

def logincode(request):
    try:
        username = request.POST['textfield']
        password = request.POST['textfield2']
        ob = login.objects.get(username=username,password=password)
        if ob.type == "admin":
            request.session['lid'] = ob.id
            var = auth.authenticate(username='admin', password='admin')
            if var is not None:
                auth.login(request, var)
            return HttpResponse('''<script>alert("Welcome");window.location="/adminhome"</script>''')
        elif ob.type == "trainer":
            request.session['lid'] = ob.id
            var = auth.authenticate(username='admin', password='admin')
            if var is not None:
                auth.login(request, var)
            return HttpResponse('''<script>alert("Welcome");window.location="/trainerhome"</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid Username Or Password");window.location="/"</script>''')
    except:
        return HttpResponse('''<script>alert("Invalid Username Or Password");window.location="/"</script>''')

@login_required(login_url='/')
def adminhome(request):
    return render(request,"admin/adminindex.html")

@login_required(login_url='/')
def mngtrainer(request):
    res=trainer.objects.all()
    return render(request,"admin/mngtrainer.html",{"data":res})

@login_required(login_url='/')
def mngtrainerpost(request):
    s=request.POST['t1']
    res=trainer.objects.filter(firstname__istartswith=s)
    return render(request,"admin/mngtrainer.html",{"data":res})


@login_required(login_url='/')
def addtrainer(request):
    return render(request,"admin/addtrainer.html")

@login_required(login_url='/')
def addtrainerpost(request):
    fname=request.POST['textfield']
    lname=request.POST['textfield2']
    dob=request.POST['textfield3']
    gender=request.POST['gender']
    qualification=request.POST['textfield4']
    phone=request.POST['textfield5']
    email=request.POST['textfield6']
    username=request.POST['textfield7']
    password=request.POST['textfield8']

    ob=login()
    ob.username=username
    ob.password=password
    ob.type='trainer'
    ob.save()

    obj=trainer()
    obj.firstname=fname
    obj.lastname=lname
    obj.dob=dob
    obj.gender=gender
    obj.Qualification=qualification
    obj.Phone=phone
    obj.Email=email
    obj.LOGIN=ob
    obj.save()
    return HttpResponse('''<script>alert("Add Success");window.location="/mngtrainer#about"</script>''')

@login_required(login_url='/')
def edittrainer(request,id):
    res=trainer.objects.get(id=id)
    request.session['et']=id
    return render(request,"admin/edittrainer.html",{"data":res})


@login_required(login_url='/')
def edittrainerpost(request):
    fname=request.POST['textfield']
    lname=request.POST['textfield2']
    # dob=request.POST['textfield3']
    # gender=request.POST['radiobutton']
    qualification=request.POST['textfield4']
    phone=request.POST['textfield5']
    email=request.POST['textfield6']

    obj=trainer.objects.get(id=request.session['et'])
    obj.firstname=fname
    obj.lastname=lname
    # obj.dob=dob
    # obj.gender=gender
    obj.Qualification=qualification
    obj.Phone=phone
    obj.Email=email
    obj.save()
    return HttpResponse('''<script>alert("Edit Success");window.location="/mngtrainer#about"</script>''')

@login_required(login_url='/')
def deletetrainer(request,id):
    res=trainer.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngtrainer#about"</script>''')



@login_required(login_url='/')
def viewuser(request):
    res=user.objects.all()
    return render(request,"admin/viewuser.html",{"data":res})


@login_required(login_url='/')
def viewuserpost(request):
    s=request.POST['t1']
    res=user.objects.filter(firstname__istartswith=s)
    return render(request,"admin/viewuser.html",{"data":res})



@login_required(login_url='/')
def mngproduct(request):
    res=product.objects.all()
    return render(request,"admin/mngproduct.html",{"data":res})


@login_required(login_url='/')
def mngproductpost(request):
    s = request.POST['t1']
    res = product.objects.filter(productname__istartswith=s)
    return render(request, "admin/mngproduct.html", {"data": res})


@login_required(login_url='/')
def addproduct(request):
    return render(request,"admin/addproduct.html")


@login_required(login_url='/')
def addproductpost(request):
    pname=request.POST['textfield']
    price=request.POST['textfield3']
    stock=request.POST['textfield4']
    image=request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(image.name, image)

    ob=product()
    ob.productname=pname
    ob.price=price
    ob.stock=stock
    ob.image=fn
    ob.save()
    return HttpResponse('''<script>alert("Add Success");window.location="/mngproduct#about"</script>''')


@login_required(login_url='/')
def editproduct(request,id):
    res=product.objects.get(id=id)
    request.session['ep']=id
    return render(request,"admin/editproduct.html",{"data":res})

@login_required(login_url='/')
def editproductpost(request):
    try:
        pname=request.POST['textfield']
        price=request.POST['textfield3']
        stock=request.POST['textfield4']
        image=request.FILES['file']
        fs = FileSystemStorage()
        fn = fs.save(image.name, image)

        ob=product.objects.get(id=request.session['ep'])
        ob.productname=pname
        ob.price=price
        ob.stock=stock
        ob.image=fn
        ob.save()
        return HttpResponse('''<script>alert("Edit Success");window.location="/mngproduct#about"</script>''')
    except:
        pname = request.POST['textfield']
        price = request.POST['textfield3']
        stock = request.POST['textfield4']

        ob = product.objects.get(id=request.session['ep'])
        ob.productname = pname
        ob.price = price
        ob.stock = stock
        ob.save()
        return HttpResponse('''<script>alert("Edit Success");window.location="/mngproduct#about"</script>''')

@login_required(login_url='/')
def deleteproduct(request,id):
    res=product.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngproduct#about"</script>''')


@login_required(login_url='/')
def mngschedule(request):
    res=schedule.objects.all()
    return render(request,"admin/mngschedule.html",{"data":res})


@login_required(login_url='/')
def mngschedulepost(request):
    s=request.POST['t1']
    res=schedule.objects.filter(date__icontains=s)
    return render(request,"admin/mngschedule.html",{"data":res})



@login_required(login_url='/')
def addschedule(request):
    res=trainer.objects.all()
    return render(request,"admin/addschedule.html",{"data":res})


@login_required(login_url='/')
def addschedulepost(request):
    trainers=request.POST['select']
    slotno=request.POST['textfield2']
    fromtime=request.POST['textfield3']
    totime=request.POST['textfield4']

    ob=schedule()
    ob.slotno=slotno
    ob.fromtime=fromtime
    ob.totime=totime
    ob.TRAINER=trainer.objects.get(id=trainers)
    ob.save()
    return HttpResponse('''<script>alert("Add Success");window.location="/mngschedule#about"</script>''')



@login_required(login_url='/')
def editschedule(request,id):
    res1=trainer.objects.all()
    res=schedule.objects.get(id=id)
    request.session['es']=id
    return render(request,"admin/editschedule.html",{"data":res,'val':res1})


@login_required(login_url='/')
def editschedulepost(request):
    date=request.POST['textfield']
    slotno=request.POST['textfield2']
    fromtime=request.POST['textfield3']
    totime=request.POST['textfield4']
    trainerr=request.POST['select']

    ob=schedule.objects.get(id=request.session['es'])
    ob.date=date
    ob.slotno=slotno
    ob.fromtime=fromtime
    ob.totime=totime
    ob.TRAINER=trainer.objects.get(id=trainerr)
    ob.save()
    return HttpResponse('''<script>alert("Edit Success");window.location="/mngschedule#about"</script>''')

@login_required(login_url='/')
def deleteschedule(request,id):
    res=schedule.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngschedule#about"</script>''')


@login_required(login_url='/')
def mngfee(request):
    res=feedetails.objects.all()
    return render(request,"admin/mngfeedetails.html",{"data":res})

@login_required(login_url='/')
def addfee(request):
    res=schedule.objects.all()
    return render(request,"admin/addfeedetails.html",{"data":res})


@login_required(login_url='/')
def addfeepost(request):
    schedules=request.POST['select']
    fee=request.POST['textfield2']
    date=request.POST['textfield3']

    ob=feedetails()
    ob.SCHEDULE=schedule.objects.get(id=schedules)
    ob.date=date
    ob.amount=fee
    ob.save()
    return HttpResponse('''<script>alert("Add Success");window.location="/mngfee#about"</script>''')


@login_required(login_url='/')
def deletefee(request,id):
    res=feedetails.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngfee#about"</script>''')



@login_required(login_url='/')
def viewreport(request):
    return render(request,"admin/viewreport.html")


@login_required(login_url='/')
def vieworderandverify(request):
    res=order.objects.all()
    return render(request,"admin/vieworderandvarify.html",{"data":res})


@login_required(login_url='/')
def vieworderandverifypost(request):
    s = request.POST['t1']
    res = order.objects.filter(date__icontains=s)
    return render(request, "admin/vieworderandvarify.html", {"data": res,'date':s})


@login_required(login_url='/')
def acceptorder(request,id):
    obj=order.objects.get(id=id)
    obj.status='accept'
    obj.save()
    return HttpResponse('''<script>alert("Approved Successfully");window.location="/vieworderandverify#about"</script>''')


@login_required(login_url='/')
def rejectorder(request,id):
    obj=order.objects.get(id=id)
    obj.status='reject'
    obj.save()
    return HttpResponse('''<script>alert("Rejected Successfully");window.location="/vieworderandverify#about"</script>''')



@login_required(login_url='/')
def viewrating(request):
    res=rating.objects.all()
    return render(request,"admin/viewrating.html",{"data":res})


@login_required(login_url='/')
def viewratingpost(request):
    s=request.POST['t1']
    res=rating.objects.filter(TRAINER__firstname__istartswith=s)
    return render(request,"admin/viewrating.html",{"data":res})



@login_required(login_url='/')
def pendinglist(request):

        res=payment.objects.all()
        if len(res) == 0:
            return render(request,"admin/pendinglist.html")

            # return HttpResponse(
            #     '''<script>alert("mmmmmmm");window.location="/adminhome"</script>''')



        else:

            for i in res:


                o=booking.objects.filter(status='accept').exclude(USER__id=i.USER.id)


            return render(request,"admin/pendinglist.html",{"data":o})






#___________________TRAINER____________________________

@login_required(login_url='/')
def trainerhome(request):
    return render(request,"trainer/trainerindex.html")


@login_required(login_url='/')
def viewschedule(request):
    res=schedule.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/viewschedule.html",{"data":res})


@login_required(login_url='/')
def viewuser1(request):
    ob=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/viewuser.html",{"data":ob})


@login_required(login_url='/')
def viewuser1post(request):
    s = request.POST['t1']
    res = user.objects.filter(firstname__istartswith=s)
    return render(request, "trainer/viewuser.html", {"data": res})

@login_required(login_url='/')
def viewrating1(request):
    res=rating.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/viewrating.html",{"data":res})

@login_required(login_url='/')
def uploadeqpvedio(request):
    res=vedios.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/uploadeqpvedio.html",{"data":res})

@login_required(login_url='/')
def addeqpvedio(request):
    return render(request,"trainer/addeqpvedio.html")

@login_required(login_url='/')
def addqpvediopost(request):
    title = request.POST['textfield']
    details = request.POST['textfield3']
    vedio = request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(vedio.name, vedio)

    ob = vedios()
    ob.title = title
    ob.details = details
    ob.vedio = fn
    ob.TRAINER = trainer.objects.get(LOGIN_id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("Added Vedio");window.location="/uploadeqpvedio#about"</script>''')



@login_required(login_url='/')
def deleteqpvedio(request,id):
    res=vedios.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Vedio");window.location="/uploadeqpvedio#about"</script>''')



@login_required(login_url='/')
def mngattendance(request):
    # res1=schedule.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    res=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/mngattendance.html",{"data":res})


@login_required(login_url='/')
def presentattendance(request,id):
    ob=attendance.objects.filter(id=id,date=datetime.datetime.today())
    print(ob,"jjjjjjjjjjjjjjj")
    if len(ob) == 0:
        obj=attendance()
        obj.status='present'
        obj.BOOKING=booking.objects.get(id=id)
        obj.date=datetime.datetime.today()
        obj.save()
        return HttpResponse('''<script>alert("Present");window.location="/mngattendance#about"</script>''')
    else:
        return HttpResponse('''<script>alert("already marked");window.location="/mngattendance#about"</script>''')


@login_required(login_url='/')
def absentattendance(request,id):
    ob = attendance.objects.filter(id=id, date=datetime.datetime.today())
    print(ob, "jjjjjjjjjjjjjjj")
    if len(ob) == 0:
        obj=attendance()
        obj.status='absent'
        obj.date=datetime.datetime.today()
        obj.BOOKING=booking.objects.get(id=id)
        obj.save()
        return HttpResponse('''<script>alert("Absent");window.location="/mngattendance#about"</script>''')
    else:
        return HttpResponse('''<script>alert("already marked");window.location="/mngattendance#about"</script>''')




@login_required(login_url='/')
def mngscheduleworkout(request):
    return render(request,"trainer/mngscheduleworkout.html")

@login_required(login_url='/')
def addworkoutschedule(request):
    return render(request,"trainer/addworkoutschedule.html")

@login_required(login_url='/')
def mngdiatchart(request):
    res=diat.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/mngdiatchart.html",{"data":res})


@login_required(login_url='/')
def mngdiatchartpost(request):
    s = request.POST['t1']
    res = diat.objects.filter(USER__firstname__istartswith=s)
    return render(request, "trainer/mngdiatchart.html", {"data": res})

@login_required(login_url='/')
def adddiatchart(request):
    res=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/adddiatchart.html",{"data":res})

@login_required(login_url='/')
def adddiatchartpost(request):
    username=request.POST['select']
    description=request.POST['textfield3']
    diatplan=request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(diatplan.name, diatplan)

    ob=diat()
    ob.USER=user.objects.get(id=username)
    ob.description=description
    ob.diatchart=fn
    ob.TRAINER=trainer.objects.get(LOGIN__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("Added Success");window.location="/mngdiatchart#about"</script>''')

@login_required(login_url='/')
def deletediat(request,id):
    res=diat.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngdiatchart#about"</script>''')



@login_required(login_url='/')
def mngtutorialvedio(request):
    res=tutorialvedio.objects.filter(TRAINER__LOGIN__id=request.session['lid'])
    print(res)
    return render(request,"trainer/tutorialvedio.html",{"data":res})

@login_required(login_url='/')
def addvedio(request):
    return render(request,"trainer/addvedio.html")

@login_required(login_url='/')
def addvediopost(request):
    details = request.POST['textfield3']
    vedio = request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(vedio.name, vedio)

    ob = tutorialvedio()
    ob.details=details
    ob.vedio = fn
    ob.date=datetime.datetime.today()
    ob.TRAINER=trainer.objects.get(LOGIN_id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("Added Success");window.location="/mngtutorialvedio#about"</script>''')

@login_required(login_url='/')
def deletevedio(request,id):
    res=tutorialvedio.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert("Delete Success");window.location="/mngtutorialvedio#about"</script>''')

@login_required(login_url='/')
def verifyschedulebooking(request):
    res=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    return render(request,"trainer/verifyschedulebooking.html",{"data":res})

@login_required(login_url='/')
def acceptbooking(request,id):
    obj=booking.objects.get(id=id)
    obj.status='accept'
    obj.save()
    return HttpResponse('''<script>alert("Approved Successfully");window.location="/verifyschedulebooking#about"</script>''')

@login_required(login_url='/')
def rejectbooking(request,id):
    obj=booking.objects.get(id=id)
    obj.status='reject'
    obj.save()
    return HttpResponse('''<script>alert("Rejected Successfully");window.location="/verifyschedulebooking#about"</script>''')


@login_required(login_url='/')
def viewfoodhistory(request):
    ob=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    res = food.objects.all()
    return render(request,"trainer/viewfoodhistory.html",{"data":ob,'val':res})


@login_required(login_url='/')
def viewfoodhistorypost(request):
    test = request.POST['user']
    res = food.objects.filter(USER=test)
    ob=booking.objects.filter(SCHEDULE__TRAINER__LOGIN__id=request.session['lid'])
    return render(request, "trainer/viewfoodhistory.html", {"val": res,'data':ob,"t":int(test)})


#___________________________ANDROID_________________________________



import json

def logincode1(request):
    print(request.POST)
    un = request.POST['uname']
    pwd = request.POST['pswd']
    print(un, pwd)
    try:
        users = login.objects.get(username=un, password=pwd,type='user')
        print(users,"ooooooooooooooooooooooo")

        if users is None:
            data = {"task": "invalid"}
        else:
            print("in user function")
            data = {"task": "valid", "id": users.id,"type":users.type}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except:
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)



def registration(request):
    print(request.POST,'ppppppppppppppppppppp')
    Fname=request.POST['fname']
    Lname=request.POST['lname']
    image=request.FILES['file']
    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    gender=request.POST['gender']
    age= request.POST['age']
    place = request.POST['place']
    phone = request.POST['phone']
    email = request.POST['email']
    uname = request.POST['username']
    passwd = request.POST['password']
    lob = login()
    lob.username = uname
    lob.password = passwd
    lob.type = 'user'
    lob.save()
    userob = user()
    userob.LOGIN=lob
    userob.firstname = Fname
    userob.lastname = Lname
    userob.gender=gender
    userob.age = age
    userob.place = place
    userob.Phone = phone
    userob.Email = email
    userob.photo = fsave
    userob.save()
    data = {"task": "success"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



# def sendrating(request):
#     # review = request.POST['review']
#     ratings = request.POST['rating']
#     lid = request.POST['lid']
#     tid = request.POST['tid']
#
#
#     lob = rating()
#     lob.rating = ratings
#     lob.date = datetime.datetime.now().strftime("%Y-%m-%d")
#     lob.USER = user.objects.get(LOGIN_id=lid)
#     lob.TRAINER=trainer.objects.get(id=tid)
#     lob.save()
#
#     data = {"task": "valid"}
#     r = json.dumps(data)
#
#     print(r)
#     return HttpResponse(r)
#

def ratings(request):
    ratingss=request.POST['rating1']
    lid=request.POST['lid']
    sid=request.POST['sid']
    print(sid,"hj99999999999999h")
    lob=rating()
    lob.rating = ratingss
    lob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    lob.TRAINER=trainer.objects.get(id=sid)
    lob.USER=user.objects.get(LOGIN__id=lid)
    lob.save()
    data = {"task": "valid"}
    r = json.dumps(data)

    print(r)
    return HttpResponse(r)

def viewtrainersendrating(request):


    ob = trainer.objects.all()

    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'trainer': i.firstname, 'id': i.id}
        mdata.append(data)

    r = json.dumps(mdata)
    return HttpResponse(r)





def foodmanage(request):
    # review = request.POST['review']
    foodd = request.POST['food']
    category = request.POST['category']
    details = request.POST['details']
    lid=request.POST['lid']
    fid=request.POST['fid']

    lob = food()
    lob.foods = foodd
    lob.category = category
    lob.details = details
    lob.USER = user.objects.get(LOGIN_id=lid)
    lob.TRAINER=trainer.objects.get(id=fid)
    lob.save()

    data = {"task": "valid"}
    r = json.dumps(data)

    print(r)
    return HttpResponse(r)



def viewtrainers(request):
    id=request.POST['id']
    ob=schedule.objects.filter(TRAINER__id=id)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'trainer': i.TRAINER.firstname, 'fromtime': i.fromtime,'totime':i.totime,'id':i.id}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def viewdiatchart(request):

    tid=request.POST['tid']
    ob=diat.objects.filter(TRAINER__id=tid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'trainer': i.TRAINER.firstname, 'diatchart': i.diatchart,'description':i.description}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)


def viewacceptedtrainers(request):
    lid=request.POST['lid']
    ob=booking.objects.filter(USER__LOGIN__id=lid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'trainer': i.SCHEDULE.TRAINER.firstname, 'gender': i.SCHEDULE.TRAINER.gender,'Qualification':i.SCHEDULE.TRAINER.Qualification,'Phone':i.SCHEDULE.TRAINER.Phone,'Email':i.SCHEDULE.TRAINER.Email,'id':i.SCHEDULE.TRAINER.id}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)





def viewtrainersearch(request):


    ob = trainer.objects.all()

    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'trainer': i.firstname, 'id': i.id}
        mdata.append(data)

    r = json.dumps(mdata)
    return HttpResponse(r)


def book(request):
    # review = request.POST['review']
    scheduleid = request.POST['shid']
    lid = request.POST['lid']


    lob = booking()
    lob.SCHEDULE = schedule.objects.get(id=scheduleid)
    lob.USER = user.objects.get(LOGIN__id=lid)
    lob.date = datetime.datetime.now().strftime("%Y-%m-%d")

    lob.status='pending'
    lob.save()

    data = {"task": "valid"}
    r = json.dumps(data)

    print(r)
    return HttpResponse(r)





def vieworderhistory(request):
    lid=request.POST['lid']
    ob=orderitem.objects.filter(USER__LOGIN__id=lid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'date': str(i.ORDER.date), 'product': i.ORDER.PRODUCT.productname,'quantity':i.ORDER.quantity,'price':i.amount}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def vieweqpvedio(request):
    vid=request.POST['vid']
    ob=vedios.objects.filter(TRAINER__id=vid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'title': i.title, 'vedio': i.vedio,'details':i.details}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def viewtutorialvedio(request):
    tvid=request.POST['tvid']
    ob=tutorialvedio.objects.filter(TRAINER__id=tvid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'date': str(i.date), 'vedio': i.vedio,'details':i.details}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def viewproduct(request):

    ob=product.objects.all()

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'productname': i.productname, 'image': str(i.image),'stock':i.stock,'price':i.price,'pid':i.id}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def viewproductsearch(request):
    s = request.POST['shopname']

    ob=product.objects.filter(productname__istartswith=s)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'id':i.id,'productname': i.productname, 'image': str(i.image),'stock':i.stock,'price':i.price}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)



def feepayment(request):
    print(request.POST,"ooooooooooooo")
    lid=request.POST['lid']
    print(lid,"KKKKKKKKKKKKKKKKK")
    mdata=[]
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT *FROM `gymdiat_booking` JOIN `gymdiat_feedetails`ON `gymdiat_booking`.`SCHEDULE_id`=`gymdiat_feedetails`.`SCHEDULE_id` JOIN `gymdiat_schedule`ON `gymdiat_schedule`.`id`=`gymdiat_feedetails`.`SCHEDULE_id` JOIN `gymdiat_user` ON `gymdiat_booking`.`USER_id`=`gymdiat_user`.`id` JOIN `gymdiat_login` ON `gymdiat_login`.`id`=`gymdiat_user`.`LOGIN_id` WHERE `gymdiat_login`.`id`='" + lid + "'")
        row = cursor.fetchall()
        for i in row:
            data = {'ftime': i[11], 'totime': i[12], 'fee': i[7], 'id': i[0], 'status': i[1]}
            mdata.append(data)
            print(mdata)
        r = json.dumps(mdata)
        return HttpResponse(r)


def orders(request):
    print(request.POST, "=================================")
    pro_id = request.POST['pid']
    qty = request.POST['quantity']
    lid = request.POST['lid']
    # off = request.POST['offer']
    print(pro_id, "PPPPPPPPPPPPPPPPPPPPPPP")
    print(qty, "qqqqqqqqqqqqqqqqqqqqqqq")
    print(lid, "lllllllllllllllllllllllll")

    ob = product.objects.get(id=pro_id)
    tt = int(ob.price) * int(qty)
    stock = ob.stock
    print(stock, "SSSSSSSSSSSSSSSSSSSSSSSSS")
    nstk = int(stock) - int(qty)
    print(nstk, "OOOOOOOOOOOOOOOOOOOO")
    if stock >= qty:
        up = product.objects.get(id=pro_id)
        up.stock = nstk
        up.save()

        ob = order()
        ob.PRODUCT = product.objects.get(id=pro_id)
        ob.status = 'order'
        ob.date = datetime.datetime.now()
        ob.quantity = qty
        # ob.total = tt
        ob.save()

        obj = orderitem()
        obj.ORDER = ob
        obj.USER = user.objects.get(LOGIN__id=lid)
        obj.amount = tt
        # obj.quantity = qty
        obj.status = 'order'

        obj.save()
        id = ob.id
        data = {"task": "valid", "oid": id}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)


    else:
        data = {"task": "out of stock"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)


def payment_sucess(request):
    amount=request.POST['amt']
    lid=request.POST['lid']
    bid=request.POST['bid']
    # print(complaint,"gbhnjkhbjn")
    lob=payment()
    lob.USER = user.objects.get(LOGIN__id=lid)
    lob.amount=amount
    lob.status='paid'
    lob.BOOKING=booking.objects.get(id=bid)
    lob.save()
    data = {"task": "success"}
    r = json.dumps(data)

    print(r)
    return HttpResponse(r)