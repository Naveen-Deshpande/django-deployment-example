# Generated by Django 2.2.5 on 2020-02-27 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_auto_20200227_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='aprroved_comment',
            new_name='approved_comment',
        ),
    ]