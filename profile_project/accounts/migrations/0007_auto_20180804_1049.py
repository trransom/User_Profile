# Generated by Django 2.0.7 on 2018-08-04 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180802_1026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='first_name',
            new_name='USERNAME_FIELD',
        ),
    ]
