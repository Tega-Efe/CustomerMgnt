# from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.shortcuts import render,redirect

from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from . forms import *
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users,admin_only


@unauthenticated_user
def registerPage(request):
			
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			# group = Group.objects.get(name='customer')
			# user.groups.add(group)

			# Customer.objects.create(user=user,name=username)

			messages.success(request, 'Account was created for' +  username )

			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user = authenticate(request, username=username, password= password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username OR password is incorrect')
			

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def createcustomer(request):
    action = 'create'
    form = createCustomerForm()

    if request.method == 'POST':
        form = createCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context =  {'action': action, 'form': form}
    return render(request, 'accounts/create_customer.html', context)
      

#-------------------(DETAIL/LIST VIEWS) -------------------
@login_required(login_url='login')
@admin_only
def dashBoard(request):
	# .order_by('-status')[0:5]
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()


	# total_orders = Order.objects.all().count()
	# delivered = Order.objects.filter(status='Delivered').count()
	# pending = Order.objects.filter(status='Pending').count()

	context = {'customers':customers, 'orders':orders,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}

	return render(request, 'accounts/dashBoard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders': orders,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance= customer)
		if form.is_valid():
			form.save()

	context = {'form': form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()


	orderFilter = OrderFilter(request.GET, queryset=orders) 
	orders = orderFilter.qs

	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
	'filter':orderFilter}
	return render(request, 'accounts/customer.html', context)


#-------------------(CREATE VIEWS) -------------------
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request):
    action = 'create'
    if request.user.groups.filter(name='admin').exists():
        form = createOrderForm(request.POST)
        redirect_url = 'dashboard'
    else:
        form = createOrderForm(request.POST or None, user=request.user)
        redirect_url = 'user_page'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(redirect_url)

    context = {'action': action, 'form': form}
    return render(request, 'accounts/order_form.html', context)



#-------------------(UPDATE VIEWS) -------------------
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])

def updateOrder(request, pk):
    action = 'update'
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if request.user.groups.filter(name='admin').exists():
                return redirect('/customer/' + str(order.customer.id))
            else:
                return HttpResponseRedirect(reverse('user_page'))

    context =  {'action': action, 'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProduct(request):
    action = 'create'
    form = AddProductForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('products')

    context =  {'action': action, 'form': form}
    return render(request, 'accounts/products_form.html', context)




#-------------------(DELETE VIEWS) -------------------
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def deleteOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	if request.method == 'POST':
# 		customer_id = order.customer.id
# 		customer_url = '/customer/' + str(customer_id)
# 		order.delete()
# 		return redirect(customer_url)
		
# 	return render(request, 'accounts/delete_item.html', {'item':order})



def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        customer_id = order.customer.id
        customer_url = '/customer/' + str(customer_id)
        order.delete()
        if request.user.groups.filter(name='admin').exists():
            return HttpResponseRedirect(customer_url)
        else:
            return HttpResponseRedirect(reverse('user_page'))
    
    return render(request, 'accounts/delete_item.html', {'item': order})
