# Generated by Django 5.0.3 on 2024-06-28 16:00

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
            name='GameRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField(default=20000000)),
                ('start_hour', models.IntegerField(default=0)),
                ('start_minute', models.IntegerField(default=0)),
                ('start_second', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=30)),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('Red', 'Red'), ('Green', 'Green'), ('Violet', 'Violet')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.gameround')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default='', max_length=50)),
                ('user_code', models.CharField(blank=True, max_length=12, null=True)),
                ('referals_number', models.IntegerField(blank=True, default=0)),
                ('userBalance', models.FloatField(default=0)),
                ('refer_code', models.CharField(blank=True, max_length=50, null=True)),
                ('total_balance', models.FloatField(blank=True, default=0)),
                ('total_withdraw', models.FloatField(blank=True, default=0)),
                ('total_deposite', models.FloatField(blank=True, default=0)),
                ('recomended_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoundWinColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_color', models.CharField(choices=[('Red', 'Red'), ('Green', 'Green'), ('Violet', 'Violet')], max_length=10)),
                ('red_bet_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('green_bet_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('violet_bet_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.gameround')),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('upi_id', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
