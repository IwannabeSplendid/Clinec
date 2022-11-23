from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        
        labels = {
            'patient': ('Patient'),
            'doctor': ('Doctor'),
            'medical_service': ('Medical service'),
            'date': ('Appointment date'),
        }
        