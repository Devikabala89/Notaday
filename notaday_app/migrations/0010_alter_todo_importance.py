# Generated by Django 5.0.4 on 2024-05-02 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notaday_app', '0009_todo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='importance',
            field=models.CharField(max_length=10),
        ),
    ]