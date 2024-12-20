# Generated by Django 5.1.3 on 2024-11-09 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0006_alter_product_sellers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='markets',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sellers',
        ),
        migrations.AddField(
            model_name='product',
            name='markets',
            field=models.ManyToManyField(null=True, related_name='products', to='market_app.market'),
        ),
        migrations.AddField(
            model_name='product',
            name='sellers',
            field=models.ManyToManyField(null=True, related_name='products', to='market_app.seller'),
        ),
    ]
