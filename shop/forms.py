from django import forms
from django.contrib.auth.models import User
from .models import Order

# --- FORM AGGIUNTA AL CARRELLO ---
class CartAddProductForm(forms.Form):
    """ Form per selezionare la quantità di un prodotto da aggiungere al carrello. """
    quantity = forms.IntegerField(
        min_value=1,
        max_value=99,
        # Il widget definisce come appare il campo nell'HTML (un input numerico con stile CSS)
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 60px;'
        })
    )
    # Campo nascosto: indica se la quantità deve essere sommata (False) o sovrascritta (True)
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

# --- FORM REGISTRAZIONE UTENTE ---
class UserRegistrationForm(forms.ModelForm):
    """ Form basato sul modello User per creare nuovi account. """
    # Definiamo i campi password manualmente per usare il widget PasswordInput (nasconde i caratteri)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        # Applichiamo classi CSS ai campi del modello per l'aspetto estetico
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        """ Validazione personalizzata: controlla che le due password coincidano. """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        """ Validazione personalizzata: controlla che l'email non sia già presente nel database. """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

# --- FORM CREAZIONE ORDINE ---
class OrderCreateForm(forms.ModelForm):
    """ Form basato sul modello Order per raccogliere i dati di spedizione. """
    class Meta:
        model = Order
        # Campi che l'utente deve compilare per completare l'acquisto
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'payment_method']
        # Widget per integrare Bootstrap (class 'form-control') in ogni campo
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

"""
forms.ModelForm: viene usato per User e Order. 
Django guarda il modello nel database e crea automaticamente i campi corrispondenti, 
risparmiandoti di scriverli uno per uno.

Metodi clean_<nome_campo>: sono fondamentali per la sicurezza e l'integrità dei dati. 
Django li esegue automaticamente quando chiami form.is_valid() nelle tue Views. 
Se i dati non passano questi test, il form restituisce un errore senza salvare nulla.

Widgets e attrs: Django separa la logica del dato dal suo aspetto. 
Usando attrs={'class': 'form-control'}, stiamo dicendo a Django di 
aggiungere quella classe HTML in modo che il sito appaia moderno e curato 
usando framework come Bootstrap

Per permettere acquisti senza registrazione, 
OrderCreateForm è già impostato. Non richiede campi legati all'account (come la password), 
quindi un utente non loggato può compilarlo tranquillamente con il proprio indirizzo 
e procedere.

"""