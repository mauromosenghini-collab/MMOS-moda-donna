from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm, UserRegistrationForm

# --- VISUALIZZAZIONE PRODOTTI ---
def product_list(request, category_slug=None):
    """ Elenca i prodotti, opzionalmente filtrati per categoria. """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) # Mostra solo prodotti disponibili
    if category_slug:
        # Se c'è uno slug nell'URL, filtra per quella categoria specifica
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    """ Mostra il dettaglio di un singolo prodotto e il modulo per aggiungerlo al carrello. """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })

# --- LOGICA DEL CARRELLO ---
@require_POST
def cart_add(request, product_id):
    """ Aggiunge un prodotto al carrello con controllo rigoroso dello stock. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        # 1. Verifica immediata: la quantità richiesta è superiore al magazzino?
        if quantity > product.stock:
            messages.error(request, f'Quantità non disponibile. Stock disponibile: {product.stock}')
            return redirect('shop:cart_detail')
        # 2. Verifica cumulata: quello che c'è già nel carrello + il nuovo supera lo stock?
        current_quantity = 0
        if str(product.id) in cart.cart:
            current_quantity = cart.cart[str(product.id)]['quantity']
        
        if not cd['override']:
            new_quantity = current_quantity + quantity
        else:
            new_quantity = quantity # Se 'override' è True, stiamo sovrascrivendo la quantità
            
        if new_quantity > product.stock:
            messages.error(request, f'Quantità non disponibile. Stock disponibile: {product.stock}')
            return redirect('shop:cart_detail')
        # 3. Esecuzione aggiunta
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
    """ Rimuove un articolo dal carrello. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} rimosso dal carrello!')
    return redirect('shop:cart_detail')


def cart_detail(request):
    """ Visualizza il carrello e permette di aggiornare le quantità per ogni riga. """
    cart = Cart(request)
    for item in cart:
        # Crea un form per ogni riga del carrello per permettere modifiche rapide
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'shop/cart/detail.html', {'cart': cart})

# --- GESTIONE ORDINI ---
def order_create(request):
    """ Gestisce la creazione di un ordine dai dati del carrello. Permette acquisti con o senza registrazione. """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # Crea l'oggetto ma non lo salva ancora nel DB
            if request.user.is_authenticated:
                order.user = request.user # Lega l'ordine all'utente loggato
            # Se pagamento con carta, marca automaticamente come pagato
            if form.cleaned_data.get('payment_method') == 'card':
                order.paid = True
            order.save() # Ora salva l'ordine nel DB
            # Trasforma ogni elemento del carrello in una riga dell'ordine (OrderItem)
            for item in cart:
                # Decrementa lo stock del prodotto
                product = item['product']
                product.stock -= item['quantity']
                product.save()
                # Crea l'elemento dell'ordine
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'], # Salviamo il prezzo attuale per storico
                    quantity=item['quantity']
                )
            cart.clear() # Svuota il carrello dopo l'acquisto
            messages.success(request, 'Ordine creato con successo!')
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        # Pre-compila il modulo con i dati dell'utente se disponibile
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
    """ Visualizza lo storico ordini dell'utente. """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order/list.html', {'orders': orders})


def order_detail(request, order_id):
    """ Mostra i dettagli di un singolo ordine. Gli utenti loggati possono vedere solo i loro ordini, gli ospiti possono vedere l'ordine col loro ID. """
    if request.user.is_authenticated:
        # Se loggato, mostra solo i propri ordini
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        # Se non loggato, mostra l'ordine per ID (gli ospiti possono accedere ai loro ordini tramite l'ID)
        order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order/detail.html', {'order': order})


@login_required
def mark_order_paid(request, order_id):
    # View semplice per marcare un ordine come pagato (per sviluppo/test)
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.save()
    messages.success(request, f'Ordine {order.id} marcato come pagato.')
    return redirect('shop:order_detail', order_id=order.id)

"""
implementato è il doppio controllo dello stock in cart_add:

Controlla se la singola aggiunta è valida.

Controlla se il totale (quello già nel carrello + il nuovo) non superi il magazzino reale.
Questo impedisce a un utente di aggiungere 5 pezzi, poi altri 10, 
superando magari una disponibilità di soli 12 pezzi.

"""