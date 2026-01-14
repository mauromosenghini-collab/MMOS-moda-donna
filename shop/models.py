from django.db import models
from django.contrib.auth.models import User # Per legare carrelli e ordini agli utenti registrati
from django.core.validators import MinValueValidator # Per impedire prezzi o quantità negative
from django.urls import reverse # Per creare URL dinamici basati su slug o ID , generare URL dinamicamente
from decimal import Decimal

# --- CATEGORIE ---
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name")
    # slug: versione dell'URL del nome (es: 'Elettronica' -> 'elettronica')
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Genera il link automatico per vedere i prodotti di questa categoria
        return reverse('shop:product_list_by_category', args=[self.slug])

# --- PRODOTTI ---
class Product(models.Model):
    # Relazione 1-a-molti: una categoria ha molti prodotti
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Category")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Name")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="Slug")
    # upload_to: organizza le foto in cartelle per data (es: products/2026/01/10/)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    # Prezzo con validazione: non può essere meno di 0.01
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Price")
    available = models.BooleanField(default=True, verbose_name="Available")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created") # Data creazione automatica
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated") # Data modifica automatica
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    
    class Meta:
        ordering = ('-created',) # I più recenti appaiono per primi
        indexes = [
            models.Index(fields=['id', 'slug']), # Ottimizza la velocità di ricerca nel database
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

# --- CARRELLO (CONTENITORE) ---
class Cart(models.Model):
    # OneToOne: un utente ha un solo carrello attivo
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name="Session Key") # Per utenti non loggati
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Cart session {self.session_key}"
    
    def get_total_price(self):
        # Somma il prezzo totale di tutti gli elementi nel carrello
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        # Somma la quantità totale di pezzi nel carrello
        return sum(item.quantity for item in self.items.all())

# --- ELEMENTI DEL CARRELLO (DETTAGLIO) ---
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="Cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Quantity")
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity

# --- ORDINE (DATI DI SPEDIZIONE E STATO) ---
class Order(models.Model):
    STATUS_CHOICES = [ # Definisce gli stati possibili di un ordine
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Alla consegna'),
        ('card', 'Con carta'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Address")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    city = models.CharField(max_length=100, verbose_name="City")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    paid = models.BooleanField(default=False, verbose_name="Paid") # Indica se il pagamento è avvenuto
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash', verbose_name="Payment Method")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

# --- DETTAGLIO PRODOTTI ORDINATI ---
class OrderItem(models.Model):
    # Lega i prodotti all'ordine. Importante: salva il prezzo al momento dell'acquisto!
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity

#Relazioni ForeignKey: crea una relazione
#"molti-a-uno". Ad esempio, molti OrderItem appartengono a un solo Order
#OrderItem ha un campo price: una scelta di logica, 
#se il prezzo di un prodotto nel modello Product cambia domani, non
#vogliamo che cambino i prezzi degli ordini passati. Salviamo quindi il prezzo storico
#dentro l'ordine.
#La classe Meta: classe interna che fornisce metadati a Django che non sono
#campi del database (es: come ordinare i risultati o come chiamare la tabella al plurale
#nell'area admin).
#get_absolute_url(): È una "best practice" di Django. Permette di ottenere l'URL di un
#oggetto direttamente dal database, rendendo i template HTML molto più puliti.