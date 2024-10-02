from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import string
from django.utils.translation import gettext_lazy as _

def validate_password(password):
    if not password:
        raise ValidationError(_("Password is required."))
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))
    if not any(char.isdigit() for char in password):
        raise ValidationError(_("Password must contain at least one digit."))
    if not any(char.islower() for char in password):
        raise ValidationError(_("Password must contain at least one lowercase letter."))
    if not any(char.isupper() for char in password):
        raise ValidationError(_("Password must contain at least one uppercase letter."))
    if any(char.isspace() for char in password):
        raise ValidationError(_("Password must not contain any whitespace characters."))

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "password1",
            "placeholder": "Password"
        }),
        strip=False,
        help_text=_("Enter your password."),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "id": "password2",
            "placeholder": "Confirm Password"
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    field_order = ("username", "email", "password1", "password2")
    
    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
            }),
        }
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Enter a valid email address."))
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with this email already exists."))
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) >=3:
            return username
        raise ValidationError(_("username should be at leaset 3 charater"))
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords do not match."))
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)