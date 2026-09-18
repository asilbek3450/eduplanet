from django.db import migrations


def add_subjects(apps, schema_editor):
    Category = apps.get_model('centers', 'Category')
    description = 'Matematika, fizika, biologiya, kimyo, tarix va boshqa fanlardan universitetga tayyorlov markazlari.'
    Category.objects.using(schema_editor.connection.alias).get_or_create(
        slug='subjects', defaults={
            'name': 'Fanlar', 'icon': '∑', 'description': description,
            'translations': {
                'name': {'uz': 'Fanlar', 'en': 'Academic subjects', 'ru': 'Учебные предметы'},
                'description': {
                    'uz': description,
                    'en': 'University preparation centers for mathematics, physics, biology, chemistry, history and other subjects.',
                    'ru': 'Подготовка к поступлению в университет: математика, физика, биология, химия, история и другие предметы.',
                },
            },
        },
    )


class Migration(migrations.Migration):
    dependencies = [('courses', '0011_primary_categories')]
    operations = [migrations.RunPython(add_subjects, migrations.RunPython.noop)]
