from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from account.forms import RejestracjaForm, LoginForm, ZaktualizujKontoForm
# Create your views here.
from grzyb.models import BlogPost

def registration_view(request):
    context = {}
    if request.POST:
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username= username, password = raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RejestracjaForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context['login_form'] = form
    return render (request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}

    if request.POST:
        form = ZaktualizujKontoForm(request.POST, instance = request.user)
        if form.is_valid():
            form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Zaktualizowano dane"
    else:
        form = ZaktualizujKontoForm(
                initial = {
                    "email": request.user.email,
                    "username": request.user.username
                }
            )
    context['account_form'] = form

    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts
    return render(request, 'account/account.html', context)

def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html',{})