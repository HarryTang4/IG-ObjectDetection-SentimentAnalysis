# Generated by Django 4.1.7 on 2023-04-07 01:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("playground", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="CurrentUser",
        ),
    ]
