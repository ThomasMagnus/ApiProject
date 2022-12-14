# Generated by Django 4.1.1 on 2022-09-27 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('table_row_index', models.IntegerField()),
                ('table_row_number', models.IntegerField()),
                ('order_num', models.IntegerField()),
                ('cost_usd', models.IntegerField()),
                ('cost_rub', models.IntegerField()),
                ('delivery_date', models.DateField()),
            ],
        ),
    ]
