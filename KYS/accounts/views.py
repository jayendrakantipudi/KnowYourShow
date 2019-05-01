from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.db import connection
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage





def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            # message = "hi"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # new_user = authenticate(username=form.cleaned_data['username'],
            #                         password=form.cleaned_data['password1'],
            #                         )
            # login(request, new_user)

            # return redirect('accounts:signup2')
            return HttpResponse('Please confirm your email address to complete the registration')
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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('accounts:signup2')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
