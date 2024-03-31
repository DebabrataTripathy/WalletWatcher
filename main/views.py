from django.shortcuts import render,redirect
from.forms import InputForm,RegistrationForm
from.models import Expense
import datetime
from django.contrib.auth import logout as auth_logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid:
            add=form.save(commit=False)
            password=add.set_password(form.cleaned_data['password'])
            print(password)
            add.save()
            return redirect('login')
    else:
        form=RegistrationForm()
    return render(request,'main/register.html',{'form':form})

def logout(request):
    auth_logout(request)
    return redirect('login')
@login_required
def index(request):
    if request.method=="POST":
        form=InputForm(data=request.POST)
        if form.is_valid:
            add=form.save(commit=False)
            add.user=request.user
            add.save()
            form.clean()
    expense=Expense.objects.filter(user=request.user)
    sum=0
    for item in expense:
        sum+=item.price
    last_year=datetime.date.today()-datetime.timedelta(days=365)
    data_last_year=Expense.objects.filter(user=request.user,date__gt=last_year)
    sum1=0
    for item in data_last_year:
        sum1+=item.price

    last_month=datetime.date.today()-datetime.timedelta(days=30)
    data_last_month=Expense.objects.filter(user=request.user,date__gt=last_month)
    sum2=0
    for item in data_last_year:
        sum2+=item.price
    last_week=datetime.date.today()-datetime.timedelta(days=7)
    data_last_month=Expense.objects.filter(user=request.user,date__gt=last_week)
    sum3=0
    for item in data_last_year:
        sum3+=item.price
    daily_sum=Expense.objects.filter(user=request.user).values('date').order_by('date').annotate(sum=Sum('price'))
    print(daily_sum)
    category_sum=Expense.objects.filter(user=request.user).values('category').order_by('category').annotate(sum=Sum('price'))
    print(category_sum)
    form=InputForm()
    return render(request,'main/index.html',{"form":form,'expenses':expense,'sum':sum,'sum1':sum1,"sum2":sum2,"sum3":sum3,'daily_sum':daily_sum,"category_sum":category_sum})

def edit(request,id):
    if request.method=="POST":
        form=InputForm(request.POST,instance=Expense.objects.get(pk=id))
        if form.is_valid:
            form.save()
            return redirect('index')
    else:
        form=InputForm(instance=Expense.objects.get(pk=id))
    return render(request,"main/edit.html",{'form':form})

def delete(request,id):
    obj=Expense.objects.get(pk=id)
    obj.delete()
    return redirect('index')