# Generated by Django 5.1.2 on 2024-11-25 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtest', '0003_indicator_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('strategy_count', models.IntegerField(default=0)),
                ('active_bots', models.IntegerField(default=0)),
                ('portfolio_size', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]