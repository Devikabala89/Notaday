# Generated by Django 5.0.4 on 2024-05-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notaday_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Availablility'),
        ),
    ]
