# Generated by Django 4.0.5 on 2022-07-04 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mine_mgt', '0003_claim_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mine',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mine', to=settings.AUTH_USER_MODEL),
        ),
    ]