from django import forms
from django.contrib.auth.models import User
from MAINAPP.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username', 'email' , 'password')

class ContactMessageForm(forms.ModelForm):
    class Meta():
        model =  ContactMessage
        fields =('reviewer_name','reviewer_email','reviewer_message',)

class ReportForm(forms.ModelForm):
    class Meta():
        model = Bug
        fields =('reported_on','problem','problem_description','problem_image',)

class MedicalProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = MedicalProfile
        fields =('updated_on','age','gender','blood_group','height','weight','emergency_contact','diabetic')
