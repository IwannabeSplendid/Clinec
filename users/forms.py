from django import forms
from .models import Appointment, Doctor, Patient, User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe


css_classes = "col-span-2 border-gray-200 rounded-global"

medical_service_choices = [
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
            "medical_service": "Medical service",
            "date": "Date",
            "doctor": "Doctor"
        }

        widgets = {
            "medical_service": forms.Select(attrs={'class': css_classes}),
            "date":            forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': css_classes}),
            "patient":         forms.HiddenInput(),
            "doctor":          forms.Select(attrs={'class': css_classes})
        }


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for fieldname in ['email', 'username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:

        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username":  forms.TextInput(attrs={'class': css_classes}),
            "email":     forms.TextInput(attrs={'class': css_classes}),
            "password1": forms.TextInput(attrs={'class': css_classes}),
            "password2": forms.TextInput(attrs={'class': css_classes})
        }


class PatientForm(forms.ModelForm):

    class Meta:

        model = Patient
        fields = [
            "date_of_birth", "gov_id", "IIN", "name",
            "surname", "middle_name", "blood_group", "contact_close",
            "phone_number", "address", "marital_status",
            "registration_date", "assigned_doctor", "user"
        ]

        widgets = {
            "user":              forms.HiddenInput(),
            "date_of_birth":     forms.DateInput(attrs={'type': 'date', 'class': css_classes}),
            "IIN":               forms.NumberInput(attrs={'class': css_classes}),
            "gov_id":            forms.NumberInput(attrs={'class': css_classes}),
            "name":              forms.TextInput(attrs={'class': css_classes}),
            "surname":           forms.TextInput(attrs={'class': css_classes}),
            "middle_name":       forms.TextInput(attrs={'class': css_classes}),
            "blood_group":       forms.Select(attrs={'class': css_classes}),
            "phone_number":      forms.NumberInput(attrs={'class': css_classes}),
            "contact_close":     forms.NumberInput(attrs={'class': css_classes}),
            "marital_status":    forms.Select(attrs={'class': css_classes}),
            "registration_date": forms.DateInput(attrs={'type': 'date', 'class': css_classes}),
            "assigned_doctor":   forms.Select(attrs={'class': css_classes}),
            "address":           forms.TextInput(attrs={'class': css_classes}),
        }


class DoctorForm(forms.ModelForm):

    class Meta:

        model = Doctor
        fields = [
            "date_of_birth", "IIN", "gov_id",
            "name", "surname", "middle_name", "spec",
            "phone_number", "experience", "photo",
            "address", "category", "appointment_price",
            "education", "rating", "user"
        ]

        widgets = {
            "user":              forms.HiddenInput(),
            "date_of_birth":     forms.DateInput(attrs={'type': 'date', 'class': css_classes}),
            "IIN":               forms.NumberInput(attrs={'class': css_classes}),
            "gov_id":            forms.NumberInput(attrs={'class': css_classes}),
            "name":              forms.TextInput(attrs={'class': css_classes}),
            "surname":           forms.TextInput(attrs={'class': css_classes}),
            "middle_name":       forms.TextInput(attrs={'class': css_classes}),
            "spec":              forms.Select(attrs={'class': css_classes}),
            "phone_number":      forms.NumberInput(attrs={'class': css_classes}),
            "experience":        forms.TextInput(attrs={'class': css_classes}),
            "photo":             forms.FileInput(attrs={'class': 'col-span-2'}),
            "address":           forms.TextInput(attrs={'class': css_classes}),
            "category":          forms.TextInput(attrs={'class': css_classes}),
            "appointment_price": forms.NumberInput(attrs={'class': css_classes}),
            "education":         forms.TextInput(attrs={'class': css_classes}),
            "rating":            forms.NumberInput(attrs={'class': css_classes}),
        }

        labels = {
            "spec": "Department"
        }

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        for fieldname in [
            "date_of_birth", "IIN", "gov_id", "name",
            "surname", "middle_name", "spec", "phone_number",
            "experience", "photo", "address", "category", "appointment_price",
            "education", "rating", "address", "user"
        ]:
            self.fields[fieldname].help_text = None
