# Generated by Django 3.2.7 on 2021-09-25 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210925_1016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='writer',
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
