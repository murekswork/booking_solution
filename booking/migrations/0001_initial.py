# Generated by Django 5.0.3 on 2024-03-27 19:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin', models.DateField(verbose_name='Дата начала брони')),
                ('checkout', models.DateField(verbose_name='Дата конца брони')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                 related_name='bookings', to='rooms.room', verbose_name='Забронированная комната')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                 to=settings.AUTH_USER_MODEL, verbose_name='Бронирующий пользователь')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(check=models.Q(
                ('checkout__gt', models.F('checkin'))), name='checkin_before_checkout'),
        ),
    ]