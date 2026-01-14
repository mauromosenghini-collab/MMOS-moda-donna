from .cart import Cart

"""
    Rende il carrello disponibile in tutti i template del sito.
    Questo permette di visualizzare il numero di articoli (badge) nella navbar.
    """
# Restituisce un dizionario. La chiave 'cart' sarà la variabile
# che useremo nei template HTML (es. {{ cart|length }})
def cart(request):
    return {'cart': Cart(request)}
