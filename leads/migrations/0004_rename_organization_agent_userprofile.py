# Generated by Django 4.0.2 on 2022-03-02 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_lead_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='organization',
            new_name='userprofile',
        ),
    ]