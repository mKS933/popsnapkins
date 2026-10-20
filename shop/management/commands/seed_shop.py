from django.core.management.base import BaseCommand

from shop.models import Category, Product

TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def slugify_ru(text):
    result = []
    for ch in text.lower():
        if ch in TRANSLIT:
            result.append(TRANSLIT[ch])
        elif ch.isalnum():
            result.append(ch)
        else:
            result.append('-')
    slug = ''.join(result)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')

CATEGORIES = {
    'paper': ('Бумажные салфетки', [
        ('Салфетки бумажные однослойные', 'Классические белые салфетки для дома, упаковка 100 шт.', '35.00', 200),
        ('Салфетки бумажные двухслойные', 'Мягкие двухслойные салфетки, упаковка 100 шт.', '55.00', 150),
        ('Салфетки с рисунком Новый год', 'Праздничные бумажные салфетки для декупажа и стола, 20 шт.', '45.00', 80),
    ]),
    'napkin-luncheon': ('Салфетки для сервировки', [
        ('Салфетки-ланч однотонные', 'Плотные бумажные салфетки для сервировки стола, 33х33 см, 20 шт.', '65.00', 120),
        ('Салфетки тканевые многоразовые', 'Хлопковые салфетки для сервировки, набор 6 шт.', '210.00', 40),
    ]),
    'wet': ('Влажные салфетки', [
        ('Влажные салфетки универсальные', 'Освежающие влажные салфетки, упаковка 15 шт.', '28.00', 300),
        ('Влажные салфетки антибактериальные', 'С антибактериальным эффектом, упаковка 20 шт.', '39.00', 250),
    ]),
}


class Command(BaseCommand):
    help = 'Заполняет каталог тестовыми категориями и товарами салфеток'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        for cat_slug, (cat_name, products) in CATEGORIES.items():
            category, _ = Category.objects.get_or_create(slug=cat_slug, defaults={'name': cat_name})
            for name, description, price, stock in products:
                Product.objects.get_or_create(
                    slug=slugify_ru(name),
                    defaults={
                        'category': category,
                        'name': name,
                        'description': description,
                        'price': price,
                        'stock': stock,
                        'available': True,
                    },
                )

        self.stdout.write(self.style.SUCCESS(f'Товаров создано: {Product.objects.count()}'))
