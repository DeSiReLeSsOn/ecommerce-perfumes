# Generated by Django 5.0 on 2024-04-22 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0004_alter_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='advertisement_text',
            field=models.TextField(blank=True, verbose_name='Текст рекламы'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banners/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активна/Неактивна'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='link',
            field=models.CharField(max_length=200, verbose_name='Ссылка'),
        ),
    ]