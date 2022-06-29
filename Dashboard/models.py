from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student_Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    Display_Name = models.CharField(max_length=256)
    Student_Branch = models.CharField(max_length=256,blank=True)
    Student_Semester = models.IntegerField(blank=True)
    Student_Profile_Photo = models.ImageField(upload_to='Profile_Pics',blank=True)

    class Meta:
        verbose_name = "Student_Profiles"
        verbose_name_plural = "Student_Profiles"

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Note_Title = models.CharField(max_length=256)
    Note_Description = models.TextField(max_length=4096)
    Note_Document = models.FileField(upload_to='Notes_Documents',blank=True)

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.Note_Title

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Homework_Subject = models.CharField(max_length=50)
    Homework_Title = models.CharField(max_length=100)
    Homework_Description = models.TextField(blank=True)
    Homework_Due = models.DateTimeField(blank=True)
    Homework_Finished = models.BooleanField(default=False)


    def __str__(self):
        return self.Homework_Title


class Todo(models.Model):
    Todo_User = models.ForeignKey(User, on_delete=models.CASCADE)
    Todo_Title = models.CharField(max_length=254)
    Todo_Finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todo"

    def __str__(self):
        return self.Todo_Title
