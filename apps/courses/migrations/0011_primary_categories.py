from django.db import migrations


def consolidate_categories(apps, schema_editor):
    Category = apps.get_model('centers', 'Category')
    Center = apps.get_model('centers', 'LearningCenter')
    Course = apps.get_model('courses', 'Course')
    alias = schema_editor.connection.alias
    definitions = [
        ('it', 'IT', '</>', 'Dasturlash, sun’iy intellekt va texnologiyalar bo‘yicha amaliy ta’lim markazlari.', 'Practical learning centers for programming, AI and technology.', 'Учебные центры программирования, ИИ и технологий.'),
        ('design', 'Dizayn', 'UI', 'Grafik dizayn, UI/UX va ijodiy ko‘nikmalarni rivojlantiruvchi ta’lim markazlari.', 'Learning centers for graphic design, UI/UX and creative skills.', 'Учебные центры графического дизайна, UI/UX и творчества.'),
        ('marketing', 'Marketing', 'M', 'SMM, raqamli marketing va brend rivojlantirishni o‘rgatuvchi ta’lim markazlari.', 'Learning centers for SMM, digital marketing and brand development.', 'Учебные центры SMM, цифрового маркетинга и развития бренда.'),
        ('languages', 'Til', 'Aa', 'Chet tillari, erkin muloqot va til imtihonlariga tayyorlovchi ta’lim markazlari.', 'Learning centers for languages, conversation and exam preparation.', 'Языковые центры разговорной практики и подготовки к экзаменам.'),
    ]
    for slug, name, icon, uz, en, ru in definitions:
        Category.objects.using(alias).update_or_create(slug=slug, defaults={
            'name': name, 'icon': icon, 'description': uz,
            'translations': {'name': {'uz': name, 'en': {'design': 'Design', 'languages': 'Languages'}.get(slug, name), 'ru': {'it': 'IT', 'design': 'Дизайн', 'marketing': 'Маркетинг', 'languages': 'Языки'}[slug]}, 'description': {'uz': uz, 'en': en, 'ru': ru}},
        })
    mapping = {'web-development': 'it', 'backend-engineering': 'it', 'data-science': 'it', 'devops': 'it', 'frontend': 'it', 'backend': 'it', 'mobile': 'it', 'data-ai': 'it', 'smm': 'marketing'}
    for old_slug, new_slug in mapping.items():
        old = Category.objects.using(alias).filter(slug=old_slug).first()
        if not old:
            continue
        target = Category.objects.using(alias).get(slug=new_slug)
        for center in Center.objects.using(alias).filter(categories=old):
            center.categories.add(target)
        Course.objects.using(alias).filter(category=old).update(category=target)


class Migration(migrations.Migration):
    dependencies = [('courses', '0010_language_category')]
    operations = [migrations.RunPython(consolidate_categories, migrations.RunPython.noop)]
