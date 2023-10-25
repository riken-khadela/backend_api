from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Registration view
def register(request):
    if request.method == 'POST': 
        ...
        # Handle registration form submission here
        # Generate email verification code and send it to the user
    else:
        # Render the registration form
        return render(request, 'registration/register.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the user's dashboard or another protected page
            else:
                # Handle invalid login
                ...
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Create HTML templates for the registration and login forms.
