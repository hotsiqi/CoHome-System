# Generated by Django 5.0.1 on 2024-02-10 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_transaction_verified_at_transaction_verified_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentproof',
            name='house_unit',
        ),
        migrations.AddField(
            model_name='paymentproof',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_proofs', to='users.transaction'),
        ),
    ]
