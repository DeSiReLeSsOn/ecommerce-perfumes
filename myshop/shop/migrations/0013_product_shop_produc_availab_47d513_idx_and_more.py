# Generated by Django 5.0 on 2024-05-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_search_count'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['available'], name='shop_produc_availab_47d513_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='shop_produc_price_3b79b5_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['views_count'], name='shop_produc_views_c_ecc996_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['search_count'], name='shop_produc_search__fe8900_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category_id'], name='shop_produc_categor_d249e3_idx'),
        ),
    ]