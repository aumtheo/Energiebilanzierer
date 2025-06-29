# Generated by Django 5.2 on 2025-06-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylist', '0002_druckverlustbauteil'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sonnenschutzfaktor',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='sonnenschutzfaktor',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='sonnenschutzfaktor',
            name='f_c_g_gt_0_40_zweifach',
            field=models.FloatField(default=1.0, help_text='Abminderungsfaktor bei g > 0,40 (zweifach)'),
        ),
        migrations.AddField(
            model_name='sonnenschutzfaktor',
            name='f_c_g_le_0_40_dreifach',
            field=models.FloatField(default=1.0, help_text='Abminderungsfaktor bei g ≤ 0,40 (dreifach)'),
        ),
        migrations.AddField(
            model_name='sonnenschutzfaktor',
            name='f_c_g_le_0_40_zweifach',
            field=models.FloatField(default=1.0, help_text='Abminderungsfaktor bei g ≤ 0,40 (zweifach)'),
        ),
        migrations.AddField(
            model_name='sonnenschutzfaktor',
            name='sonnenschutzvorrichtung',
            field=models.CharField(default='', help_text='Beschreibung der Sonnenschutzeinrichtung', max_length=200),
        ),
        migrations.AddField(
            model_name='sonnenschutzfaktor',
            name='zeile',
            field=models.CharField(default='', help_text="Zeilennummer (z. B. '2.1', '3.1.2' …)", max_length=10, unique=True),
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='beschreibung',
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='fc_g_gt0_4_dreifach',
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='fc_g_gt0_4_zweifach',
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='fc_g_le0_4_dreifach',
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='fc_g_le0_4_zweifach',
        ),
        migrations.RemoveField(
            model_name='sonnenschutzfaktor',
            name='zeilennr',
        ),
    ]
