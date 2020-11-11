# Generated by Django 3.1.2 on 2020-11-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_auto_20201110_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='calcium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='calories',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='carbohydrates',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='cholesterol',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat_monounsatured',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat_polyunsaturated',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat_saturated',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fat_trans',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='fibre',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='iron',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='potassium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='protein',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='sodium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='sugar',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='vitamin_a',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='vitamin_c',
            field=models.FloatField(null=True),
        ),
    ]
