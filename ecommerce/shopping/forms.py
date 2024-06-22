from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+?1?\d{9,15}$'
password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'


class CustomerRegistration(UserCreationForm):
    email = forms.CharField(label='Email Address', required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
                            validators=[
                                RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password', 'class': 'form-control'}), validators=[
        RegexValidator(regex=password_pattern,
                       message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Retype Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already taken.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(CustomerRegistration, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])  # Set hashed password
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()
            # Assign user to a group (You can replace 'my_group_name' with your desired group name)
            # group = Group.objects.get(name='user_person')
            # user.groups.add(group)
        else:
            print("User not created.")
        print(user)
        return user


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Email Address', required=True,
                widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}),
                validators=[RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    password = forms.CharField(label=_('Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

    # def clean_email(self):
    #     username = self.cleaned_data.get('username')
    #     if not User.objects.filter(username__iexact=username).exists():
    #         raise ValidationError("This email is already taken.")
    #     return username


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control', 'autofocus': 'True'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html(), validators=[
        RegexValidator(regex=password_pattern, message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    new_password2 = forms.CharField(label=_('Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))

    def clean_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Passwords do not match")
        return new_password2


class UserPasswordReset(PasswordResetForm):
    email = forms.EmailField(label=_('Email Address'), max_length=255, required=True,
             widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}),
             validators=[RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])


class UserSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": _("The confirm password doesn't match with new password."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class UserProfileView(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileView, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone'].required = True
        self.fields['city'].required = True
        self.fields['zipcode'].required = True
        self.fields['state'].required = True
        self.fields['locality'].required = True
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'locality', 'city', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Your Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Khurja'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '123456'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }