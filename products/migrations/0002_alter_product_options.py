# Generated by Django 4.0.4 on 2022-04-19 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-publish_date']},
        ),
    ]