from django import forms
from django.contrib.auth.models import User
from Dashboard.models import Student_Profile, Notes, Homework, Todo

class Student_Profile_Form(forms.ModelForm):
    class Meta():
        model = Student_Profile
        fields = ('Display_Name','Student_Branch','Student_Semester','Student_Profile_Photo')

class User_Form(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','email','password')
        widgets = {'password':forms.PasswordInput()}

class Notes_Form(forms.ModelForm):

    class Meta():
        model = Notes
        fields = ('Note_Title','Note_Description','Note_Document')
        widgets = {
            'Note_Document': forms.FileInput(attrs={'class': 'form-control'}),
        }

class Search_Form(forms.Form):
    Search_Text = forms.CharField(max_length=256, label="")

class DateInput(forms.DateInput):
    input_type = 'date'

class Homework_Form(forms.ModelForm):
    class Meta():
        model = Homework
        widgets = {'Homework_Due':DateInput()}
        fields = ['Homework_Subject','Homework_Title','Homework_Description','Homework_Due','Homework_Finished']
        # Fields To Be Excluded

# # Books
# class Search_Form(forms.Form):
#     text = forms.CharField(max_length=256, label="")

class Todo_Form(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('Todo_Title','Todo_Finished')
        # Fields To Be Included

# class Search_Form(forms.Form):
#     text = forms.CharField(max_length=256, label="")
