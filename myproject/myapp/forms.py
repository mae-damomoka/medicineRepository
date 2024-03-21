from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hospital, Department
from .models import Event


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={'autocomplete': 'username'})  # autocomplete属性を追加
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})  # autocomplete属性を追加
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})  # autocomplete属性を追加
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class HospitalForm(forms.ModelForm):
    department_name = forms.CharField(max_length=100)  # ユーザー入力用のカスタムフィールドを追加

    class Meta:
        model = Hospital
        fields = ['name']  # 'department_name'は除外

    def save(self, commit=True):
        hospital = super().save(commit=False)
        department_name = self.cleaned_data['department_name']
        department, created = Department.objects.get_or_create(name=department_name)
        hospital.department = department
        if commit:
            hospital.save()
        return hospital
    
class YourForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User 
        fields = ("username", "email", "password1", "password2")  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'description'] 