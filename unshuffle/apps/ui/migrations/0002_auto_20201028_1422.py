# Generated by Django 3.1.2 on 2020-10-28 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'get_latest_by': 'updated_at'},
        ),
    ]
