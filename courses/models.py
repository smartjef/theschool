from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os
# Create your models here.

import os

class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='courses' ,null=True, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def save_subject_image(instance, filename):
    upload_to = "Images/"
    ext = filename.split('.')[-1]

    if instance.subject_id:
        filename = 'Subject_Picture/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)

class Subject(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    subject_id = models.CharField(max_length=100, unique=True)
    name=models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name= 'Subject Image')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]

    if instance.lesson_id:
        filename = 'lesson_file/{}/{}.{}'.format(instance.lesson_id, instance.lesson_id,exit)

        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(instance.lesson_id, new_name, ext)
    return os.path.join(upload_to, filename)

class Lesson(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE) 
    lesson_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE, related_name = 'lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name = 'Chapter no. ')
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files, verbose_name='Video', blank=True, null=True)
    ppt = models.FileField(upload_to=save_lesson_files, verbose_name='Presentation', blank=True, null=True)
    Notes = models.FileField(upload_to=save_lesson_files, verbose_name='Notes', blank=True, null=True)
    d_notes = models.TextField(blank=True, null=True, verbose_name='d_notes')
    code = models.TextField(blank=True, null=True, editable=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=save_lesson_files, verbose_name='image', blank=True, null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('lesson_list', kwargs={'slug': self.subject.slug, 'standard':self.standard.slug})

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE, related_name='comments') 
    comm_name = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-"+str(self.author)+ str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)

class WorkingDays(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_days')
    day = models.CharField(max_length=100)
    def __str__(self):
        return self.day

class TimeSlots(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time) 

class SlotSubject(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_slots')
    day = models.ForeignKey(WorkingDays, on_delete=models.CASCADE,related_name='standard_slots_days')
    slot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,related_name='standard_slots_time')
    slot_subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='standard_slots_subject')

    def __str__(self):
        return str(self.standard)+ ' - ' + str(self.day) + ' - ' + str(self.slot) + ' - ' + str(self.slot_subject)

