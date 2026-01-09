# E-commerce Django

Un sito e-commerce completo sviluppato con Django, Python e Bootstrap 5.

## Caratteristiche

- ✅ Catalogo prodotti con categorie
- ✅ Carrello della spesa (session-based)
- ✅ Sistema di checkout e ordini
- ✅ Autenticazione utenti
- ✅ Gestione ordini per utenti registrati
- ✅ Admin panel Django per gestione prodotti
- ✅ Design moderno e responsive con Bootstrap 5
- ✅ Supporto immagini prodotti

## Requisiti

- Python 3.8 o superiore
- pip (Python package manager)

## Installazione

1. **Clona o scarica il progetto**

2. **Crea un ambiente virtuale** (consigliato):
```bash
python -m venv venv
```

3. **Attiva l'ambiente virtuale**:
   - Su Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Su Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Installa le dipendenze**:
```bash
pip install -r requirements.txt
```

5. **Esegui le migrazioni del database**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crea un superuser** (per accedere all'admin):
```bash
python manage.py createsuperuser
```

7. **Avvia il server di sviluppo**:
```bash
python manage.py runserver
```

8. **Apri il browser** e vai a:
   - Sito: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Utilizzo

### Aggiungere prodotti

1. Accedi all'admin panel: http://127.0.0.1:8000/admin/
2. Vai su "Categorie" e crea una categoria
3. Vai su "Prodotti" e aggiungi i prodotti con:
   - Nome
   - Slug (generato automaticamente)
   - Categoria
   - Prezzo
   - Descrizione
   - Immagine (opzionale)
   - Quantità disponibile

### Funzionalità utente

- **Navigazione prodotti**: Visualizza tutti i prodotti o filtra per categoria
- **Dettagli prodotto**: Clicca su un prodotto per vedere i dettagli
- **Carrello**: Aggiungi prodotti al carrello, modifica quantità, rimuovi articoli
- **Checkout**: Completa l'ordine inserendo i dati di spedizione
- **Ordini**: Gli utenti registrati possono visualizzare i loro ordini

## Struttura del progetto

```
project e-commerce/
├── ecommerce/          # Configurazione principale Django
│   ├── settings.py     # Impostazioni progetto
│   ├── urls.py         # URL principali
│   └── wsgi.py         # WSGI config
├── shop/               # Applicazione principale
│   ├── models.py       # Modelli (Product, Category, Order, etc.)
│   ├── views.py        # Viste
│   ├── urls.py         # URL dell'app
│   ├── admin.py        # Configurazione admin
│   └── cart.py         # Logica carrello
├── templates/          # Template HTML
│   ├── base.html       # Template base
│   └── shop/           # Template shop
├── static/             # File statici (CSS, JS, immagini)
├── media/              # Immagini caricate (generato automaticamente)
├── manage.py           # Script di gestione Django
└── requirements.txt    # Dipendenze Python
```

## Personalizzazione

### Modificare lo stile

I file CSS si trovano in `static/css/style.css`. Puoi anche modificare i template in `templates/` per personalizzare l'aspetto.

### Aggiungere funzionalità

- **Pagamenti**: Integra un gateway di pagamento (Stripe, PayPal, etc.)
- **Email**: Configura l'invio di email per conferme ordini
- **Ricerca**: Aggiungi una funzione di ricerca prodotti
- **Recensioni**: Aggiungi un sistema di recensioni prodotti

## Note di sicurezza

⚠️ **IMPORTANTE**: Questo è un progetto di sviluppo. Per la produzione:

1. Cambia `SECRET_KEY` in `settings.py`
2. Imposta `DEBUG = False`
3. Configura un database più robusto (PostgreSQL, MySQL)
4. Configura HTTPS
5. Aggiungi protezione CSRF e altre misure di sicurezza
6. Configura correttamente `ALLOWED_HOSTS`

## Supporto

Per problemi o domande, consulta la [documentazione Django](https://docs.djangoproject.com/).

## Licenza

Questo progetto è open source e disponibile per uso personale e commerciale.
