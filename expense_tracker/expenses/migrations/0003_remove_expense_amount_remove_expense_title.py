# Generated by Django 5.1.2 on 2024-10-16 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0002_remove_expense_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="title",
        ),
    ]
