# Generated by Django 5.1.1 on 2024-10-31 10:57

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(default='')),
                ('date_opened', models.DateField(default=datetime.datetime.today)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('restaurant_type', models.CharField(choices=[('IN', 'Indian'), ('IT', 'Italian'), ('CH', 'Chinese'), ('JP', 'Japanese'), ('MX', 'Mexican'), ('FR', 'French'), ('US', 'American'), ('MD', 'Mediterranean'), ('TH', 'Thai'), ('GR', 'Greek')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField()),
                ('review', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_time', models.DateTimeField()),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.restaurant')),
            ],
        ),
    ]
