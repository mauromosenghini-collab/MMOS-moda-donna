from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Alla consegna'), ('card', 'Con carta')], default='cash', max_length=10, verbose_name='Payment Method'),
        ),
    ]
