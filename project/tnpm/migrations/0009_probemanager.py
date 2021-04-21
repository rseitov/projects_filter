# Generated by Django 3.1.6 on 2021-02-17 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnpm', '0008_propdesc'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProbeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(db_column='Manager_Name', max_length=64, unique=True, verbose_name='Manager')),
                ('manager_server', models.CharField(db_column='Manager_Server', max_length=64)),
                ('filter_file_path', models.CharField(db_column='Filter_File_Path', max_length=254)),
                ('sftp_user_name', models.CharField(db_column='Sftp_user_name', max_length=64)),
                ('sftp_password', models.CharField(db_column='Sftp_password', max_length=64)),
                ('backup_server_ip', models.CharField(blank=True, db_column='Backup_Server_IP', max_length=64)),
                ('http_port', models.CharField(db_column='HTTP_Port', max_length=50)),
                ('http_username', models.CharField(db_column='HTTP_username', max_length=50)),
                ('http_password', models.CharField(db_column='HTTP_password', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_updated', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
            ],
            options={
                'verbose_name': 'probe manager',
                'verbose_name_plural': 'probe managers',
                'db_table': 'probemanager',
            },
        ),
    ]
