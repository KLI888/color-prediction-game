# Generated by Django 5.0.3 on 2024-06-28 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_alter_bet_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roundwincolor',
            name='win_color',
            field=models.CharField(blank=True, choices=[('Red', 'Red'), ('Green', 'Green'), ('Violet', 'Violet')], max_length=10, null=True),
        ),
    ]
