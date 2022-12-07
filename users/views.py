from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from .models import Patient, Doctor, Chatrooms, Messages, User
from .models import Appointment, Treatment, Specialization, Schedule
from .forms import AppointmentForm, UserForm, PatientForm, DoctorForm

from django.core.paginator import Paginator

# Create your views here.

#to check group of user
def is_patient(user):
    try:
        if user.patient:
            return True
    except:
        return False

def is_doctor(user):
    try:
        if user.doctor:
            return True
    except:
        return False

def is_admin(user):
    return user.is_staff
 
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
            user.email = request.POST["email"]
            user.save()
            user.patient.gov_id = request.POST["gov_id"]
            user.patient.name = request.POST["name"]
            user.patient.surname = request.POST["surname"]
            user.patient.middle_name = request.POST["middle_name"]
            user.patient.address = request.POST["address"]
            user.patient.phone_number = request.POST["phone_number"]
            user.patient.contact_close = request.POST["contact_close"]
            user.patient.save()
            return HttpResponseRedirect(reverse('personal'))
            
        return render(request, 'users/patient_page.html')

    elif is_doctor(user):
        return render(request, 'users/doctor_page.html')
    
    elif is_admin(user):
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        
        return render(request, 'users/admin_page.html', {
            'patients' : patients, 'doctors' : doctors
        })

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
        'specs' :  Specialization.objects.all(),
        'doctors' : Doctor.objects.all()
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
                                     'mon_hours', 'tue_hours', 'wed_hours', 'thu_hours',
                                      'fri_hours','doctor__user_id', 'week')
    
    for d in doctors:
        d['available_mon'] = string_to_schedule(d['mon_hours'])['Available']
        d['available_tue'] = string_to_schedule(d['tue_hours'])['Available'] 
        d['available_wed'] = string_to_schedule(d['wed_hours'])['Available'] 
        d['available_thu'] = string_to_schedule(d['thu_hours'])['Available'] 
        d['available_fri'] = string_to_schedule(d['fri_hours'])['Available']
        d['doctor__user_id'] = str(d['doctor__user_id'])
        d['mon_day'] = d['week'] 
        d['tue_day'] = d['week'] + timedelta(days=1)
        d['wed_day'] = d['week'] + timedelta(days=2)
        d['thu_day'] = d['week'] + timedelta(days=3)
        d['fri_day'] = d['week'] + timedelta(days=4)
        d['photo']=Doctor.objects.get(user_id= d['doctor__user_id']).photo

    # return render(request, 'users/search.html', {
    #     'doctors' :  doctors, 
    # })
    paginator = Paginator(doctors, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/search.html', {'page_obj': page_obj})
    
#appointment
@login_required
def appointment(request, id, h, day):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
        
        #update schedule so that the time will not be available
        date = form['date'].value()
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        h = date.time().hour
        doctor = Doctor.objects.get(user_id=form['doctor'].value())
        schedule = Schedule.objects.filter(doctor=doctor)[0]
        if date.weekday()==0:
            s = schedule.mon_hours
            schedule.mon_hours=s[:h-9]+'1'+s[h-8:]
        elif date.weekday()==1:
            s = schedule.tue_hours
            schedule.tue_hours=s[:h-9]+'1'+s[h-8:]
        elif date.weekday()==2:
            s = schedule.wed_hours
            schedule.wed_hours=s[:h-9]+'1'+s[h-8:]
        elif date.weekday()==3:
            s = schedule.thu_hours
            schedule.thu_hours=s[:h-9]+'1'+s[h-8:]
        elif date.weekday()==4:
            s = schedule.fri_hours
            schedule.fru_hours=s[:h-9]+'1'+s[h-8:]
        schedule.save()
        
        return HttpResponseRedirect(reverse('personal'))
    else:
        doctor = Doctor.objects.get(user_id=id)
        patient = Patient.objects.get(user_id=request.user)
        if day == '0':
            form = AppointmentForm({'patient' : patient, 'doctor' : doctor})   
        else:
            date = datetime.strptime(day, '%Y-%m-%d') + timedelta(hours=h)
            form = AppointmentForm({'patient' : patient, 'doctor' : doctor, 'date' : date})      
    
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

# admin register user 
@staff_member_required
def register_view(request):
    form = UserForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'users/register.html', {'form': form})    
        user = User.objects.filter(email = form['email'].value())[0]
        
        #create user admin
        if request.POST['role']=='Admin':
            user.is_staff = True
            user.is_superuser= True
            user.save()
        elif request.POST['role']=='Patient':
            return redirect('register_patient', id = user.id) 
        elif request.POST['role']=='Doctor':   
            return redirect('register_doctor', id = user.id) 
        
        return HttpResponseRedirect(reverse('personal'))
            
    return render(request, 'users/register.html', {
        'form' :  form
    })

# admin register patient 
@staff_member_required
def register_p(request, id):  
    form = PatientForm({"registration_date": datetime.today().date()})  
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = str(id)
        form = PatientForm(data)
        if form.is_valid():
            form.save()
                    
        return HttpResponseRedirect(reverse('personal'))
        
    return render(request, 'users/register_p.html', {
        'form' :  form
    })
    

# admin register patient 
@staff_member_required
def register_d(request, id):
    form = DoctorForm()  
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = str(id)
        form = DoctorForm(data, request.FILES)
        if form.is_valid():
            form.save()
        
        doctor = Doctor.objects.get(user_id=id)
        schedule = Schedule(doctor = doctor)
        schedule.save()
                    
        return HttpResponseRedirect(reverse('personal'))
        
    return render(request, 'users/register_d.html', {
        'form' :  form
    })


#update
@staff_member_required    
def update(request, role, id):
    if role == 'Patient':
        patient = Patient.objects.get(user_id = str(id))
        form = PatientForm(instance=patient) 
        
        if request.method == 'POST':
            if 'Delete' in request.POST:
                user = User.objects.get(id = id)
                patient.delete()
                user.delete()
            else:
                form = PatientForm(request.POST, instance=patient)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse('personal'))
        
    elif role == 'Doctor':
        doctor = Doctor.objects.get(user_id = str(id))
        form = DoctorForm(instance=doctor)
          
        if request.method == 'POST':
            if 'Delete' in request.POST:
                user = User.objects.get(id = id)
                doctor.delete()
                user.delete()
            else:
                form = DoctorForm(request.POST, request.FILES, instance=doctor)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse('personal'))
    
        
    return render(request, 'users/update.html', {
        'form' :  form, 'role' : role
    })
