# Generated by Django 3.1.2 on 2020-12-03 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Matchmaking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('num_players', models.PositiveIntegerField(default=0)),
                ('client1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='client1_match', to=settings.AUTH_USER_MODEL)),
                ('client2', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client2_match', to=settings.AUTH_USER_MODEL)),
                ('client3', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client3_match', to=settings.AUTH_USER_MODEL)),
                ('client4', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client4_match', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('turn', models.CharField(default='game_not_started', max_length=20)),
                ('board', models.CharField(max_length=5000)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('score_1', models.IntegerField(default=0)),
                ('score_2', models.IntegerField(default=0)),
                ('score_3', models.IntegerField(default=None, null=True)),
                ('score_4', models.IntegerField(default=None, null=True)),
                ('client1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='client1_game', to=settings.AUTH_USER_MODEL)),
                ('client2', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='client2_game', to=settings.AUTH_USER_MODEL)),
                ('client3', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client3_game', to=settings.AUTH_USER_MODEL)),
                ('client4', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client4_game', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
