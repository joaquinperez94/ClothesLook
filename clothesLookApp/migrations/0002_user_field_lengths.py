from django.db import migrations, models


class Migration(migrations.Migration):
    """Align the user table with models.py.

    nickName (30 -> 50) and first_name (30 -> 60) were enlarged in models.py
    after 0001_initial was generated, so "makemigrations --check" reported
    pending changes.
    """

    dependencies = [
        ('clothesLookApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=60, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickName',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nick Name'),
        ),
    ]
