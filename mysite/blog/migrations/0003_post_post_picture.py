# Generated by Django 2.2.5 on 2020-05-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200112_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_picture',
            field=models.ImageField(db_index=True, default='', upload_to='images/post_images/'),
        ),
    ]
