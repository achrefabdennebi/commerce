# Generated by Django 3.1.1 on 2020-10-06 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auctionlist_createdby'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
