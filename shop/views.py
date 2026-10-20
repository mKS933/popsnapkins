from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Category, Order, OrderItem, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        messages.success(request, f'«{product.name}» добавлен в корзину.')
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'«{product.name}» удалён из корзины.')
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order/create.html', {'cart': cart, 'form': form})
