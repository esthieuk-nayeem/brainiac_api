from django import forms
from django.contrib.auth.models import User
from .models import *


#for Attendance related form
presence_choices=(('Absent','Absent'),('Present','Present'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    topic = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'class': 'topic-input-style'}) )



class CreateBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_name','assigned_course']
      


class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_name','assigned_course']
      