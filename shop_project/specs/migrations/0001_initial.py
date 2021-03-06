# Generated by Django 3.2.3 on 2021-05-29 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0013_auto_20210529_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='Characteristic name')),
                ('feature_filter_name', models.CharField(max_length=70, verbose_name='Filter name')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='Unit')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
            ],
            options={
                'unique_together': {('category', 'feature_name', 'feature_filter_name')},
            },
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Feature')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValidator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_feature_value', models.CharField(max_length=100, verbose_name='Valid name')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Category')),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Characteristic key')),
            ],
        ),
    ]
