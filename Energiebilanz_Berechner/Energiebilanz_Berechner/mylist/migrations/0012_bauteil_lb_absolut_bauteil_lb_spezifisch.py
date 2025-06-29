# Generated by Django 5.2 on 2025-06-26 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0011_bauteil_laufzeit_da_bauteil_laufzeit_hd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bauteil',
            name='lb_absolut',
            field=models.FloatField(blank=True, null=True, verbose_name='Lüftungswärmebedarf (kWh)'),
        ),
        migrations.AddField(
            model_name='bauteil',
            name='lb_spezifisch',
            field=models.FloatField(blank=True, null=True, verbose_name='Lüftungsbedarf spezifisch (kWh/m²)'),
        ),
    ]
