# Generated by Django 4.1.1 on 2022-10-04 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_alter_bookreview_rating_alter_paperbook_rating_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='biography',
            new_name='information',
        ),
    ]
