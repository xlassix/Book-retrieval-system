from django import forms
from .core import EmailBackend
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator,ProhibitNullCharactersValidator
#password = RegexValidator('((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,8})', "Your string should contain letter A in it.")

contain_num = RegexValidator(r'(?=.*\d)','must contain at least one digit',code='invalid')
contain_upper = RegexValidator( r'(?=.*[A-Z])','must contain at least one uppercase character',code='invalid')
contain_symbols = RegexValidator(r'(?=.*\W)','must contain at least one special symbol',code='invalid')
Users=EmailBackend()
def validate_email(value):
    if Users.check_user(username=value):
        raise ValidationError("Email address already exist",code="not unique")
def validate_matric(value):
    if Users.check_user(username=value):
        raise ValidationError("Account already exist",code="not unique")       
class Registration_Test_form(forms.Form):
    username = forms.CharField(validators=[validate_matric,ProhibitNullCharactersValidator],label='username', max_length=50,widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Matric"}))
    email = forms.EmailField(validators=[validate_email],label='email', max_length=50,widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    first_name = forms.CharField(label='first name', max_length=30,widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"First Name"}))
    last_name = forms.CharField(label='last name', max_length=30, widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Last Name"}))
    password = forms.CharField(validators=[contain_num,contain_symbols,contain_upper,ProhibitNullCharactersValidator],label='password',min_length=8, max_length=30,widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Password"}))
    password2 = forms.CharField(label='password2',min_length=8, max_length=30, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Confirm Password"}))

    def clean(self):
        cleanedData= super(Registration_Test_form, self).clean()
        password = cleanedData.get('password')
        password2 = cleanedData.get('password2')
        if password and password2:
            if password != password2:
                raise forms.ValidationError("The two password fields must match.")
        return cleanedData

    def get_data(self):
        data=super(Registration_Test_form, self).clean()
        data.pop("password2")
        password=data.pop('password')
        username=data.pop('username')
        email=data.pop('email')
        return [email,username,password,data]
    register=True

class Login_form(forms.Form):
    username = forms.CharField(validators=[ProhibitNullCharactersValidator],label='username', max_length=50,widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Email or Matric"}))
    password = forms.CharField(validators=[ProhibitNullCharactersValidator],label='password',min_length=8, max_length=30,widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Password"}))
    register=False
    def get_data(self):
        data=super(Login_form, self).clean()
        return data

class Change_password_form(forms.Form):
    password = forms.CharField(validators=[ProhibitNullCharactersValidator],label='password', max_length=30, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Old Password"}))
    password1 = forms.CharField(validators=[contain_num,contain_symbols,contain_upper,ProhibitNullCharactersValidator],label='password1',min_length=8, max_length=30,widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Password"}))
    password2 = forms.CharField(validators=[ProhibitNullCharactersValidator],label='password2', max_length=30, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Confirm Password"}))
    change_password=True


    def clean(self):
        cleanedData= super(Change_password_form, self).clean()
        password1 = cleanedData.get('password1')
        password2 = cleanedData.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields must match.")
        return cleanedData

    def get_data(self):
        data=super(Change_password_form, self).clean()
        return data