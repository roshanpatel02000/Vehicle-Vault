from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserLoginForm, OTPVerifyForm, ForgotPasswordForm, ResetPasswordForm
from .models import User, OTPCode
from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(user, purpose):
    """Generate OTP, save it, and email it to the user."""
    # Invalidate existing unused OTPs for the same user+purpose
    OTPCode.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

    code = OTPCode.generate_code()
    OTPCode.objects.create(user=user, code=code, purpose=purpose)

    purpose_labels = {
        'signup': 'Sign Up Verification',
        'login': 'Login Verification',
        'reset': 'Password Reset',
    }
    subject = f"Vehicle Vault – Your {purpose_labels.get(purpose, 'OTP')} Code"
    message = (
        f"Hello {user.first_name or user.email},\n\n"
        f"Your 6-digit verification code is: {code}\n\n"
        f"This code is valid for 2 minutes. Do not share it with anyone.\n\n"
        f"— Vehicle Vault Team"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
    return code


# ─── Signup ───────────────────────────────────────────────────────────────────

@ensure_csrf_cookie
def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Store signup data in session temporarily (user not created yet)
            request.session['signup_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'gender': form.cleaned_data['gender'],
                'email': form.cleaned_data['email'],
                'role': form.cleaned_data['role'],
                'password': form.cleaned_data['password1'],
            }
            # Check if email is already taken
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'An account with this email already exists.')
                return render(request, 'core/signup.html', {'form': form})

            # Create a temporary inactive user to attach OTP to
            temp_user, created = User.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'gender': form.cleaned_data['gender'],
                    'role': form.cleaned_data['role'],
                    'is_active': False,
                }
            )
            if created:
                temp_user.set_password(form.cleaned_data['password1'])
                if form.cleaned_data['role'] == "Admin":
                    temp_user.is_staff = True
                    temp_user.is_admin = True
                temp_user.save()

            send_otp_email(temp_user, 'signup')
            request.session['otp_email'] = form.cleaned_data['email']
            request.session['otp_purpose'] = 'signup'
            messages.info(request, f"A 6-digit OTP has been sent to {form.cleaned_data['email']}.")
            return redirect('verify_otp')
    else:
        form = UserSignupForm()
    return render(request, 'core/signup.html', {'form': form})


# ─── Login ────────────────────────────────────────────────────────────────────

@ensure_csrf_cookie
def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                # Block unapproved Admins
                if user.role == 'Admin' and not user.is_approved:
                    return render(request, 'core/login.html', {
                        'form': form,
                        'error': 'Your Admin account is pending approval and cannot log in yet.'
                    })
                    
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('admin_dashboard' if user.role == 'Admin' else 'user_dashboard')
            else:
                return render(request, 'core/login.html', {
                    'form': form,
                    'error': 'Invalid email or password.'
                })
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})


def userLogoutView(request):
    logout(request)
    return redirect('login')


# ─── OTP Verification ─────────────────────────────────────────────────────────

@ensure_csrf_cookie
def verifyOtpView(request):
    email = request.session.get('otp_email')
    purpose = request.session.get('otp_purpose')

    if not email or not purpose:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('login')

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            try:
                user = User.objects.get(email=email)
                otp = OTPCode.objects.filter(
                    user=user,
                    code=entered_code,
                    purpose=purpose,
                    is_used=False
                ).latest('created_at')

                if otp.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return render(request, 'core/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})

                # Mark OTP as used
                otp.is_used = True
                otp.save()

                if purpose == 'signup':
                    # Activate user
                    user.is_active = True
                    if user.role != 'Admin':
                        user.is_approved = True
                    user.save()
                    
                    # Clean session
                    request.session.pop('otp_email', None)
                    request.session.pop('otp_purpose', None)
                    request.session.pop('signup_data', None)
                    
                    if user.role == 'Admin' and not user.is_approved:
                        messages.warning(request, f'Registration successful, {user.first_name or user.email}. An active Admin must approve your account before you can log in.')
                        return redirect('login')

                    login(request, user)
                    messages.success(request, f'Welcome to Vehicle Vault, {user.first_name or user.email}!')
                    # Send welcome email
                    from django.core.mail import send_mail
                    from django.template.loader import render_to_string
                    from django.conf import settings
                    
                    subject = 'Welcome to Vehicle Vault!'
                    text_content = f'Hi {user.first_name or user.email},\n\nYour account has been successfully created. Welcome aboard!\n\n— Vehicle Vault Team'
                    site_url = request.build_absolute_uri('/')[:-1] # Remove trailing slash
                    
                    try:
                        html_content = render_to_string('core/emails/welcome.html', {
                            'name': user.first_name or user.email.split('@')[0],
                            'email': user.email,
                            'role': user.role,
                            'site_url': site_url,
                        })
                        
                        send_mail(
                            subject,
                            text_content,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            html_message=html_content,
                            fail_silently=True,
                        )
                    except Exception as e:
                        pass # Silently proceed if welcome email fails, so user still logs in
                        
                    return redirect('admin_dashboard' if user.role == 'Admin' else 'user_dashboard')

                elif purpose == 'login':
                    login(request, user)
                    request.session.pop('otp_email', None)
                    request.session.pop('otp_purpose', None)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('admin_dashboard' if user.role == 'Admin' else 'user_dashboard')

                elif purpose == 'reset':
                    # Store email in session for the reset step
                    request.session['reset_email'] = email
                    request.session.pop('otp_email', None)
                    request.session.pop('otp_purpose', None)
                    messages.success(request, 'OTP verified! Please set your new password.')
                    return redirect('reset_password')

            except OTPCode.DoesNotExist:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'core/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})
    else:
        form = OTPVerifyForm()

    return render(request, 'core/verify_otp.html', {'form': form, 'email': email, 'purpose': purpose})


@ensure_csrf_cookie
def resendOtpView(request):
    email = request.session.get('otp_email')
    purpose = request.session.get('otp_purpose')
    if not email or not purpose:
        messages.error(request, 'Session expired.')
        return redirect('login')
    try:
        user = User.objects.get(email=email)
        send_otp_email(user, purpose)
        messages.success(request, f'A new OTP has been sent to {email}.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('verify_otp')


# ─── Forgot / Reset Password ──────────────────────────────────────────────────

@ensure_csrf_cookie
def forgotPasswordView(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_otp_email(user, 'reset')
                request.session['otp_email'] = email
                request.session['otp_purpose'] = 'reset'
                messages.info(request, f'A 6-digit OTP has been sent to {email}.')
                return redirect('verify_otp')
            except User.DoesNotExist:
                # Don't reveal if email exists or not (security)
                messages.info(request, f'If an account with {email} exists, an OTP has been sent.')
                return redirect('forgot_password')
    else:
        email_prefill = request.GET.get('email', '')
        form = ForgotPasswordForm(initial={'email': email_prefill})
    return render(request, 'core/forgot_password.html', {'form': form})


@ensure_csrf_cookie
def resetPasswordView(request):
    reset_email = request.session.get('reset_email')
    if not reset_email:
        messages.error(request, 'Session expired. Please start the password reset again.')
        return redirect('forgot_password')

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=reset_email)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                request.session.pop('reset_email', None)
                messages.success(request, 'Password reset successfully! Please log in with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('forgot_password')
    else:
        form = ResetPasswordForm()
    return render(request, 'core/reset_password.html', {'form': form})


# ─── Profile Settings ─────────────────────────────────────────────────────────

@login_required(login_url='login')
def profileSettingsView(request):
    return render(request, 'core/profile_settings.html', {'user': request.user})
