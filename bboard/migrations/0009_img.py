# Generated by Django 2.2.10 on 2021-06-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0008_revrubric'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='archives/%Y/%m/%d/', verbose_name='Изображение')),
                ('decs', models.TextField(verbose_name='Описание')),
            ],
        ),
    ]
