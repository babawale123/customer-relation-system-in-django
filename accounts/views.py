from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *


# Create your views here.

def home(request):
	orders = Order.objects.all()
	customer = Customer.objects.all()


	total_customers = customer.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()



	context = {'order':orders, 'customer':customer,'total_orders':total_orders, 'delivered':delivered, 'pending':pending }

	return render(request, 'accounts/dashboard.html', context)


def products(request):
	products = Product.objects.all()
	return render(request,'accounts/product.html', {'products':products})

def customer(request, pk):
	customer = Customer.objects.get(id=pk)


	orders = customer.order_set.all()
	orders_count = orders.count()
 
	context = {'customer': customer, 'orders':orders, 'orders_count':orders_count}
	return render(request,'accounts/customer.html', context)

def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status' ), extra=10)
	customer = Customer.objects.get(id=pk)

	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})

	if request.method == 'POST':
		formset = OrderFormSet(request.POST,instance=customer)
		#form =OrderForm(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	

	context = {'formset':formset}

	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
		order = Order.objects.get(id=pk)
		form = OrderForm(instance=order)

		if request.method == 'POST':
			form =OrderForm(request.POST, instance=order)
			if form.is_valid():
				form.save()
				return redirect('/')

		context = {'form':form}
		return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'accounts/delete.html', context)