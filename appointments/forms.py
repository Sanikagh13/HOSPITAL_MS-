from django import forms
from .models import Patient, Doctor, Appointment

# forms.py
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'age', 'disease']  # <--- ERROR IS HERE

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'instructions'] # Add instructions here
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'instructions': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g. Fasting required'}),
        }