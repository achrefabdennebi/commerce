# Generated by Django 3.1.1 on 2020-09-22 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlist_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlist',
            name='watchlist',
            field=models.BooleanField(default=False),
        ),
    ]