# Generated by Django 2.0.5 on 2018-05-17 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('auth_system', models.CharField(max_length=64, null=True)),
                ('user_ip', models.CharField(max_length=64, null=True)),
                ('destination_ip', models.CharField(max_length=64, null=True)),
                ('destination_port', models.IntegerField(default=0)),
                ('connected_at', models.DateTimeField(max_length=64)),
            ],
        ),
    ]
