# Generated by Django 5.0.1 on 2024-02-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_houseunit_houseimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseunit',
            name='location',
            field=models.CharField(choices=[('JHR', 'Johor'), ('KDH', 'Kedah'), ('KTN', 'Kelantan'), ('MLK', 'Malacca'), ('NSN', 'Negeri Sembilan'), ('PHG', 'Pahang'), ('PRK', 'Perak'), ('PLS', 'Perlis'), ('PNG', 'Penang'), ('SBH', 'Sabah'), ('SWK', 'Sarawak'), ('SGR', 'Selangor'), ('TRG', 'Terengganu'), ('KUL', 'Kuala Lumpur'), ('LBN', 'Labuan'), ('PJY', 'Putrajaya')], default='KUL', max_length=255),
        ),
    ]
