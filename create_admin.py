from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@marsit.local', 'admin123')
    print("✓ Admin user created: admin / admin123")
else:
    print("✓ Admin user already exists")
