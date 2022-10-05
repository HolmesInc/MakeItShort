# Generated by Django 4.1.1 on 2022-10-05 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_url', models.URLField(unique=True)),
                ('url_hash', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LinkUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.CharField(max_length=30)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='link_transformer.url')),
            ],
        ),
    ]