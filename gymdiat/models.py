from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)


class trainer(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=90)
    lastname=models.CharField(max_length=90)
    dob=models.CharField(max_length=90)
    gender=models.CharField(max_length=90)
    Qualification=models.CharField(max_length=90)
    Phone=models.BigIntegerField()
    Email=models.CharField(max_length=90)


class schedule(models.Model):
    TRAINER=models.ForeignKey(trainer,on_delete=models.CASCADE)
    slotno=models.CharField(max_length=90)
    fromtime=models.CharField(max_length=90)
    totime=models.CharField(max_length=90)


class user(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=90)
    lastname=models.CharField(max_length=90)
    gender=models.CharField(max_length=90)
    place=models.CharField(max_length=90)
    Phone=models.BigIntegerField()
    Email=models.CharField(max_length=90)
    age=models.CharField(max_length=90)
    photo=models.FileField()


class rating(models.Model):
    USER=models.ForeignKey(user,on_delete=models.CASCADE)
    TRAINER=models.ForeignKey(trainer,on_delete=models.CASCADE)
    date=models.DateField()
    rating=models.FloatField()


class feedetails(models.Model):
    SCHEDULE=models.ForeignKey(schedule,on_delete=models.CASCADE)
    date=models.DateField()
    amount=models.IntegerField()


class diat(models.Model):
    USER=models.ForeignKey(user,on_delete=models.CASCADE)
    TRAINER=models.ForeignKey(trainer,on_delete=models.CASCADE)
    diatchart=models.CharField(max_length=100)
    description=models.CharField(max_length=100)



class product(models.Model):
    productname=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    stock=models.CharField(max_length=100)
    price=models.IntegerField()


class vedios(models.Model):
    TRAINER = models.ForeignKey(trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    vedio = models.CharField(max_length=100)
    details = models.CharField(max_length=100)


class food(models.Model):
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    TRAINER = models.ForeignKey(trainer, on_delete=models.CASCADE)
    foods = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    details = models.CharField(max_length=100)



class tutorialvedio(models.Model):
    TRAINER=models.ForeignKey(trainer,on_delete=models.CASCADE)
    date = models.DateField()
    vedio = models.CharField(max_length=100)
    details = models.CharField(max_length=100)


class workout(models.Model):
    SCHEDULE=models.ForeignKey(schedule,on_delete=models.CASCADE)
    TRAINER=models.ForeignKey(trainer,on_delete=models.CASCADE)
    time=models.TimeField()
    work=models.CharField(max_length=100)


class order(models.Model):
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date=models.DateField()


class orderitem(models.Model):
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    ORDER = models.ForeignKey(order, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    amount = models.IntegerField()



class booking(models.Model):
    SCHEDULE = models.ForeignKey(schedule, on_delete=models.CASCADE)
    USER = models.ForeignKey(user, on_delete=models.CASCADE)
    status=models.CharField(max_length=100)
    date=models.DateField()



class payment(models.Model):
    BOOKING=models.ForeignKey(booking,on_delete=models.CASCADE)
    USER=models.ForeignKey(user,on_delete=models.CASCADE)
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)


class attendance(models.Model):
    BOOKING = models.ForeignKey(booking, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100)
