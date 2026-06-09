#!/bin/bash
# Setup script for Mars IT Django Project

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Creating superuser..."
echo "Creating admin user: admin, password: admin123"
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@marsit.local', 'admin123')
    print("Admin user created successfully!")
else:
    print("Admin user already exists!")
END

echo "Loading sample data..."
python manage.py shell << END
from django.contrib.auth.models import User
from courses.models import Course, Module, Lesson
from shop.models import Product

# Create sample courses
if Course.objects.count() == 0:
    admin_user = User.objects.get(username='admin')
    
    # Course 1
    course1 = Course.objects.create(
        title='HTML & CSS для начинающих',
        description='Научитесь создавать красивые веб-сайты с HTML и CSS',
        level='Beginner',
        instructor=admin_user,
        price=0
    )
    
    module1 = Module.objects.create(course=course1, title='Введение в HTML', order=1)
    Lesson.objects.create(module=module1, title='Что такое HTML?', lesson_type='video', order=1)
    Lesson.objects.create(module=module1, title='HTML структура', lesson_type='video', order=2)
    
    # Course 2
    course2 = Course.objects.create(
        title='Python для программистов',
        description='Освойте Python и создавайте мощные приложения',
        level='Intermediate',
        instructor=admin_user,
        price=0
    )
    
    module2 = Module.objects.create(course=course2, title='Основы Python', order=1)
    Lesson.objects.create(module=module2, title='Переменные и типы данных', lesson_type='video', order=1)
    
    # Course 3
    course3 = Course.objects.create(
        title='JavaScript для экспертов',
        description='Углубленное изучение JavaScript и асинхронного программирования',
        level='Advanced',
        instructor=admin_user,
        price=50000
    )
    
    module3 = Module.objects.create(course=course3, title='Продвинутый JS', order=1)
    Lesson.objects.create(module=module3, title='Async/Await', lesson_type='video', order=1)
    
    print("Courses created successfully!")

# Create sample products
if Product.objects.count() == 0:
    products = [
        {'name': 'Mars Pen', 'price': 49, 'category': 'pen', 'stock': 100},
        {'name': 'Keyboard Sticker', 'price': 49, 'category': 'sticker', 'stock': 50},
        {'name': 'Strobar', 'price': 49, 'category': 'sticker', 'stock': 30},
        {'name': 'Notepad', 'price': 149, 'category': 'notepad', 'stock': 25},
        {'name': 'Mars Rug', 'price': 149, 'category': 'rug', 'stock': 10},
        {'name': 'Keychain', 'price': 149, 'category': 'keychain', 'stock': 40},
        {'name': 'Phone Stand', 'price': 199, 'category': 'stand', 'stock': 15},
        {'name': 'Mug', 'price': 199, 'category': 'mug', 'stock': 20},
    ]
    
    for product_data in products:
        Product.objects.create(**product_data)
    
    print("Products created successfully!")

print("Sample data loaded!")
END

echo "Setup complete! You can now run: python manage.py runserver"
