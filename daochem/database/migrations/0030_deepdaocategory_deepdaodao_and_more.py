# Generated by Django 4.0.3 on 2022-09-08 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_blockchainaddress_record_modified_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeepdaoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('deepdao_id', models.CharField(max_length=36, unique=True)),
            ],
            options={
                'db_table': 'deepdao_categories',
            },
        ),
        migrations.CreateModel(
            name='DeepdaoDao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=50, null=True)),
                ('deepdao_id', models.CharField(max_length=36, unique=True)),
            ],
            options={
                'db_table': 'deepdao_daos',
            },
        ),
        migrations.RenameModel(
            old_name='DeepdaoAddress',
            new_name='DeepdaoAddressDeprecated',
        ),
        migrations.RemoveField(
            model_name='dao',
            name='deepdao_addresses',
        ),
        migrations.AlterModelTable(
            name='deepdaoaddressdeprecated',
            table='deepdao_addresses_deprecated',
        ),
    ]
