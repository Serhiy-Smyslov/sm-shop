# Generated by Django 3.2.3 on 2021-05-19 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210519_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Total price'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Total price'),
        ),
    ]