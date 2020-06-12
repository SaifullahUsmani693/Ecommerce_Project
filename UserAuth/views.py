from django.shortcuts import render, redirect

# Auth Forms (Login.Logout,Signin,Signout)
from django.contrib.auth.forms import UserCreationForm
# Customized Auth Forms As Needed
from .forms import UserRegistrationForm

# Messages For Inforamtion
from django.contrib import messages

# Blockers For Privacy
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account has been created for {username}!')

            return redirect('login')
        else:
            messages.error(
                request, f'Username or Password is incorrect!')

    else:

        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)
