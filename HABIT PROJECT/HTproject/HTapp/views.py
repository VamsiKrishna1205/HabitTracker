from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import HT
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        email = request.POST.get('email')  # Captures email if needed

        # Authenticate user
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)

            # Send a notification email after login
            if email:
                send_mail(
                    subject="Incomplete Habit Notification",
                    message="Your task is incomplete. Please complete the Habit, if you have completed the tasks just ignor this message ",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )

            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'HTapp/login.html')


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_HT = HT(user=request.user, HT_name=task)
        new_HT.save()
        
    all_Hts = HT.objects.filter(user=request.user)
    context = {
        'Hts' : all_Hts
    }
    # return render(request, 'HTapp/HT.html')
    return render(request, 'HTapp/HT.html', context)




def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 3:
            messages.error(request, "Password should be at least 3 (or) more characters long")
            return redirect('register')
        
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, "User already exists, choose another username")
            return redirect('register')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User successfully created account, login now')
        return redirect('login')
    return render(request, 'HTapp/register.html')

def Logoutview(request):
    logout(request)
    return redirect('login')

@login_required
def delete_habit(request, habit_name):
    try:
        habit = HT.objects.get(user=request.user, HT_name=habit_name)
        habit.delete()
        messages.success(request, f"Habit '{habit_name}' deleted successfully!")
    except HT.DoesNotExist:
        messages.error(request, f"Habit '{habit_name}' does not exist!")
    return redirect('home')

from django.shortcuts import redirect
from .models import HT


@login_required
def update_habit(request, habit_name):
    try:
        habit = HT.objects.get(user=request.user, HT_name=habit_name)
        habit.status = True  # Update the status to 'Completed'
        habit.save()
        messages.success(request, f"Habit '{habit_name}' marked as completed!")
    except HT.DoesNotExist:
        messages.error(request, f"Habit '{habit_name}' does not exist!")
    return redirect('home')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HT


@login_required
def edit_habit(request, habit_name):
    try:
        habit = HT.objects.get(user=request.user, HT_name=habit_name)
        if request.method == 'POST':
            new_name = request.POST.get('new_name')
            if new_name:
                habit.HT_name = new_name
                habit.save()
                messages.success(request, f"Habit renamed to '{new_name}'!")
                return redirect('home')
            else:
                messages.error(request, "New name cannot be empty!")
        return render(request, 'HTapp/edit_habit.html', {'habit': habit})
    except HT.DoesNotExist:
        messages.error(request, f"Habit '{habit_name}' not found!")
        return redirect('home')
