# Generated by Django 4.2.7 on 2023-12-04 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_description_alter_blogpost_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='image',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='thumbnail',
            field=models.URLField(default='missing image'),
            preserve_default=False,
        ),
    ]
