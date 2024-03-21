from django.db import models
from django import forms
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save




# 病院情報を格納するためのデータモデルを定義
class Department(models.Model):
    name = models.CharField(max_length=100)  # 診療科名

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=100)  # 病院名
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department, related_name='hospitals')  # 診療科との多対多の関係
    is_primary_care = models.BooleanField(default=False)  # プライマリケアの提供有無
    is_favorite = models.BooleanField(default=False)  # お気に入りの状態

    def __str__(self):
        return self.name
        
class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'department', 'departments', 'is_primary_care']
        widgets = {'departments': forms.CheckboxSelectMultiple}

class YourModelForm(forms.ModelForm):
    pass



# 薬
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    effect = models.CharField(max_length=255, default='No effect provided')
    hospital = models.CharField(max_length=100, default='Default Hospital')


    def __str__(self):
        return self.name
    


# カレンダー
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    description = models.TextField(default='')

    def __str__(self):
        return self.description

class AnotherModel(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
