from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_mine = True
            new_user.balance = 0
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('mine_mgt:dashboard')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
