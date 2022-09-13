from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm


def signup_view(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        # refresh_from_db() method  handle synchronism issue, basically reloading the database after the signal
        user.refresh_from_db()
        # choosing the default for the first sign in, afterward user can change his profile photo manually.
        user.profile_avatar = 'default/img_avatar.png'
        user.save()
        # cleaned_data is holding the validated form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        # authenticate() method takes credentials as keyword arguments
        user = authenticate(username=username, password=password)
        # login() method takes an HttpRequest object and a User object and saves the user’s ID in the session
        login(request, user)
        # clear guest session except for shopping cart session
        request.session['guest_data'].clear()
        return redirect('homepage')
    else:
        form = SignupForm()
    return render(request, 'account/signupview.html', {'form': form})
