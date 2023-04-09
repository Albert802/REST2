from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from . models import *
from .forms import OrderForm,CreateUserForm,CustomerForm,CreateProductForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login ,authenticate,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()


    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context ={
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending


    }
    return render(request,'accounts/user.html',context)

@login_required(login_url='login')
def registerPage(request):


    form = CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')





            messages.success(request,'Congrats!! Account was created for '+ username)
            return redirect('accounts:login')


    context = {'form':form}
    return render(request,'accounts/register.html',context)


def loginPage(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
           username=request.POST.get('username')
           password=request.POST.get('password')

           user = authenticate(request,username=username,password=password)

           if user is not None:
               login(request,user)
               return redirect('accounts:home')
           else:
                messages.info(request,'Username or Password is incorrect')



    return render(request,'accounts/login2.html',context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


@admin_only
#@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context ={
        'orders': orders,
        'customer': customer,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered ':delivered ,
        'pending':pending
    }


    return render(request,'accounts/dashboard2.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):

    customer = Customer.objects.get(id=pk_test)
    order = customer.order_set.all()
    order_count = order.count()

    myFilter = OrderFilter(request.GET ,queryset=order)
    order= myFilter.qs


    context = {
        'customer':customer,
        'order':order,
        'order_count':order_count,
        'myFilter': myFilter,
    }

    return render(request,'accounts/customer2.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Product.objects.all()
    return render(request,'accounts/products2.html',{'product':product})

@login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order, fields=('product','status'))
    customer = Customer.objects.get(id=pk)
    form = OrderFormSet(instance= customer)


    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        form = OrderFormSet(request.POST ,instance= customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form,'customer':customer}

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')




    context= {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request,'accounts/delete.html',context)

@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer

    cusform = CustomerForm(instance=customer)
    if request.method == 'POST':
        cusform= CustomerForm(request.POST,request.FILES,instance=customer)
        if cusform.is_valid():
            cusform.save()


    context ={'cusform':cusform}
    return render(request,'accounts/acccount_settings.html',context)

def createProduct(request):
    form = CreateProductForm()

    if request.method== 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context ={
        'form':form
    }
    return render(request,'accounts/create_product.html',context)