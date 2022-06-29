from django.contrib import admin
from Dashboard.models import Student_Profile, Notes, Homework, Todo

# Register your models here.
admin.site.register(Student_Profile)
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
