from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course
from shop.models import Product


def home(request):
    courses = Course.objects.all()[:6]
    products = Product.objects.all()[:8]
    context = {
        'courses': courses,
        'products': products,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    user = request.user
    courses = user.enrolled_courses.all() if hasattr(user, 'enrolled_courses') else []
    
    # Calculate total spent from all orders
    total_spent = sum(order.total for order in user.orders.all())
    
    context = {
        'courses': courses,
        'user': user,
        'total_spent': total_spent,
    }
    return render(request, 'dashboard.html', context)
