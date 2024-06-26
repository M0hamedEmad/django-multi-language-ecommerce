# Generated by Django 5.0.3 on 2024-04-15 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='payment type')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='total')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('done', 'done'), ('canceld', 'canceld'), ('waited', 'waited'), ('error', 'error')], max_length=40, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('processing', 'processing'), ('in delivery', 'in delivery'), ('completed', 'completed'), ('cancelled', 'cancelled')], max_length=255, null=True, verbose_name='status')),
                ('paid', models.BooleanField(default=False, verbose_name='paid')),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='shipping cost')),
                ('customer_first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='customer name')),
                ('customer_last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='customer last name')),
                ('customer_email', models.CharField(blank=True, max_length=255, null=True, verbose_name='customer email')),
                ('customer_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='customer phone')),
                ('adress_line', models.CharField(blank=True, max_length=255, null=True, verbose_name='adress_line')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='city')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='state')),
                ('zip_code', models.CharField(blank=True, max_length=155, null=True, verbose_name='zip_code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('shipping', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='store.shippers')),
                ('payment_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payment.paymentdata')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='payment.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='product.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='product.size')),
            ],
        ),
    ]
