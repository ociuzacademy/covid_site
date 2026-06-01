from django.shortcuts import render,redirect
from . models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . detect import predict_covid_status

# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_home(request):
    return render(request,'admin/admin_home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Validate the form data (add more validation if needed)
        if not name or not email or not message:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Send email (update 'your_email@example.com' with your email address)
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'your_email@example.com',
            ['your_email@example.com'],  # Add more recipients if needed
            fail_silently=False,
        )

        return JsonResponse({'success': 'Message sent successfully'})
    else:
        return render(request, 'contact.html')  # Render the contact form template

def admin_view_hospital(request):
    data = tbl_register.objects.all().filter(utype='hospital',status='pending')
    return render(request,'admin/admin_view_hospital.html',{'data':data})


def admin_view_user(request):
    data = tbl_register.objects.all().filter(utype='user')
    return render(request,'admin/admin_view_user.html',{'data':data})


def admin_viewpending(request):
    pending_hospitals = tbl_register.objects.filter(status='pending')
    return render(request, 'admin/admin_viewpending.html', {'pending_hospitals': pending_hospitals})

def admin_viewapproved(request):
    approved_hospitals = tbl_register.objects.filter(status='approved')
    return render(request, 'admin/admin_viewapproved.html', {'pending_hospitals': approved_hospitals})

def admin_viewrejected(request):
    rejected_hospitals = tbl_register.objects.filter(status='rejected')
    return render(request, 'admin/admin_viewrejected.html', {'pending_hospitals': rejected_hospitals})

# def admin_approve_hospital(request):
#     id=request.GET['id']
#     tbl_register.objects.all().filter(id=id).update(status='pending')
#     return render(request,'admin/admin_approve_hospital.html')

def admin_approve(request,id):
    hospital = tbl_register.objects.get(id=id)
    hospital.status = 'approved'
    hospital.save()
    return redirect('/admin_viewpending/')

def admin_reject(request, id):
    hospital = tbl_register.objects.get(id=id)
    hospital.status = 'rejected'
    hospital.save()
    return redirect('/admin_viewpending/')
def admin_rejectapproved(request, id):
    hospital = tbl_register.objects.get(id=id)
    hospital.status = 'rejected'
    hospital.save()
    return redirect('/admin_viewapproved/')
def admin_approverejected(request, id):
    hospital = tbl_register.objects.get(id=id)
    hospital.status = 'approved'
    hospital.save()
    return redirect('/admin_viewrejected/')

def admin_reject_hospital(request):
    id=request.GET['id']
    tbl_register.objects.all().filter(id=id).update(status='rejected')
    return render(request,'admin/admin_view_hospital.html')


def admin_view_hospital(request):
    hospitals = tbl_register.objects.filter(status='approved')
    return render(request, 'admin/admin_view_hospital.html', {'hospitals': hospitals})

def admin_view_doctors(request, id):
    doctors = tbl_doctors.objects.filter(hospital_id=id)
    return render(request, 'admin/admin_view_doctors.html', {'doctors': doctors})

def admin_view_appointments(request):

    # Get filter values
    selected_date = request.GET.get('selected_date')
    selected_doctor = request.GET.get('selected_doctor')

    # Get all doctors
    doctors = tbl_doctors.objects.all()

    # Get all appointments
    appointments = Appointment.objects.all()

    # Filter by date
    if selected_date:

        appointments = appointments.filter(
            date=selected_date
        )

    # Filter by doctor
    if selected_doctor:

        appointments = appointments.filter(
            doctor_id=selected_doctor
        )

    # Latest first
    appointments = appointments.order_by('-id')

    return render(
        request,
        'admin/admin_view_appointments.html',
        {
            'bookings': appointments,
            'doctors': doctors,
            'selected_date': selected_date,
            'selected_doctor': selected_doctor
        }
    )
# --------user --------

def user_register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        plc=request.POST.get('plc')
        bldgrp=request.POST.get('bldgrp')
        weight=request.POST.get('weight')
        height=request.POST.get('height')
        tbl_register(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,utype='user',plc=plc,age=age,height=height,weight=weight,bldgrp=bldgrp,gender=gender).save()
        return render(request,'index.html')
    else:
        return render(request,'user_register.html')


def user_profile(request):
    id=request.session['id']
    data=tbl_register.objects.all().filter(id=id)
    return render(request,'user/user_profile.html',{'data':data})



def user_edit_profile(request):
    id = request.session['id']

    if request.method == 'POST':

        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        gender = request.POST.get('gender')
        adrs = request.POST.get('adrs')
        phn = request.POST.get('phn')
        plc = request.POST.get('plc')

        age = request.POST.get('age')
        # status = request.POST.get('status')
        bldgrp = request.POST.get('bldgrp')
        weight = request.POST.get('weight')
        height = request.POST.get('height')

        tbl_register.objects.filter(id=id).update(
            name=name,
            uname=uname,
            email=email,
            pswd=pswd,
            adrs=adrs,
            phn=phn,
            plc=plc,
            gender=gender,
            age=age,
            # status=status,
            bldgrp=bldgrp,
            weight=weight,
            height=height
        )

        return HttpResponseRedirect('/user_profile/')

    else:
        data = tbl_register.objects.filter(id=id)

        return render(
            request,
            'user/user_edit_profile.html',
            {'data': data}
        )
    
def user_home(request):
    return render(request,'user/user_home.html')

import uuid,os
import uuid
import os
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import tbl_register, tbl_coviddetails
from .detect import predict_covid_status


def user_upload_coviddetails(request):

    id = request.session['id']

    if request.method == 'POST':

        user_id = request.session['id']

        doxray = request.POST.get('doxray')
        effected = request.POST.get('effected')
        symptoms = request.POST.get('symptoms')

        xray_image = request.FILES.get('xray_image')

        # Get user
        user_instance = tbl_register.objects.get(id=user_id)

        # Generate random image filename
        random_filename = f"{uuid.uuid4()}{os.path.splitext(xray_image.name)[1]}"

        # Create new record every time
        user_coviddetails = tbl_coviddetails.objects.create(
            user=user_instance,
            effected=effected,
            doxray=doxray,
            symptoms=symptoms
        )

        # Save image
        user_coviddetails.xray_image.save(
            random_filename,
            xray_image
        )

        # Model path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        model_path = os.path.join(BASE_DIR, 'Detection_covid19.h5')

        # Predict result
        image_path = user_coviddetails.xray_image.path

        prediction_result = predict_covid_status(
            image_path,
            model_path
        )

        print("Prediction Result:", prediction_result)

        # Save result
        user_coviddetails.covid_result = prediction_result

        user_coviddetails.save()

        return redirect('/user_view_coviddetails/')

    else:

        user_data = tbl_register.objects.filter(id=id)

        return render(
            request,
            'user/user_upload_coviddetails.html',
            {'user_data': user_data}
        )
def user_view_coviddetails(request):

    id = request.session['id']

    user_instance = tbl_register.objects.get(id=id)

    data = tbl_coviddetails.objects.filter(user=user_instance)

    return render(
        request,
        'user/user_view_coviddetails.html',
        {'data': data}
    )


def user_view_hospitals(request):
    hospitals = tbl_register.objects.filter(status='approved')
    return render(request, 'user/user_view_hospitals.html', {'hospitals': hospitals})

def user_view_doctors(request,id):
    doctors = tbl_doctors.objects.all().filter(hospital_id=id)
    return render(request, 'user/user_view_doctors.html', {'doctors': doctors})

def user_book_appointment(request, id):
    user_id = request.session['id']
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')
        user_instance=tbl_register.objects.get(id=user_id)
        doctor_instance = tbl_doctors.objects.get(id=id)  # Make sure to have the correct doctor_id
        # Assuming you have an Appointment model to store the booking details
        appointment_instance = Appointment.objects.create(doctor=doctor_instance,user_id=user_id,date=date,time=time,message=message)
            # Add other fields as needed)
        success_message = 'Appointment booked successfully'
        return render(request, 'user/user_book_appointment.html', {'success_message': success_message})
    else:
        user_profile = tbl_register.objects.filter(id=user_id)
        return render(request, 'user/user_book_appointment.html', {'user_profile': user_profile})

def user_view_bookings(request):
    user_id = request.session['id']

    # Retrieve bookings for the logged-in user
    bookings = Appointment.objects.filter(user_id=user_id)

    return render(request, 'user/user_view_bookings.html', {'bookings': bookings})
#     doctor = tbl_doctors.objects.all().filter(id=id)
#     return render(request, 'user/user_book_appointment.html')


# -------- HOSPITAL --------
    

def hospital_home(request):
    return render(request,'hospital/hospital_home.html')

def hospital_register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        plc=request.POST.get('plc')
        tbl_register(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,utype='hospital',plc=plc,status='pending').save()
        return render(request,'index.html')
    else:
        return render(request,'hospital_register.html')

def hospital_profile(request):
    id=request.session['id']
    data=tbl_register.objects.all().filter(id=id)
    return render(request,'hospital/hospital_profile.html',{'data':data})


def hospital_edit_profile(request):
    id=request.session['id']
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pswd=request.POST.get('pswd')
        adrs=request.POST.get('adrs')
        phn=request.POST.get('phn')
        plc=request.POST.get('plc')
        tbl_register.objects.all().filter(id=id).update(name=name,uname=uname,email=email,pswd=pswd,adrs=adrs,phn=phn,plc=plc)
        return HttpResponseRedirect('/hospital_profile/')
    else:
        data=tbl_register.objects.all().filter(id=id)
        return render(request,'hospital/hospital_edit_profile.html',{'data':data})
 
# from datetime import datetime, timedelta   
def hospital_add_doctors(request):
    id=request.session['id']
    if request.method=='POST':
        doc_name=request.POST.get('doc_name')
        phn=request.POST.get('phn')
        email=request.POST.get('email')
        designation=request.POST.get('designation')
        qualification=request.POST.get('qualification')
        availability=request.POST.get('availability')
        experience=request.POST.get('experience')
        time = request.POST.get('time')
        hospital_instance = tbl_register.objects.get(id=id)
        doctor_instance=tbl_doctors.objects.create(hospital=hospital_instance,doc_name=doc_name, availability=availability,phn=phn,email=email,designation=designation,qualification=qualification,experience=experience,time=time).save()
        
        # success_message = 'Doctor added successfully'
        # return render(request, 'hospital/hospital_add_doctors.html',{'success_message':success_message})
        return redirect('/hospital_view_doctors/')
    
    else:
        # user_data = tbl_register.objects.filter(id=id)
        return render(request, 'hospital/hospital_add_doctors.html')
    

def hospital_view_doctors(request):
    id=request.session['id']
    doctors = tbl_doctors.objects.all().filter(hospital_id=id)
    return render(request, 'hospital/hospital_view_doctors.html', {'doctors': doctors})

def hospital_edit_doctor(request, doctor_id):
    doctor = tbl_doctors.objects.get(id=doctor_id)
    if request.method == 'POST':
        doc_name = request.POST.get('doc_name')
        phn = request.POST.get('phn')
        email = request.POST.get('email')
        designation = request.POST.get('designation')
        qualification = request.POST.get('qualification')
        availability = request.POST.get('availability')
        experience = request.POST.get('experience')
        time = request.POST.get('time')
        
        # hospital_instance = tbl_register.objects.get(id=id)

        # Update the doctor instance
        doctor.doc_name = doc_name
        doctor.phn = phn
        doctor.email = email
        doctor.designation = designation
        doctor.qualification = qualification
        doctor.availability = availability
        doctor.experience = experience
        doctor.time = time  # Assuming you have a 'time' field in your model
        doctor.save()

        success_message = 'Doctor updated successfully'
        # return render(request, 'hospital/hospital_edit_doctor.html', {'success_message': success_message, 'doctor': doctor})
        return redirect('/hospital_view_doctors/')
    else:
        return render(request, 'hospital/hospital_edit_doctor.html', {'doctor': doctor})

def hospital_delete_doctor(request, doctor_id):
    doctor = tbl_doctors.objects.get(id=doctor_id)
    if request.method == 'POST':
        # Check if the user has confirmed the deletion
        if request.POST.get('confirm_delete'):
            doctor.delete()
            return redirect('/hospital_view_doctors/')

    return render(request, 'hospital/hospital_view_doctors.html')



def hospital_view_patient(request):
    hospital_id = request.session['id']
    selected_date = request.GET.get('selected_date')
    selected_doctor = request.GET.get('selected_doctor')
    doctors = tbl_doctors.objects.filter(hospital=hospital_id)
    appointments = Appointment.objects.filter(doctor__hospital=hospital_id)
    if selected_date:
        appointments = appointments.filter(date=selected_date)

    if selected_doctor:
        appointments = appointments.filter(doctor__id=selected_doctor)

    appointments = appointments.order_by('-id')
    # Fetch tbl_coviddetails for the patients associated with the hospital
    patient_coviddetails = tbl_coviddetails.objects.filter(user__id__in=appointments.values('user__id'))
    return render(request, 'hospital/hospital_view_patient.html', {'bookings': appointments, 'doctors': doctors, 'patient_coviddetails': patient_coviddetails})






def hospital_view_bookings(request):

    hospital_id = request.session['id']
    selected_date = request.GET.get('selected_date')
    selected_doctor = request.GET.get('selected_doctor')

    # Fetch all doctors associated with the login hospital for the dropdown
    doctors = tbl_doctors.objects.filter(hospital=hospital_id)

    # Apply filters based on the selected date and doctor
    appointments = Appointment.objects.filter(doctor__hospital=hospital_id, status='pending')

    if selected_date:
        appointments = appointments.filter(date=selected_date)

    if selected_doctor:
        appointments = appointments.filter(doctor__id=selected_doctor)

    # Fetch user id for each appointment
    user_ids = appointments.values_list('user', flat=True)

    # Fetch user objects based on the user ids
    users = tbl_register.objects.filter(id__in=user_ids)


    appointments = appointments.order_by('-id')
    return render(request, 'hospital/hospital_view_bookings.html', {'bookings': appointments, 'doctors': doctors,'users': users})



def hospital_view_approved_bookings(request):
    
    hospital_id = request.session['id']
    selected_date = request.GET.get('selected_date')
    selected_doctor = request.GET.get('selected_doctor')

    # Fetch all doctors associated with the login hospital for the dropdown
    doctors = tbl_doctors.objects.filter(hospital=hospital_id)
    # user = tbl_register.objects.all().filter(utype='user')
    
    

    # Apply filters based on the selected date and doctor
    appointments = Appointment.objects.filter(doctor__hospital=hospital_id, status='approved')

    if selected_date:
        appointments = appointments.filter(date=selected_date)

    if selected_doctor:
        appointments = appointments.filter(doctor__id=selected_doctor)
    appointments = appointments.order_by('-id')
    return render(request, 'hospital/hospital_view_approved_bookings.html', {'bookings': appointments, 'doctors': doctors})




from django.shortcuts import get_object_or_404

def hospital_approve_booking(request, booking_id):
    id=request.session['id']
    # Add logic to ensure the booking belongs to the hospital
    booking = get_object_or_404(Appointment, id=booking_id, doctor__hospital=id)
    booking.status = 'Approved'
    booking.save()
    bookings = Appointment.objects.filter(doctor__hospital=id, status='pending')
    return render(request, 'hospital/hospital_view_bookings.html', {'bookings': bookings})


def hospital_reject_booking(request, booking_id):
    id=request.session['id']
    # Add logic to ensure the booking belongs to the hospital
    booking = get_object_or_404(Appointment, id=booking_id, doctor__hospital=id)
    booking.status = 'Rejected'
    booking.save()
    bookings = Appointment.objects.filter(doctor__hospital=id, status='pending')
    return render(request, 'hospital/hospital_view_bookings.html', {'bookings': bookings})


def login(request):
    if request.method == "POST":
        pswd = request.POST['pswd']
        email = request.POST['email']
        var = tbl_register.objects.all().filter(pswd=pswd, email=email, utype='user')
        var2 = tbl_register.objects.all().filter(pswd=pswd, email=email, utype='hospital')
        var3= tbl_register.objects.all().filter(pswd=pswd, email=email, utype='admin')

        if var:
            for x in var:
                request.session['id'] = x.id
            return render(request, 'user/user_home.html')
        elif var2:
            for x in var2:
                request.session['id'] = x.id
            return render(request, 'hospital/hospital_home.html')
        
        elif var3:
            for x in var3:
                request.session['id'] = x.id
            return render(request, 'admin/admin_home.html')

        else:
            txt = """<script>alert("Invalid user Credentials....");window.location='/';</script>"""
            return HttpResponse(txt) 
    else:
        return render(request, "login.html")



def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,'index.html')


