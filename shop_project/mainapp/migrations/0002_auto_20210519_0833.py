# Generated by Django 3.2.3 on 2021-05-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='for_anonymous_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
    ]
