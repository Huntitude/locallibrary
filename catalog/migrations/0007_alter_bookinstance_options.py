# Generated by Django 4.0.5 on 2022-07-09 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_rename_barrower_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back', 'status'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]