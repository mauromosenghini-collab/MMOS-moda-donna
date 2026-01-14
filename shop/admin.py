from django.contrib import admin
from django.forms import MediaDefiningClass
from .models import Category, Product, Cart, CartItem, Order, OrderItem

# --- CLASSE BASE PERSONALIZZATA PER LAYOUT ADMIN ---
class CustomAdminMixin(metaclass=MediaDefiningClass):
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }

# --- CONFIGURAZIONE CATEGORIE ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Colonne visibili nella lista generale delle categorie
    list_display = ['name', 'slug']
    # Genera automaticamente lo slug mentre digiti il nome (es. "Libri Gialli" -> "libri-gialli")
    prepopulated_fields = {'slug': ('name',)}

# --- CONFIGURAZIONE PRODOTTI ---
@admin.register(Product)
class ProductAdmin(CustomAdminMixin, admin.ModelAdmin):
    # Colonne visualizzate nella tabella prodotti
    list_display = ['name', 'slug', 'price', 'available', 'stock', 'created', 'updated']
    # Pannello filtri laterale (molto utile quando hai molti prodotti)
    list_filter = ['available', 'created', 'updated', 'category']
    # Permette di modificare prezzo, disponibilità e scorte direttamente dalla lista, senza cliccare sul prodotto
    list_editable = ['price', 'available', 'stock']
    # Generazione automatica dello slug dal nome
    prepopulated_fields = {'slug': ('name',)}

# --- GESTIONE CARRELLO (Visualizzazione In-line) ---
# TabularInline permette di vedere i prodotti nel carrello dentro la scheda del carrello stesso
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 # Evita di mostrare righe vuote aggiuntive predefinite


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created', 'updated']
    # Mostra gli oggetti nel carrello come una tabella dentro la pagina del Carrello
    inlines = [CartItemInline]

# --- GESTIONE ORDINI (Visualizzazione In-line) ---
# Permette di visualizzare gli articoli acquistati direttamente dentro la pagina dell'Ordine
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Mostra solo gli articoli effettivamente presenti, senza righe extra vuote


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Dettagli rapidi visibili nella lista ordini
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'paid', 'status', 'created']
    # Permette di modificare rapidamente lo stato 'paid' direttamente dalla lista ordini
    list_editable = ['paid']
    # Filtri rapidi per stato pagamento, stato ordine e data
    list_filter = ['paid', 'status', 'created']
    # Mostra gli articoli dell'ordine (OrderItem) in fondo alla pagina del dettaglio ordine
    inlines = [OrderItemInline]

    # AGGIUNTA: Registriamo l'azione personalizzata nell'elenco azioni
    actions = ['make_shipped']

    # DEFINIZIONE DELL'AZIONE:
    @admin.action(description='Segna gli ordini selezionati come Spediti')
    def make_shipped(self, request, queryset):
        # Aggiorna il campo 'status' per tutti gli ordini selezionati
        updated_count = queryset.update(status='shipped')
        # Invia un messaggio di conferma all'amministratore
        self.message_user(request, f'Successo! {updated_count} ordini sono stati segnati come spediti.')

#@admin.register: usare questa classe per gestire questo modello nell'admin.
#list_editable: permette di fare "aggiornamenti di massa" (es. cambiare i prezzi) molto velocemente.
#TabularInline: senza questo, per vedere cosa ha comprato un utente dovresti aprire
#l'ordine, segnarti l'ID, andare nella tabella OrderItem e cercarlo. Con gli inlines, vedi
#tutto in una sola schermata, proprio come una vera fattura.
#actions = ['make_shipped']: Dice a Django di aggiungere una voce nel menu a tendina
#"Azione" che trovi sopra la lista degli ordini.
#queryset: elenco degli ordini che hai selezionato cliccando sulle caselle (checkbox) a sinistra.
#queryset.update(status='shipped'): esegue un'unica operazione efficiente sul 
#database per modificare tutti i record scelti in un colpo solo.
#self.message_user: fa apparire quella striscia verde di conferma in alto nella pagina
#dopo che l'operazione è stata completata.