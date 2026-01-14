
# Importa il modulo per l'interfaccia di amministrazione predefinita di Django
from django.contrib import admin
# 'path' serve per definire le rotte, 'include' permette di collegare file urls.py di altre app
from django.urls import path, include
# Importa l'oggetto settings per accedere alle variabili definite in settings.py (come DEBUG o MEDIA_URL)
from django.conf import settings
# Funzione utilizzata per generare le rotte necessarie a servire file statici e media durante lo sviluppo
from django.conf.urls.static import static

# Definizione dell'elenco delle rotte (URL) del progetto
urlpatterns = [
    # Rotta per l'interfaccia di amministrazione predefinita di Django
    path('admin/', admin.site.urls),
    # Include le rotte dell'app personalizzata 'shop' come rotta principale
    path('', include('shop.urls')),
    # Include le rotte predefinite di Django per l'autenticazione (login, logout, gestione password)
    path('accounts/', include('django.contrib.auth.urls')),
]
# Configurazione per servire i file multimediali (media) e statici durante lo sviluppo
# Questa parte viene eseguita solo se la modalità DEBUG è attiva nel file settings.py
if settings.DEBUG:
    # Aggiunge il supporto per i file caricati dagli utenti (es. immagini dei prodotti)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Aggiunge il supporto per i file statici (es. CSS, JavaScript, immagini del tema)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#path('admin/', ...): Crea il punto di accesso per il pannello di controllo dove puoi gestire i dati del database.

#include('shop.urls'): Questo è il cuore della tua applicazione. Dice a Django di andare a guardare dentro la cartella dell'app "shop" per trovare le altre pagine (come la home, il carrello, ecc.).

#django.contrib.auth.urls: Ti risparmia la fatica di scrivere manualmente le rotte per il login e il logout.

#if settings.DEBUG: È fondamentale perché, in produzione, i file statici vengono solitamente gestiti da server web dedicati (come Nginx o Apache). In fase di sviluppo, invece, lasciamo che sia Django a mostrarli.