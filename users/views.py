from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import Patient, Doctor, Chatrooms, Messages
from .models import Appointment, Treatment, Specialization, Schedule
from .forms import AppointmentForm

# Create your views here.

#to check group of user
def is_patient(user):
    return user.groups.filter(name='Patient').exists()

def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()
 
 
 #to work with schedule and available slots
def string_to_schedule(s): # s - string
    sched = {'Available' : [], 'Working' : []}
    for i in range(len(s)):
        if s[i] == '0':
            sched['Available'].append(i+9)
        elif s[i]=='1':
            sched['Working'].append(i+9)
    return sched
    

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('personal'))
    
def login_view(request):

    #when submitted (button clicked)
    if request.method == "POST":

        #authenticate user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        
        #redirect to their pages
        if user is not None: 
            login(request, user)

            return HttpResponseRedirect(reverse('personal'))
        else:
            return render(request, 'users/login.html', {
                'message': 'Invalid credentials'
            })
    
    #if method==get: not yet submitted (opened before logining)
    return render(request, 'users/login.html')

@login_required
def personal(request):

    user = request.user

    if is_patient(user):

        #if there is no chatroom of the patient to the doctor, create one
        if not user.patient.chatrooms.first(): 
            Chatrooms.objects.create(patient = user.patient, doctor = user.patient.assigned_doctor)

        #if form submitted (patient info form)
        if request.method == "POST":
            user.patient.gov_id = request.POST["gov_id"]
            user.patient.name = request.POST["name"]
            user.patient.surname = request.POST["surname"]
            user.patient.middle_name = request.POST["middle_name"]
            user.patient.address = request.POST["address"]
            user.patient.phone_number = request.POST["phone_number"]
            user.patient.email = request.POST["email"]
            user.patient.contact_close = request.POST["contact_close"]
            user.patient.save()
            return HttpResponseRedirect(reverse('personal'))
            
        return render(request, 'users/patient_page.html')

    elif is_doctor(user):
        return render(request, 'users/doctor_page.html')

    return HttpResponseRedirect(reverse('admin:index'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


#search for appointment (search bar to search by doctor name or specialization name)
def search_appointment(request):
    #search bar
    if 'search' in request.GET:
        keyword = request.GET['search']
        doctor_names = Doctor.objects.values_list('name', flat = True)
        specs = Specialization.objects.values_list('name', flat = True)
        if keyword in doctor_names: 
            return redirect('search', object = 'doctor', name = keyword)
        elif keyword in specs:
            id = Specialization.objects.filter(name=keyword).values_list('id',flat=True)[0]
            return redirect('search', object = 'spec', name = str(id))

    return render(request, 'users/appointment_search.html', {
        'specs' :  Specialization.objects.all()
    })


#website with doctor with given specialization or name
def search(request, object, name):
    if object == 'spec':
        id = int(name)
        spec = Specialization.objects.get(id=id)
        doctors_name = Doctor.objects.filter(spec = spec)   
    elif object == 'doctor':
        doctors_name = Doctor.objects.filter(name = name) 
        
    doctors = Schedule.objects.filter(doctor__in=doctors_name).values('doctor__name', 'doctor__surname', 
                                        'doctor__photo', 'mon_hours', 'tue_hours', 'wed_hours', 'thu_hours',
                                        'fri_hours','doctor__user_id', 'week')
    
    for d in doctors:
        d['available_mon'] = string_to_schedule(d['mon_hours'])['Available']
        d['available_tue'] = string_to_schedule(d['tue_hours'])['Available'] 
        d['available_wed'] = string_to_schedule(d['wed_hours'])['Available'] 
        d['available_thu'] = string_to_schedule(d['thu_hours'])['Available'] 
        d['available_fri'] = string_to_schedule(d['fri_hours'])['Available']
        d['doctor__user_id'] = str(d['doctor__user_id'])
        d['mon_day'] = d['week']  
        d['tue_day'] = d['week'] + datetime.timedelta(days=1)
        d['wed_day'] = d['week'] + datetime.timedelta(days=2)
        d['thu_day'] = d['week'] + datetime.timedelta(days=3)
        d['fri_day'] = d['week'] + datetime.timedelta(days=4)
          
    
    return render(request, 'users/search.html', {
        'doctors' :  doctors, 
    })
    
#appointment
@login_required
def appointment(request, id):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('personal'))
    else:
        doctor = Doctor.objects.get(user_id=id)
        patient = Patient.objects.get(user_id=request.user)
        form = AppointmentForm({'patient' : patient, 'doctor' : doctor})

    return render(request, 'users/appointment.html', {
        'form' :  form,
    })

#treatment
def treatment(request):
    user = request.user

    #if form submitted (treatment form)
    if request.method=="POST":
        Treatment.objects.create(
            patient=user.doctor.assigned_patients.get(gov_id=request.POST["gov_id"]),
            doctor=user.doctor,
            medicaments=request.POST["medicaments"],
            description=request.POST["description"],
            date=request.POST["date"]
        )

    return render(request, 'users/doctor_page.html')



#sens message to chat
def send(request, chatroom_id):
    
    if request.method == "POST":
        user = request.user

        if is_patient(user):
            Messages.objects.create(
                user = user,
                message_text = request.POST["message_text"],
                chatroom = Chatrooms.objects.get(id=chatroom_id),
                username = str(user.patient)
            )
        
        if is_doctor(user):
            Messages.objects.create(
                user = user,
                message_text = request.POST["message_text"],
                chatroom = Chatrooms.objects.get(id=chatroom_id),
                username = str(user.doctor)
            )

        return HttpResponseRedirect(reverse('personal'))


def updateMessages(request, chatroom_id):
    #get messages
    chatroom = Chatrooms.objects.get(id=chatroom_id)
    messages = chatroom.messages

    user = request.user

    #pass the message info from django model to js
    return JsonResponse({
        'messages' : list(messages.values())
    })

