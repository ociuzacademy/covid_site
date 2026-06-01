from django.db import models

# Create your models here.
class tbl_register(models.Model):
    name=models.CharField(max_length=100,default='')
    email=models.EmailField(max_length=100,default='')
    pswd=models.CharField(max_length=100,default='')
    phn=models.CharField(max_length=100,default='')
    uname=models.CharField(max_length=100,default='')
    adrs=models.CharField(max_length=100,default='')
    plc=models.CharField(max_length=100,default='')
    utype=models.CharField(max_length=100,default='')
    age=models.CharField(max_length=100,default='')
    gender=models.CharField(max_length=100,default='')
    status=models.CharField(max_length=100,default='active')
    # age = models.CharField(max_length=100,default='')
    bldgrp=models.CharField(max_length=100, default='')
    weight =models.CharField(max_length=100,default='')    
    height=models.CharField(max_length=100,default='')   
    
class tbl_coviddetails(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    doxray= models.DateField()
    effected=models.CharField(max_length=100,default='')
    symptoms=models.CharField(max_length=100,default='')
    xray_image = models.ImageField(upload_to='xray_image/', blank=True, null=True)
    covid_result = models.CharField(max_length=100,default='')
    prediction_date = models.DateField(auto_now_add=True)
    

    
class tbl_doctors(models.Model):
    hospital = models.ForeignKey(tbl_register, on_delete=models.CASCADE, blank=True, null=True)
    doc_name=models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,default='')
    phn= models.CharField(max_length=100,default='')
    qualification=models.CharField(max_length=100,default='')
    time = models.CharField(max_length=100,default='')
    designation= models.CharField(max_length=100,default='')
    availability = models.CharField(max_length=100,default='')
    experience= models.CharField(max_length=100,default='')
    

    
class Appointment(models.Model):
    user=models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor=models.ForeignKey(tbl_doctors, on_delete=models.CASCADE) 
    message=models.TextField(max_length=500)
    date = models.DateField(default='2023-12-31') 
    time=models.TextField(null=True, blank=True)
    status=models.CharField(max_length=100,default='pending')
    

    