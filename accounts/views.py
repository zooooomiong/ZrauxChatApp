from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from accounts.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UserSignupForm , LoginForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from .tasks import send_code_via_email



def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()
            user.create_code()
            
            send_code_via_email.delay(user.id)
            
            return redirect("confirm_email")
        else:
            messages.error(request, form.errors)

    else:
        form = UserSignupForm()
        
    return render(request, 'signup.html', {'form': form})


def confirm_email(request):
    if request.method == "POST":
        code = request.POST.get("code")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
            
            if user.check_password(password) and user.confirm_code == code:
                user.confirm_email = True
                user.is_active = True
                user.save()
                messages.success(request, "Your email has been confirmed successfully.")
                return JsonResponse({"status": "success", "message": "Email confirmed. Redirecting..."})
            else:
                return JsonResponse({"status": "error", "message": "Invalid credentials or confirmation code."}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User does not exist."}, status=404)

    return render(request, 'confirm_email.html')

def email_confirmed_view(request):
    return render(request, 'email_confirmed.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    if not user.confirm_email:
                        # Resend confirmation code and redirect to confirm_email page
                        user.create_code()  # Create a new confirmation code
                        send_code_via_email.delay(user.id)  # Send the confirmation email
                        messages.warning(request, "Your email is not confirmed. We've sent a confirmation code to your email.")
                        return redirect("confirm_email")
                    else:
                        # Log the user in if email is confirmed
                        login(request, user)
                        return redirect("home")
                else:
                    messages.error(request, "Invalid username or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
@login_required
def logout_view(request):
    if request.method == "POST":
        if request.POST.get("logout"):
            logout(request)
            return JsonResponse({"logout":"done"})
        return JsonResponse({"logout":"failed"})
    
    return render(request, "logout.html")

