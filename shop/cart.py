from decimal import Decimal
from django.conf import settings
from shop.models import Product, Cart as CartModel, CartItem


class Cart:
    def __init__(self, request):
        """
        Inizializza il carrello recuperandolo dalla sessione corrente.
        """
        self.session = request.session
        # Prova a recuperare il carrello usando l'ID definito nei settings
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            ## Se non esiste, crea un carrello vuoto (un dizionario) nella sessione
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Aggiunge un prodotto al carrello o ne aggiorna la quantità.
        """
        product_id = str(product.id) # Usiamo stringhe perché le chiavi JSON devono essere stringhe
        if product_id not in self.cart:
            # Se il prodotto non è nel carrello, lo inizializza con prezzo e quantità 0
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            # Sostituisce la quantità esistente (utile se l'utente cambia valore nel carrello)
            self.cart[product_id]['quantity'] = quantity
        else:
            # Incrementa la quantità esistente (utile dal tasto "Aggiungi")
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        #Notifica a Django che la sessione è stata modificata e deve essere salvata.
        self.session.modified = True
    
    def remove(self, product):
        """
        Rimuove completamente un prodotto dal carrello.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
        Permette di ciclare sugli elementi del carrello (es. in un ciclo for nel template).
        Recupera gli oggetti Product dal database per avere i dati aggiornati.
        """
        product_ids = self.cart.keys()
        # Recupera tutti i prodotti presenti nel carrello dal database
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            # Aggiunge l'oggetto prodotto reale al dizionario del carrello
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            # Converte il prezzo da stringa a Decimal per i calcoli
            item['price'] = Decimal(item['price'])
            # Calcola il subtotale per ogni riga
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Conta il numero totale di pezzi presenti nel carrello (somma delle quantità).
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calcola il costo totale complessivo del carrello.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_items(self):
        """
        Restituisce il numero totale di articoli (equivalente a __len__).
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_item_quantity(self, product_id):
        """
        Restituisce la quantità di un prodotto specifico già presente nel carrello.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        return 0
    
    def clear(self):
        """
        Svuota completamente il carrello eliminandolo dalla sessione.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

"""
Velocità: Usare le sessioni (spesso salvate in cache o database temporanei)
rende l'aggiunta al carrello istantanea,
senza rallentare il server con continue query SQL "pesanti".

JSON friendly: Memorizziamo il prezzo come str (stringa)
perché il formato JSON delle sessioni non supporta nativamente il tipo Decimal.
Lo riconvertiamo in numero solo quando dobbiamo fare i calcoli
(metodo __iter__ e get_total_price).

Indipendenza: Grazie al metodo __iter__,
nei template HTML si può scrivere semplicemente {% for item in cart %}
per accesso immediato a item.product.name, item.total_price, ecc.

"""