# Generated by Django 3.1.6 on 2021-02-17 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tnpm', '0009_probemanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnpmProbeManager',
            fields=[
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tnpm.probemanager')),
            ],
        ),
    ]