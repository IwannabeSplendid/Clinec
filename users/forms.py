from django import forms
from .models import Appointment, Doctor, Patient, User
from django.contrib.auth.forms import UserCreationForm

 
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        
        labels = {
    
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
            "user": forms.HiddenInput(attrs={'class':'form-control', 'placeholder':""}),
            "registration_date" : forms.TextInput(attrs={'class':'form-control', 'placeholder':""}),
            "IIN" : forms.TextInput(attrs={'class':'form-control', 'placeholder':""})
        }


    
        

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "department_ID", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "address", "user"] 
        widgets = {"user": forms.HiddenInput()} 

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)

        for fieldname in ["date_of_birth", "IIN", "gov_id", "name", "surname", "middle_name", "department_ID", "spec", 
                  "phone_number", "experience", "photo", "address", "category", "appointment_price", 
                  "education", "rating", "address", "user"] :
            self.fields[fieldname].help_text = None
