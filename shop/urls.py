from django.urls import path
from . import views  # Importa le viste definite nel file views.py della stessa cartella

# Nome dello spazio dei nomi (namespace) per identificare le URL di questa app nel progetto
app_name = 'shop'

urlpatterns = [
    # Pagina principale dello shop: mostra tutti i prodotti
    path('', views.product_list, name='product_list'),

    #path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    #path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # --- Gestione del Carrello ---

    # Visualizzazione del contenuto del carrello
    path('cart/', views.cart_detail, name='cart_detail'),
    # Aggiunta di un prodotto al carrello (richiede l'ID del prodotto)
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    # Rimozione di un prodotto dal carrello
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # --- Gestione Ordini ---

    # Checkout: creazione di un nuovo ordine
    path('order/create/', views.order_create, name='order_create'),
    # Storico ordini dell'utente
    path('orders/', views.order_list, name='order_list'),
    # Dettaglio di un singolo ordine specifico tramite il suo ID
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    # Marcare un ordine come pagato (view di test/utility)
    path('orders/<int:order_id>/mark-paid/', views.mark_order_paid, name='mark_order_paid'),

    #path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # --- Filtri e Dettagli Prodotto ---

    # Pagina di dettaglio di un prodotto: usa ID (numerico) e Slug (testo per SEO)
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    # Filtro prodotti per categoria: lo slug della categoria viene passato alla vista
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

]

#<int:id> o <int:product_id>: Indica a Django di aspettarsi un numero intero.
#  Se l'utente scrive una parola al posto del numero, Django restituirà un errore 404 automaticamente.

#<slug:slug>: Lo "slug" è la parte finale dell'URL leggibile (es: il-mio-prodotto-fantastico).
#  È ottimo per il posizionamento sui motori di ricerca (SEO).

#name='...': Questo nome è fondamentale perché ti permette di richiamare l'URL
#  nei template HTML usando il tag {% url 'shop:product_list' %} senza dover scrivere l'indirizzo a mano.
