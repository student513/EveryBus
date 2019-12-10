from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import password_validation
from .models import Profile
#from phonenumber_field.formfields import PhoneNumberField
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20, label="아이디")
    #email = forms.EmailField(max_length=64, label="이메일")


    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        #help_text="Enter the same password as before, for verification.",
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username',  'password1','password2',
        #'email',
        ]

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone',]
        widgets ={
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'숫자만 입력해주세요'})
        }
        labels ={
            'phone': '연락처',
        }
    bookmark={}
    bookkey=[]

    def push(self, key, value):
        self.bookmark[key] = value
        self.bookkey.append(key)
    def pop(self, key):
        del self.bookmark[key]
        self.bookkey.remove(key)
    
    stopbookmark={}
    stopbookkey=[]

    def stoppush(self, key, value):
        self.stopbookmark[key] = value
        self.stopbookkey.append(key)
    def stoppop(self,key):
        del self.stopbookmark[key]
        self.stopbookkey.remove(key)
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        
class CustomUserChangeForm(UserChangeForm):
    phone = forms.CharField(
        label="연락처",
        )
    class Meta:
        model = Profile
        fields = ['phone',]