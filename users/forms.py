from django import forms
from .models import Appointment, Doctor, Patient, User
from django.contrib.auth.forms import UserCreationForm

 
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
            "medical_service" : "Medical Service",
            "date" : "Date",
            "patient" : "Patient",
            "doctor" : "Doctor"
        }
        widgets = {
            "medical_service": forms.Select(attrs={'class': 'medical_service'}),
            "date": forms.DateInput(attrs={'type': 'date', 'class': 'date'}),
            "patient" : forms.Select(attrs={'class': 'patient'}),
            "doctor" : forms.Select(attrs={'class': 'doctor'})
        }


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ["date_of_birth", "gov_id", "IIN", "name", "surname", "middle_name", "blood_group", "contact_close", 
                  "phone_number", "address", "marital_status", "registration_date", "assigned_doctor", "user"]
        widgets = {
            "user": forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "registration_date" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""}),
            "IIN" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': ""})
        }


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "address", "user"] 

        widgets = {"user": forms.HiddenInput()} 
        
        labels = {
            "spec" : "Department"
        }      

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)

        for fieldname in ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "address", "user"] :
            self.fields[fieldname].help_text = None
