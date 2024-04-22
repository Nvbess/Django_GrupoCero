# Generated by Django 5.0.1 on 2024-04-22 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='obra',
            name='nombre_obra',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='obra',
            name='valor',
            field=models.IntegerField(default=0),
        ),
    ]
