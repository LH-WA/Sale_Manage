# Generated by Django 2.2.9 on 2021-05-19 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('user_account', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('user_psw', models.CharField(max_length=10)),
                ('user_branch', models.CharField(max_length=10)),
                ('user_dep', models.CharField(max_length=10)),
            ],
        ),
    ]
