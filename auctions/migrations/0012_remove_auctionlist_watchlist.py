# Generated by Django 3.1.1 on 2020-10-10 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201010_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlist',
            name='watchlist',
        ),
    ]
