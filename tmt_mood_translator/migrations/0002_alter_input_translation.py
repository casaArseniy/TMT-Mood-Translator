# Generated by Django 3.2.8 on 2021-11-01 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmt_mood_translator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='translation',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
