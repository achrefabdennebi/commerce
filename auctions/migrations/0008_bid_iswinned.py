# Generated by Django 3.1.1 on 2020-10-06 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_bidedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='isWinned',
            field=models.BooleanField(default=False),
        ),
    ]
