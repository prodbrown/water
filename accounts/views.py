from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import CustomUser
from django.http import HttpResponse
import csv
from django.contrib.auth import get_user_model
from .utils import add_message  # Import the utility function

CustomUser = get_user_model()

def handle_error(request, error_message):
    add_message(request, 'error', error_message)  # Use the utility function
    return render(request, 'error.html', {'error_message': error_message})

def default_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/default.html')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            add_message(request, 'success', 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            add_message(request, 'error', 'Error creating account. Please check your input.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                add_message(request, 'success', 'Logged in successfully!')
                return redirect('dashboard')
            else:
                add_message(request, 'error', 'Invalid email or password')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    add_message(request, 'success', 'You have successfully logged out.')
    return redirect('default')

@login_required
@user_passes_test(lambda u: u.is_serviceprovider)
def list_users(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.all()
    
    if query:
        users = users.filter(email__icontains=query)

    return render(request, 'accounts/list_users.html', {'users': users, 'query': query})

@login_required
@user_passes_test(lambda u: u.is_serviceprovider)
def promote_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        try:
            if user.is_customer:
                user.is_serviceprovider = True
                user.is_customer = False
                add_message(request, 'success', f'{user} has been promoted to Service Provider.')
            elif user.is_serviceprovider:
                user.is_customer = True
                user.is_serviceprovider = False
                add_message(request, 'success', f'{user} has been demoted to Customer.')

            user.save()
            return redirect('list_users')
        except Exception as e:
            return handle_error(request, str(e))

    return render(request, 'accounts/promote_user.html', {'user': user})

@login_required
@user_passes_test(lambda u: u.is_serviceprovider)
def download_users(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'First Name', 'Last Name', 'Status'])

        users = CustomUser.objects.all()
        for user in users:
            status = 'Service Provider' if user.is_serviceprovider else 'Customer'
            writer.writerow([user.email, user.first_name, user.last_name, status])

        return response
    except Exception as e:
        return handle_error(request, str(e))




def about(request):
    return render(request, 'accounts/about.html')

def contact(request):
    return render(request, 'accounts/contact.html')