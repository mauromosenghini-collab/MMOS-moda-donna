from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        
        # Check stock availability
        if quantity > product.stock:
            messages.error(request, f'Quantità non disponibile. Stock disponibile: {product.stock}')
            return redirect('shop:cart_detail')
        
        # Check if adding this quantity would exceed stock
        current_quantity = 0
        if str(product.id) in cart.cart:
            current_quantity = cart.cart[str(product.id)]['quantity']
        
        if not cd['override']:
            new_quantity = current_quantity + quantity
        else:
            new_quantity = quantity
            
        if new_quantity > product.stock:
            messages.error(request, f'Quantità non disponibile. Stock disponibile: {product.stock}')
            return redirect('shop:cart_detail')
        
        cart.add(product=product, quantity=quantity, override_quantity=cd['override'])
        if cd['override']:
            messages.success(request, f'Quantità di {product.name} aggiornata!')
        else:
            messages.success(request, f'{product.name} aggiunto al carrello!')
    else:
        messages.error(request, 'Errore nella modifica della quantità.')
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} rimosso dal carrello!')
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'shop/cart/detail.html', {'cart': cart})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
    )
            # clear the cart
            cart.clear()
            messages.success(request, 'Ordine creato con successo!')
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            })
        else:
            form = OrderCreateForm()
    return render(request, 'shop/order/create.html', {'cart': cart, 'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order/list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order/detail.html', {'order': order})
