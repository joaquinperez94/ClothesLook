# Generated by Django 2.0 on 2019-01-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothesLookApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='look',
            name='prenda',
        ),
        migrations.AddField(
            model_name='look',
            name='clothes',
            field=models.ManyToManyField(null=True, to='clothesLookApp.Clothing'),
        ),
    ]
