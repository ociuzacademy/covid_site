from django.urls import include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('about/',views.about),
    path('contact/',views.contact),


    path('user_register/',views.user_register),
    path('user_home/',views.user_home),
    path('user_profile/',views.user_profile),
    path('user_edit_profile/',views.user_edit_profile),
    path('user_upload_coviddetails/',views.user_upload_coviddetails),
    path('user_view_hospitals/',views.user_view_hospitals),
    path('user_view_doctors/<int:id>/',views.user_view_doctors),
    path('user_book_appointment/<int:id>/',views.user_book_appointment),
    path('user_view_bookings/',views.user_view_bookings),
    path('user_view_coviddetails/',views.user_view_coviddetails),


    path('hospital_register/',views.hospital_register),
    path('hospital_home/',views.hospital_home),
    path('hospital_profile/',views.hospital_profile),
    path('hospital_edit_profile/',views.hospital_edit_profile),
    path('hospital_add_doctors/',views.hospital_add_doctors),
    path('hospital_view_doctors/',views.hospital_view_doctors),
    path('hospital_edit_doctor/<int:doctor_id>/',views.hospital_edit_doctor),
    path('hospital_delete_doctor/<int:doctor_id>/',views.hospital_delete_doctor),
    path('hospital_view_bookings/',views.hospital_view_bookings),
    path('hospital_approve_booking/<int:booking_id>/',views.hospital_approve_booking),
    path('hospital_reject_booking/<int:booking_id>/',views.hospital_reject_booking),
    path('hospital_view_approved_bookings/',views.hospital_view_approved_bookings),
    path('hospital_view_patient/',views.hospital_view_patient),
    
    


    
    
    
    path('admin_home/',views.admin_home),
    path('admin_view_hospital/',views.admin_view_hospital),
    path('admin_view_user/',views.admin_view_user),
    path('admin_viewpending/', views.admin_viewpending),
    path('admin_viewrejected/', views.admin_viewrejected),
    path('admin_viewapproved/', views.admin_viewapproved),
    path('admin_approve/<int:id>/', views.admin_approve),
    path('admin_approverejected/<int:id>/', views.admin_approverejected),
    path('admin_rejectapproved/<int:id>/', views.admin_rejectapproved),
    path('admin_approve/<int:id>/', views.admin_approve),
    path('admin_reject/<int:id>/', views.admin_reject),
    # path('admin_approve_hospital/',views.admin_approve_hospital),
    path('admin_reject_hospital/',views.admin_reject_hospital),
    path('admin_view_doctors/<int:id>/',views.admin_view_doctors),
    path('admin_view_hospital/',views.admin_view_hospital),
    path('admin_view_appointments/',views.admin_view_appointments),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
