# Generated by Django 5.0.6 on 2024-06-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0006_userfile_commentary_userfile_last_download_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userfile",
            name="link_hash",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]