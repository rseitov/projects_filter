# Generated by Django 3.1.6 on 2021-02-16 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnpm', '0007_auto_20210216_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropDesc',
            fields=[
                ('idx_resourse', models.IntegerField(primary_key=True, serialize=False)),
                ('str_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('str_user', models.CharField(blank=True, max_length=80, null=True)),
                ('dte_date', models.IntegerField(blank=True, null=True)),
                ('str_value', models.CharField(blank=True, max_length=275, null=True)),
            ],
            options={
                'db_table': 'prop_desc',
                'managed': False,
            },
        ),
    ]
