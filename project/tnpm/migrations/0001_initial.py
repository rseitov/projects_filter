# Generated by Django 3.1.6 on 2021-02-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElmtDesc',
            fields=[
                ('idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('str_name', models.CharField(blank=True, max_length=80, null=True, unique=True)),
                ('str_state', models.CharField(blank=True, max_length=3, null=True)),
                ('str_origin', models.CharField(blank=True, max_length=32, null=True)),
                ('int_date', models.IntegerField(blank=True, null=True)),
                ('str_profile', models.CharField(blank=True, max_length=255, null=True)),
                ('str_type', models.CharField(blank=True, max_length=32, null=True)),
                ('str_comment', models.CharField(blank=True, max_length=4000, null=True)),
                ('str_user', models.CharField(blank=True, max_length=32, null=True)),
                ('int_collector', models.IntegerField(blank=True, null=True)),
                ('int_inv_miss_cnt', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'elmt_desc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FrmlDesc',
            fields=[
                ('idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('str_name', models.CharField(blank=True, max_length=80, null=True)),
                ('str_type', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'frml_desc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mtrc001dra000h0',
            fields=[
                ('idx_resource', models.IntegerField(primary_key=True, serialize=False)),
                ('idx_metric', models.IntegerField()),
                ('dbl_max', models.FloatField()),
                ('dte_max', models.IntegerField()),
            ],
            options={
                'db_table': '"PV_METRIC"."MTRC00_1DRA_000_H0"',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProbeDesc',
            fields=[
                ('idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('str_invariant', models.CharField(blank=True, max_length=255, null=True)),
                ('int_date', models.IntegerField(blank=True, null=True)),
                ('str_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('str_user', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'probe_desc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProbeType',
            fields=[
                ('idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('str_name', models.CharField(blank=True, max_length=80, null=True)),
                ('str_description', models.CharField(blank=True, max_length=255, null=True)),
                ('str_invariant_def', models.CharField(blank=True, max_length=1000, null=True)),
                ('str_class', models.CharField(blank=True, max_length=30, null=True)),
                ('int_date', models.IntegerField(blank=True, null=True)),
                ('str_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('str_user', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'probe_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PropDesc',
            fields=[
                ('idx_resource', models.IntegerField(primary_key=True, serialize=False)),
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
        migrations.CreateModel(
            name='RefDesc',
            fields=[
                ('ncl_idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('ncl_str_name', models.CharField(blank=True, max_length=80, null=True)),
                ('ncl_str_type', models.CharField(blank=True, max_length=32, null=True)),
                ('str_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('str_user', models.CharField(blank=True, max_length=80, null=True)),
                ('ncl_str_oid', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'ref_desc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SeDesc',
            fields=[
                ('idx_ind', models.IntegerField(primary_key=True, serialize=False)),
                ('str_alias', models.CharField(blank=True, max_length=255, null=True)),
                ('str_state', models.CharField(blank=True, max_length=3, null=True)),
                ('str_name', models.CharField(blank=True, max_length=255, null=True)),
                ('str_ulabel', models.CharField(blank=True, max_length=255, null=True)),
                ('idx_formula', models.IntegerField(blank=True, null=True)),
                ('idx_formula_group', models.IntegerField(blank=True, null=True)),
                ('str_type', models.CharField(blank=True, max_length=80, null=True)),
                ('str_type_data', models.CharField(blank=True, max_length=80, null=True)),
                ('str_instance', models.CharField(blank=True, max_length=255, null=True)),
                ('int_date', models.IntegerField(blank=True, null=True)),
                ('str_invariant', models.CharField(blank=True, max_length=140, null=True)),
                ('str_profile', models.CharField(blank=True, max_length=255, null=True)),
                ('idx_rule', models.IntegerField(blank=True, null=True)),
                ('str_origin', models.CharField(blank=True, max_length=80, null=True)),
                ('str_user', models.CharField(blank=True, max_length=80, null=True)),
                ('str_comment', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'se_desc',
                'managed': False,
            },
        ),
    ]
