from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Customer, category_master, Product, Cart, OrderPlaced
from .forms import CustomerRegistration, UserProfileView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# class based view
class HomeView(View):
    def get(self, request):
        topwear = Product.objects.filter(category_id='4')
        jeans = Product.objects.filter(category_id='1')
        mobile = Product.objects.filter(category_id='2')
        laptop = Product.objects.filter(category_id='3')
        context = {
            'topwear': topwear,
            'jeans': jeans,
            'mobile': mobile,
            'laptop': laptop
        }
        return render(request, 'shopping/home.html', context)


class ProductDetail(View):
    def get(self, request, prim_key):
        product = Product.objects.get(id=prim_key)
        return render(request, 'shopping/productdetail.html', {'product': product})

    def post(self, request, prim_key):
        if request.method == 'POST':
            user = request.user
            form_id = request.POST['form_id']
            product_id = request.POST.get('prod_id')
            print(user, form_id, product_id)
            product = Product.objects.get(id=product_id)

            # check product existance
            def product_in_cart(user, product):
                # Query the Cart model to check if the product exists for the user
                return Cart.objects.filter(user=user, product=product).exists()

            # Example usage:
            if form_id == 'add_to_cart':
                print(form_id)
                # user is the user instance and product is the product instance you want to check
                if product_in_cart(user, product):
                    messages.warning(request, 'The product already exists. You can increase their quantity.')
                else:
                    Cart(user=user, product=product).save()
                return redirect('add-to-cart')
            else:
                # user is the user instance and product is the product instance you want to check
                if product_in_cart(user, product):
                    messages.warning(request, 'The product already exists. You can buy it directly.')
                else:
                    Cart(user=user, product=product).save()
                return redirect('checkout')


def product(request, slug=None):
    cat_list = category_master.objects.all()
    if slug is None:
        pro_list = category_master.objects.all()
        products = Product.objects.all()
        category_data_slug = None
    else:
        category_data_slug = get_object_or_404(category_master, slug=slug)
        pro_list = category_master.objects.filter(slug=category_data_slug)
        products = Product.objects.filter(category=category_data_slug)
    data = {
        'cat_lists': cat_list,
        'pro_list': pro_list,
        'products': products
    }
    return render(request, 'shopping/mobile.html', data)


class Registration(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = CustomerRegistration()
            data = {
                'form': form
            }
            return render(request, 'shopping/customerregistration.html', data)
        else:
            return redirect('profile')

    def post(self, request):
        if not request.user.is_authenticated:
            form = CustomerRegistration(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You account has been successfully created.')
                form = CustomerRegistration()
            data = {
                'form': form
            }
            return render(request, 'shopping/customerregistration.html', data)
        else:
            return redirect('profile')


@login_required
def checkout(request):
    add = Customer.objects.filter(user=request.user)
    cart_list = [p for p in Cart.objects.filter(user=request.user)]
    amount = 0.0
    shipping_charge = 40.0
    total_amt = 0.0
    print(cart_list)
    if cart_list:
        for x in cart_list:
            temp_amt = x.quantity * x.product.discounted_price
            amount += temp_amt
            total_amt = amount + shipping_charge
        context = {
            'add': add,
            'total_amt': total_amt,
            'cart_lists': cart_list
        }
        return render(request, 'shopping/checkout.html', context)
    else:
        return redirect("product")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, id=None):
        if id is None:
            form = UserProfileView()
            data = {
                'form': form,
            }
        else:
            id = get_object_or_404(Customer, pk=id)
            form = UserProfileView(instance=id)
            data = {
                'form': form
            }
        return render(request, 'shopping/profile.html', data)

    def post(self, request, id=None):
        form = UserProfileView(request.POST)
        data = {
            'form': form,
        }
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            if id is None:
                messages.success(request, 'New address has been created...')
                address_data = Customer(user=user, name=name, phone=phone, locality=locality, city=city, zipcode=zipcode, state=state)
            else:
                add_id = get_object_or_404(Customer, pk=id)
                # we need add_id.id for getting the actual id in type string.
                cust_id = Customer.objects.get(Q(id=add_id.id) & Q(user=request.user)).id
                print(add_id, type(add_id), cust_id, type(cust_id))
                messages.success(request, 'Your Address has been updated...')
                address_data = Customer(id=cust_id, user=user, name=name, phone=phone, locality=locality, city=city, zipcode=zipcode, state=state)
            address_data.save()
            return redirect('address')
        return render(request, 'shopping/profile.html', data)


@login_required
def address(request):
    address_data = Customer.objects.all()
    data = {
        'address_data': address_data
    }
    if request.method == 'POST':
        add_id = request.POST.get('add_id')
        print(add_id)
        Customer(user=request.user, id=add_id).delete()
        messages.success(request, 'Address has been deleted...')
        return redirect('address')
    return render(request, 'shopping/address.html', data)


def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        print(cart_product)
        if cart_product:
            for product_amt in cart_product:
                tempamt = product_amt.quantity * product_amt.product.discounted_price
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
            return JsonResponse(data)


def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for product_amt in cart_product:
                tempamt = product_amt.quantity * product_amt.product.discounted_price
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
            return JsonResponse(data)


def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 40.0
        total_amt = 0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        print(prod_id, cart_product)
        if cart_product:
            for product_amt in cart_product:
                tempamt = product_amt.quantity * product_amt.product.discounted_price
                amount += tempamt
                total_amt = amount + shipping_amount
            data = {
                'cart_len': len(cart_product),
                'amount': amount,
                'shipping_amount': shipping_amount,
                'total_amt': total_amt
            }
        else:
            data = {
                'cart_len': len(cart_product),
                "HTML": '<div class="text-center mb-5"><h1 class="mb-3">Cart is empty.</h1><p>Please add some products in cart.</p><a href="/product/" class="btn btn-primary">Shop Now</a></div>'
            }
        return JsonResponse(data)


@login_required
def add_to_cart(request):
    # get product details
    cart_data = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 40.0
    total_amt = 0.0
    cart_product = [p for p in cart_data]
    if cart_product:
        for product_amt in cart_product:
            tempamt = product_amt.quantity * product_amt.product.discounted_price
            amount += tempamt
            total_amt = amount + shipping_amount
    context = {
        'datas': cart_data,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amt': total_amt
    }
    return render(request, 'shopping/addtocart.html', context)


@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET.get('address')
    if cust_id is not None:
        customer = Customer.objects.get(id=cust_id)
        print(cust_id, customer)
        cart_item = Cart.objects.filter(user=user)
        for product_item in cart_item:
            OrderPlaced(user=user, customer=customer, product=product_item.product, quantity=product_item.quantity).save()
            product_item.delete()
        return redirect('orders')
    else:
        messages.warning(request, 'You need add at least one address.')
        return redirect('profile')


def orders(request):
    order_data = OrderPlaced.objects.all()
    order_len = len([p for p in order_data])
    data = {
        'datas': order_len,
        'order_datas': order_data
    }
    return render(request, 'shopping/orders.html', data)
