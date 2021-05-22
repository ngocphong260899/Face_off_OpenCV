from django.db import models

# Create your models here.
class Class(models.Model):
    name =  models.CharField(default='', max_length=255, null=False, unique=True)
class Subject(models.Model):
    name = models.CharField(default='', max_length=255, null=False, unique=True)
class User(models.Model):
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
class Student(models.Model):
    name = models.CharField(default='', max_length=255, null=False)
    birthday = models.DateField(null=False)
    msv = models.CharField(null=False, max_length=255, unique=True)
    address = models.CharField(default='', max_length=255)
    sex = models.BooleanField(default='')
    id_class = models.CharField(max_length=255,default='')
    id_subject = models.CharField(max_length=255,default='')
class Roll_up(models.Model):
    date = models.DateField(null=False)
    id_class = models.CharField(max_length=255)
    id_subject = models.CharField(max_length=255)
    id_student = models.CharField(max_length=255)
