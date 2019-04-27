from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.db import connection


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

            return redirect('accounts:signup2')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signup2(request):
    if request.method == 'POST':
        age = request.POST['age']
        # profilePic = request.POST['profilePic']
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO accounts_profile(age,user_id)
                VALUES(%s,%s);
            ''',[age,request.user.id])
        return redirect('/')
    else:
        return render(request, 'accounts/signup2.html', {})
