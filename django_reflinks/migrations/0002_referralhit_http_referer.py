# Generated by Django 2.0.2 on 2018-02-05 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("django_reflinks", "0001_initial"),
	]

	operations = [
		migrations.AddField(
			model_name="referralhit",
			name="http_referer",
			field=models.TextField(blank=True, help_text="Referer header at hit time"),
		),
	]
