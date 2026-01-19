# E-commerce Django

Un'applicazione e-commerce completa e funzionale sviluppata con Django, Python e Bootstrap 5. Il progetto gestisce l'intero ciclo di vendita: dalla navigazione dei prodotti alla gestione del carrello in sessione, fino alla creazione dell'ordine e al checkout (sia per utenti registrati che ospiti).
Superuser: amministratore Email: amministratore@ecommerce.com Password:Projectecommerce

## Caratteristiche

- ✅ Catalogo prodotti con categorie
- ✅ Carrello della spesa (session-based)
- ✅ Sistema di checkout e ordini (con/senza login)
- ✅ Scelta metodo di pagamento (Alla consegna / Con carta)
- ✅ Decremento automatico dello stock
- ✅ Autenticazione utenti (Login e Registrazione)
- ✅ Gestione ordini per utenti registrati
- ✅ Admin panel Django per gestione prodotti
- ✅ Design moderno e responsive con Bootstrap 5
- ✅ Supporto immagini prodotti

## Funzionalità Implementate

### Shopping & Catalogo
- **Vetrina Prodotti**: Visualizzazione dinamica dei prodotti con filtri per categoria
- **Dettaglio Prodotto**: Scheda tecnica con controllo real-time della disponibilità in magazzino
- **Navigazione Categoria**: Filtri intuitivi per categoria dai prodotti disponibili

### Carrello (Cart System)
- **Session-based**: Il carrello è salvato nella sessione dell'utente (non richiede login obbligatorio)
- **Gestione Quantità**: Possibilità di aggiungere, rimuovere o aggiornare le quantità con validazione stock
- **Context Processor**: Il badge del carrello è aggiornato globalmente in ogni pagina del sito

### Ordini & Checkout
- **Checkout Flessibile**: Supporto per acquisti sia da utente registrato che da ospite (Guest Checkout)
- **Metodi di Pagamento**: Scelta tra pagamento alla consegna o con carta (che autorizza automaticamente)
- **Validazione Dati**: Utilizzo di **Django Crispy Forms** per un'esperienza di inserimento dati pulita e sicura
- **Gestione Stock**: Decremento automatico della quantità disponibile al momento della conferma ordine
- **Riepilogo Ordine**: Pagina di conferma finale con generazione automatica del numero d'ordine
- **Stato Spedizione**: Monitoraggio dello stato dell'ordine e del pagamento tramite badge colorati

### Sicurezza & Autenticazione
- **Sistema di Login/Registrazione**: Autenticazione integrata con validazione email
- **Protezione CSRF**: Sicurezza garantita su tutti i moduli di invio dati
- **Guest Checkout**: Gli ospiti possono visualizzare i dettagli dell'ordine tramite ID

## Tecnologie Utilizzate

| Componente | Tecnologia |
|-----------|-----------|
| **Backend** | [Django 5.1](https://www.djangoproject.com/) |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Styling** | [Bootstrap 5](https://getbootstrap.com/), [Bootstrap Icons](https://icons.getbootstrap.com/) |
| **Form Framework** | [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/), [Crispy Bootstrap5](https://pypi.org/project/crispy-bootstrap5/) |
| **Database** | SQLite (sviluppo), MySQL/PostgreSQL (produzione) |
| **Immagini** | [Pillow](https://python-pillow.org/) |
| **Python** 3.8 o superiore
- **pip** (Python package manager)
- **Git** (opzionale, per clonare il repository)

## Installazione

### 1. Clona il repository

```bash
git clone <url-del-tuo-repository>
cd "project e-commerce"
```

### 2. Crea e attiva un ambiente virtuale

**Su Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Su Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Genera il file requirements.txt (se non esiste)

Se il repository non contiene il file `requirements.txt`, puoi generarlo:

```bash
pip freeze > requirements.txt
```

Questo comando salva tutte le dipendenze attualmente installate nel tuo ambiente virtuale.

### 4. Installa le dipendenze

```bash
pip install -r requirements.txt
```

Se il file non esiste, installa i pacchetti manualmente:
```bash
pip install django pillow django-crispy-forms crispy-bootstrap5
```

### 5. Esegui le migrazioni del database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crea un account superuser (admin)

```bash
python manage.py createsuperuser
```

Segui le istruzioni per creare un utente amministratore.

### 7. Avvia il server di sviluppo

```bash
python manage.py runserver
```

### 8. Accedi all'applicazione

- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Configurazione Email

Il sistema è predisposto per inviare email di conferma al termine di ogni ordine.

### Modalità Sviluppo (Console)

Di default, le email vengono stampate nella console del terminale. Nessuna configurazione richiesta.

### Modalità Produzione (SMTP)

Per inviare email reali, modifica `ecommerce/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tua-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tua-password-app-google'  # Usa una "App Password" se hai 2FA
DEFAULT_FROM_EMAIL = 'noreply@tuosito.com'
```
EMAGuida Operativa

### Aggiungere Prodotti

1. Accedi all'admin panel: http://127.0.0.1:8000/admin/
2. **Crea una Categoria**:
   - Clicca su "Categorie" → "Aggiungi categoria"
   - Inserisci nome e slug (es: "abbigliamento-donna")
   - Salva

3. **Aggiungi Prodotti**:
   - Clicca su "Prodotti" → "Aggiungi prodotto"
   - Compila i campi:
     - **Nome**: Nome del prodotto
     - **Slug**: URL-friendly (es: "maglietta-nera")
     - **Categoria**: Seleziona la categoria creata
     - **Prezzo**: Prezzo in €
     - **Descrizione**: Dettagli e specifiche
     - **Immagine**: Foto del prodotto (opzionale)
     - **Stock**: Quantità disponibile
     - **Available**: Spunta se il prodotto è disponibile
   - Salva

### Come Usare l'Applicazione (Utente Finale)

- **Navigazione**: Visualizza i prodotti nella home o filtra per categoria
- **Dettagli Prodotto**: Clicca su un prodotto per vederne i dettagli completi
- **Carrello**: Aggiungi prodotti, modifica quantità, rimuovi articoli
- **Checkout**: 
  - Inserisci dati di spedizione (funziona con/senza login)
  - Scegli il metodo di pagamento:
    - 💳 **Con carta**: Ordine marcato automaticamente come pagato
    - 🚚 **Alla consegna**: Pagamento al ritiro
- **Ordini**: Gli utenti registrati possono visualizzare lo storico ordini

## Struttura del Progetto

```
project e-commerce/
├── ecommerce/                  # Configurazione principale Django
│   ├── settings.py             # Impostazioni progetto
│   ├── urls.py                 # URL principali
│   ├── asgi.py                 # ASGI config
│   └── wsgi.py                 # WSGI config
├── shop/                        # Applicazione principale e-commerce
│   ├── models.py               # Modelli (Product, Category, Order, OrderItem, Cart, CartItem)
│   ├── views.py                # Viste (product, cart, checkout, order management)
│   ├── urls.py                 # URL routing dell'app
│   ├── forms.py                # Form (CartAddProductForm, OrderCreateForm, UserRegistrationForm)
│   ├── admin.py                # Configurazione Django Admin
│   ├── cart.py                 # Logica e classe Cart (session-based)
│   └── migrations/             # Migration del database
├── templates/                   # Template HTML
│   ├── base.html Stile

- I file CSS si trovano in `static/css/style.css`
- Modifica i template in `templates/` per personalizzare layout e design
- Usa Bootstrap 5 classes per mantenere la responsività

### Aggiungere Nuove Funzionalità

Ecco alcune estensioni consigliate:

| Funzionalità | Implementazione |
|-------------|-----------------|
| **Gateway Pagamento** | Integra Stripe, PayPal o Razorpay |
| **Filtri Prodotti** | Aggiungi ricerca per nome e filtri per prezzo/categoria |
| **Recensioni** | Sistema di valutazione (rating) e commenti per prodotto |
| **Wishlist** | Salvataggio prodotti preferiti (model + session) |
| **Notifiche Email** | Configura Django-Celery per invio asincrono |
| **Analytics** | Integra Google Analytics o Matomo |
| **SEO** | Aggiungi sitemap.xml e robots.txt |

## Dipendenze Principali

| Libreria | Versione | Utilizzo |
|---------|---------|----------|
| **Django** | 5.1+ | Framework web principale |
| **Pillow** | 10.0+ | Gestione immagini (ImageField) |
| **django-crispy-forms** | 2.1+ | Rendering form con Bootstrap |
| **crispy-bootstrap5** | 2.0+ | Theme Bootstrap 5 per Crispy Forms |

## Sicurezza - Checklist Pre-Produzione

Prima di mettere online, assicurati di:

- [ ] Cambiare `SECRET_KEY` in `settings.py` (genera uno nuovo con `django.core.management.utils.get_random_secret_key()`)
- [ ] Impostare `DEBUG = False` in `settings.py`
- [ ] Configurare `ALLOWED_HOSTS` con i tuoi domini
- [ ] Usare un database robusto (PostgreSQL, MySQL) invece di SQLite
- [ ] Abilitare HTTPS/SSL su server
- [ ] Configurare CSRF_TRUSTED_ORIGINS correttamente
- [ ] Usare variabili d'ambiente per credenziali sensibili (`.env`)
- [ ] Impostare `SECURE_SSL_REDIRECT = True`
- [ ] Configurare CORS se hai frontend separato
- [ ] Implementare rate limiting su checkout
- [ ] Fare regolari backup del database

## Troubleshooting

| Problema | Soluzione |
|---------|-----------|
| **ModuleNotFoundError** | Assicurati di aver eseguito `pip install -r requirements.txt` |
| **Database locked** | Elimina `db.sqlite3` e rifai le migrazioni |
| **Immagini non caricate** | Controlla che `MEDIA_ROOT` e `MEDIA_URL` siano configurati in `settings.py` |
| **Static files non trovati** | Esegui `python manage.py collectstatic` |
| **Email non inviate** | Controlla la configurazione SMTP in `settings.py` (modalità console in sviluppo) |

## Risorse Utili

- 📚 [Documentazione Django](https://docs.djangoproject.com/)
- 🎨 [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- 📝 [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/)
- 🖼️ [Pillow Documentation](https://pillow.readthedocs.io/)

## Licenza

Questo progetto è **open source** e disponibile per uso personale e commerciale sotto licenza MIT.

## Author

Progetto Django e-commerce professionale - 2026
- **Email**: Configura l'invio di email per conferme ordini
- **Ricerca**: Aggiungi una funzione di ricerca prodotti
- **Recensioni**: Aggiungi un sistema di recensioni prodotti

Spiegazione delle librerie:

Django: Il framework principale.

django-crispy-forms: Per rendere i form Bootstrap eleganti.

crispy-bootstrap5: Il pacchetto specifico per il design di Bootstrap 5.

Pillow: La libreria fondamentale per gestire il caricamento delle immagini dei prodotti (ImageField).

## Note di sicurezza


1. Cambia `SECRET_KEY` in `settings.py`
2. Imposta `DEBUG = False`
3. Configura un database più robusto ( MySQL)
4. Configura HTTPS
5. Aggiungi protezione CSRF e altre misure di sicurezza
6. Configura correttamente `ALLOWED_HOSTS`

## Supporto

Per problemi o domande, consulta la [documentazione Django](https://docs.djangoproject.com/).

## Licenza

Questo progetto è open source e disponibile per uso personale e commerciale.
