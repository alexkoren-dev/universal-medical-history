from datetime import datetime

from django.db.models import Q
from django.shortcuts import render

from medical_visit.models import *
from usermgmt.models import UserDetails


# Create your views here.
def todayAppointments(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'today_appointments'

    if (request.method == "GET"):
        visits = Visit.objects.filter(
            Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False))

    elif (request.method == "POST"):
        data = request.POST

        if (data['category'] == 'patient_name'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False) & Q(
                    Q(patient__first_name__icontains=data['search_term']) | Q(
                        patient__last_name__icontains=data['search_term']) | Q(
                        patient__username__icontains=data['search_term'])))


        elif (data['category'] == 'purpose'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(date_time__date=datetime.now().date()) & Q(completed=False) & Q(
                    purpose__icontains=data['search_term']))



    ctxt['visits'] = visits.order_by('date_time')

    return render(request, 'dashboard/doctor_dash/today_appointments.html', context=ctxt)


def allAppointments(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'all_appointments'


    if (request.method == "GET"):
        visits = Visit.objects.filter(Q(doctor=request.user))

    elif (request.method == "POST"):
        data = request.POST


        if (data['category'] == 'patient_name'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    Q(patient__first_name__icontains=data['search_term']) | Q(
                        patient__last_name__icontains=data['search_term']) | Q(
                        patient__username__icontains=data['search_term'])))


        elif (data['category'] == 'purpose'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    purpose__icontains=data['search_term']))

        elif (data['category'] == 'diagnosis'):
            visits = Visit.objects.filter(
                Q(doctor=request.user) & Q(
                    diagnosis__icontains=data['search_term']))


        if(data['visit_date'] != ''):
            visits = visits.filter(date_time__date=data['visit_date'])


    ctxt['visits'] = visits.order_by('-date_time')

    return render(request, 'dashboard/doctor_dash/all_appointments.html', context=ctxt)


def medicalHistory(request):
    ctxt = {}
    ctxt['dash_type'] = 'doctor'
    ctxt['active'] = 'medical_history'

    patients = Visit.objects.filter(doctor=request.user).values('patient').distinct()
    patients_details = UserDetails.objects.filter(user__in=patients)


    if(request.method == "POST"):
        data = request.POST

        if(data['category'] == "patient_name"):
            patients_details = patients_details.filter(Q(user__first_name__icontains=data['search_term']) | Q(user__last_name__icontains=data['search_term']) | Q(user__username__icontains=data['search_term']))

        elif(data['category'] == "patient_id"):
            patients_details = patients_details.filter(user__id=data['search_term'])

        elif(data['category'] == "city"):
            patients_details = patients_details.filter(city__icontains=data['search_term'])


    ctxt['patients'] = patients_details

    return render(request, 'dashboard/doctor_dash/medical_history.html', context=ctxt)
