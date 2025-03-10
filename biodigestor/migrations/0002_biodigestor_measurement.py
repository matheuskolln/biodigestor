# Generated by Django 5.0.4 on 2024-04-04 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biodigestor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioDigestor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_temperature', models.FloatField()),
                ('external_temperature', models.FloatField()),
                ('main_pressure', models.FloatField()),
                ('gas_level', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ],
        ),
    ]
