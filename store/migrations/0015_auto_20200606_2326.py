# Generated by Django 3.0.7 on 2020-06-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default='Customer', max_length=50, null=True),
        ),
    ]
