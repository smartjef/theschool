from django.db import models
from django.contrib.auth.models import User
import os
from django.urls import reverse
# Create your models here.

def path_and_rename(instance, filename):
    upload_to = 'users_images/'
    ext = filename.split('.')[-1]

    if instance.user.username:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


    
class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    profile_Pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", default="undraw_profile.svg")

    teacher = 'teacher'
    student = 'student'
    parent = 'parent'

    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        (parent, 'parent'),
    ]
    user_type = models.CharField(max_length=20, choices=user_types, default=student)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')