# Generated by Django 5.0.3 on 2024-06-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0005_alter_bet_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='total_balance',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_deposite',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_withdraw',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_balance',
            field=models.IntegerField(default=0),
        ),
    ]
