from django.db import models
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import datetime

# Create your models here.


class FileUpModel(models.Model):
    file_name = models.CharField(max_length=100)
    upload_time = models.DateTimeField(default=datetime.now)
    upload_size = models.FloatField(default=0)
    upload_path = models.CharField(max_length=100, default='/')
    upload_group = models.CharField(max_length=50, default="")