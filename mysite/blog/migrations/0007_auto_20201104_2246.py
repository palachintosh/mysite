# Generated by Django 2.2.5 on 2020-11-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, db_index=True, max_length=800, verbose_name='Preview'),
        ),
    ]
