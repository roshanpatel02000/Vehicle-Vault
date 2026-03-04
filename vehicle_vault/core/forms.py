from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'dark-input',
            'placeholder': 'Create a password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'dark-input',
            'placeholder': 'Repeat your password',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'dark-input',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'dark-input',
                'placeholder': 'Last Name',
            }),
            'gender': forms.Select(attrs={
                'class': 'dark-input',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'dark-input',
                'placeholder': 'you@example.com',
            }),
            'role': forms.Select(attrs={
                'class': 'dark-input',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if user.role == "Admin":
            user.is_staff = True
            user.is_admin = True
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'dark-input',
            'placeholder': 'you@example.com',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'dark-input',
            'placeholder': '••••••••',
        })
    )


class OTPVerifyForm(forms.Form):
    code = forms.CharField(
        label='OTP Code',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'dark-input otp-input',
            'placeholder': '000000',
            'maxlength': '6',
            'autofocus': True,
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        if not code.isdigit():
            raise forms.ValidationError('OTP must contain only digits.')
        return code


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'dark-input',
            'placeholder': 'you@example.com',
        })
    )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'dark-input',
            'placeholder': 'Enter new password',
        })
    )
    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'dark-input',
            'placeholder': 'Repeat new password',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data