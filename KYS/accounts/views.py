from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    # Create your views here.
    if request.method=='POST':
        print(1)
        form=SignUpForm(request.POST,request.FILES)
        if form.is_valid():

            username=form.cleaned_data.get('username')
            print(username)
            raw_password=form.cleaned_data.get('password1')
            print(raw_password)
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            new_user.refresh_from_db()  # load the profile instance created by the signal
            new_user.save()
            age = form.cleaned_data.get('age')
            picture = form.cleaned_data.get('picture')
            Profile=Profile()
            Profile.user = new_user
            if picture:
                Profile.picture = picture
            Profile.age=age
            Profile.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
