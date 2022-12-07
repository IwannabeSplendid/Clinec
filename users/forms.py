from django import forms
from .models import Appointment, Doctor, Patient, User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
 
medical_service_choices =[
    ("consultation", "Consultation"),
    ("examination", "Examination"),
    ("treatment", "Assign new treatment"),
]

class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        for fieldname in ["medical_service", 'date', 'patient', 'doctor']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = Appointment
        fields = "__all__"
        
        labels = {
            "medical_service" : "Medical service",
            "date" : "Date",
            "doctor" : "Doctor"
        }
        widgets = {
            "medical_service": forms.Select(attrs={
                'class': 'medical_service col-span-2 border-gray-200 rounded-global'
            }),
            "date": forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'date col-span-2 border-gray-200 rounded-global'
            }),
            "patient" : forms.HiddenInput(),
            "doctor" : forms.Select(attrs={
                'class': 'doctor col-span-2 border-gray-200 rounded-global'
            })
        }


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
        widgets = {
            "username": forms.TextInput(attrs={'class': 'username'}),
            "email": forms.TextInput(attrs={'class': 'email'}),
            "password1" : forms.TextInput(attrs={'class': 'password1'}),
            "password2" : forms.TextInput(attrs={'class': 'password2'})
        }


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ["date_of_birth", "gov_id", "IIN", "name", "surname", "middle_name", "blood_group", "contact_close", 
                  "phone_number", "address", "marital_status", "registration_date", "assigned_doctor", "user"]
        widgets = {"user": forms.HiddenInput(),
                   "date_of_birth": forms.DateInput(attrs={'type': 'date', 'class': 'date_of_birth'}),
                   "IIN": forms.NumberInput(attrs={'class': 'IIN'}),
                   "gov_id": forms.NumberInput(attrs={'class': 'gov_id'}),
                   "name": forms.TextInput(attrs={'class': 'name'}),
                   "surname": forms.TextInput(attrs={'class': 'surname'}),
                   "middle_name": forms.TextInput(attrs={'class': 'middle_name'}),
                   "blood_group": forms.Select(attrs={'class': 'blood_group'}),
                   "phone_number": forms.NumberInput(attrs={'class': 'phone_number'}),
                   "contact_close": forms.NumberInput(attrs={'class': 'contact_close'}),
                   "marital_status": forms.Select(attrs={'class': 'marital_status'}),
                   "registration_date": forms.DateInput(attrs={'type': 'date', 'class': 'registration_date'}),
                   "assigned_doctor": forms.Select(attrs={'class': 'assigned_doctor'}),
                   "address": forms.TextInput(attrs={'class': 'address'}),
                   }
        
      
class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "user"] 

        widgets = {"user": forms.HiddenInput(),
                   "date_of_birth": forms.DateInput(attrs={'type': 'date', 'class': 'date_of_birth'}),
                   "IIN": forms.NumberInput(attrs={'class': 'IIN'}),
                   "gov_id": forms.NumberInput(attrs={'class': 'gov_id'}),
                   "name": forms.TextInput(attrs={'class': 'name'}),
                   "surname": forms.TextInput(attrs={'class': 'surname'}),
                   "middle_name": forms.TextInput(attrs={'class': 'middle_name'}),
                   "spec": forms.Select(attrs={'class': 'department'}),
                   "phone_number": forms.NumberInput(attrs={'class': 'phone_number'}),
                   "experience": forms.TextInput(attrs={'class': 'experience'}),
                   "photo": forms.FileInput(attrs={'class': 'photo'}),
                   "category": forms.TextInput(attrs={'class': 'category'}),
                   "appointment_price": forms.NumberInput(attrs={'class': 'appointment_price'}),
                   "education": forms.TextInput(attrs={'class': 'education'}),
                   "rating": forms.NumberInput(attrs={'class': 'rating'}),
                   } 
        
        labels = {
            "spec" : "Department"
        }      

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)

        for fieldname in ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "address", "user"] :
            self.fields[fieldname].help_text = None2