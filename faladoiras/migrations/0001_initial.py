# Generated by Django 4.0.3 on 2023-08-17 22:33

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import faladoiras.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='faladoiras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faladoiras_persoa', models.CharField(max_length=120)),
                ('faladoiras_image_persoa', models.ImageField(blank=True, null=True, upload_to=faladoiras.models.upload_image_path)),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Deixar_en_blanco')),
                ('faladoiras_resumen_persoa', models.TextField()),
                ('faladoiras_content', ckeditor.fields.RichTextField()),
                ('faladoiras_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='faladoiras_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('correo_electrónico', models.EmailField(max_length=255, validators=[faladoiras.models.email_validation])),
                ('comentario', models.TextField()),
                ('date_added', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('faladoiras_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='faladoiras.faladoiras')),
            ],
            options={
                'ordering': ['date_added'],
            },
        ),
    ]