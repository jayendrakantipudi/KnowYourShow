from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm



def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # age=request.POST['age']
            # print(age)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})
