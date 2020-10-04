# Generated by Django 3.1.1 on 2020-10-04 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlist_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='auctionList',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_List', to='auctions.auctionlist'),
        ),
    ]
