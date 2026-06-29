from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('board', 'Category')

    categories = [
        {
            'name': 'free',
            'description': '자유 게시판',
            'has_answer': True,
        },
        {
            'name': 'qna',
            'description': '질문 게시판',
            'has_answer': True,
        },
        {
            'name': 'inquiry',
            'description': '문의 게시판',
            'has_answer': True,
        },
    ]

    for category in categories:
        Category.objects.update_or_create(
            name=category['name'],
            defaults={
                'description': category['description'],
                'has_answer': category['has_answer'],
            }
        )


def delete_default_categories(apps, schema_editor):
    Category = apps.get_model('board', 'Category')
    Category.objects.filter(name__in=['free', 'qna', 'inquiry']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0014_question_hits'),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories,
            delete_default_categories,
        ),
    ]