# Generated by Django 3.1 on 2020-08-16 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200816_1058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bestdeal',
            options={'ordering': ['sub_category', 'category']},
        ),
        migrations.AddField(
            model_name='bestdeal',
            name='sub_category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]