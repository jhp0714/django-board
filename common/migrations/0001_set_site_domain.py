from django.db import migrations


def set_site_domain(apps, schema_editor):
    site_model = apps.get_model('sites', 'Site')

    site_model.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'django-board.kro.kr',
            'name': 'django-board',
        },
    )


def reset_site_domain(apps, schema_editor):
    site_model = apps.get_model('sites', 'Site')

    site_model.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'example.com',
            'name': 'example.com',
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(
            set_site_domain,
            reset_site_domain,
        ),
    ]