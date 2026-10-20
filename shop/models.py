from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField('Остаток на складе', default=0)
    available = models.BooleanField('В продаже', default=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Order(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=30)
    address = models.CharField('Адрес доставки', max_length=250)
    created = models.DateTimeField('Создан', auto_now_add=True)
    paid = models.BooleanField('Оплачен', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
