# Generated by Django 3.0.3 on 2020-03-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_auto_20200316_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='e-mail address'),
        ),
    ]