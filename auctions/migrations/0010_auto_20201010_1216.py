# Generated by Django 3.1.1 on 2020-10-10 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201010_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.CharField(default=2, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_watch_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
