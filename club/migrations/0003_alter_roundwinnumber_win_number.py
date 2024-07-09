# Generated by Django 5.0.3 on 2024-07-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_alter_roundwinnumber_win_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roundwinnumber',
            name='win_number',
            field=models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], default='6', max_length=10),
        ),
    ]
