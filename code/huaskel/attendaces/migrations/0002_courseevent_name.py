# Generated by Django 3.2.8 on 2023-05-14 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendaces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseevent',
            name='name',
            field=models.CharField(default='Test name', max_length=200),
            preserve_default=False,
        ),
    ]
