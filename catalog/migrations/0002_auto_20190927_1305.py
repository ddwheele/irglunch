# Generated by Django 2.2.5 on 2019-09-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostaction',
            name='comments',
            field=models.TextField(blank=True, help_text='Information about this IRG Lunch, ie, restaurant'),
        ),
        migrations.AlterField(
            model_name='person',
            name='num_guest_actions',
            field=models.IntegerField(default=1, help_text='Times person has attended IRG lunch'),
        ),
    ]
