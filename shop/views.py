from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem


def shop_list(request):
    category = request.GET.get('category', '')
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    
    categories = [choice[0] for choice in Product._meta.get_field('category').choices]
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'shop/shop_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart')
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context)


@login_required
def remove_from_cart(request, item_pk):
    cart_item = get_object_or_404(CartItem, pk=item_pk, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart')
    return redirect('cart_view')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('shop_list')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            total=cart.get_total(),
            status='pending'
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', pk=order.pk)
    
    context = {
        'cart': cart,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def order_list(request):
    orders = request.user.orders.all()
    context = {
        'orders': orders,
    }
    return render(request, 'shop/order_list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'shop/order_detail.html', context)
