# Generated by Django 3.1.2 on 2020-12-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_auto_20201208_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestate',
            name='last_move',
            field=models.DateTimeField(default=1607442186.1610126, verbose_name='last_move'),
        ),
    ]
