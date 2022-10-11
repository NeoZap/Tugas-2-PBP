from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render
from todolist.models import Task
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, models;
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import TaskForm

@login_required(login_url='/todolist/login/')
def show_todolist(request):
    user = request.user
    context = {
        "todo_list": Task.objects.filter(user=user),
        "name": user.username,
    }
    return render(request, 'todolist.html', context=context)

@login_required(login_url='/todolist/login/')
def change_task(request, task_id):
    task = Task.objects.filter(user=request.user).get(id=task_id)
    task.is_finished = not task.is_finished
    task.save()
    return redirect('todolist:show_todolist')

@login_required(login_url='/todolist/login/')
def delete_task(request, task_id):
    task = Task.objects.filter(user=request.user).get(id=task_id)
    task.delete()
    return redirect('todolist:show_todolist')

@login_required(login_url='/todolist/login/')
def create_task(request):
    form = TaskForm();
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.create(user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            task.save()
            return redirect('todolist:show_todolist')
    return render(request, "create_task.html", {"form" : form})

# src: https://stackoverflow.com/questions/42546006/deleting-clearing-django-contrib-messages
def delete_messages(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass

def register(request):
    form = UserCreationForm()
    form_errors = ""

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            delete_messages(request)
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
        else:
            form_errors = form.errors
            form_errors = form_errors.get('password2')
            if form_errors:
                form_errors = form_errors.as_data()
                form_errors = "".join([str(error) for error in form_errors])
                form_errors = [errors for errors in form_errors.split("'") if '[' not in errors and ']' not in errors]
            else:
                messages.error(request, 'Akun gagal dibuat!')
    
    context = {'form':form, 'messages': form_errors}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    return response
