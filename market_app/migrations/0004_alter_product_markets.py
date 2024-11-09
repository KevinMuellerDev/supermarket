# Generated by Django 5.1.3 on 2024-11-09 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0003_rename_market_product_markets_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='markets',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='market_app.market'),
        ),
    ]
