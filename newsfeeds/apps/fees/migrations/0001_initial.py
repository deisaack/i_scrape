# Generated by Django 2.0.2 on 2018-03-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('shortcode', models.CharField(blank=True, max_length=20, null=True)),
                ('comments', models.PositiveIntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('owner_id', models.PositiveIntegerField(blank=True, null=True)),
                ('tags', models.CharField(blank=True, max_length=200, null=True)),
                ('caption', models.TextField()),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
