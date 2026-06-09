from django.db import models
from django.contrib.auth.models import User
from urllib.parse import parse_qs, urlparse


def normalize_video_url(url):
    if not url:
        return ''

    normalized_url = url.strip()
    if normalized_url and '://' not in normalized_url:
        normalized_url = f'https://{normalized_url}'
    return normalized_url


def get_video_embed_url(url):
    normalized_url = normalize_video_url(url)
    if not normalized_url:
        return ''

    parsed_url = urlparse(normalized_url)
    hostname = (parsed_url.hostname or '').lower()
    if hostname.startswith('www.'):
        hostname = hostname[4:]

    video_id = ''
    path_parts = [part for part in parsed_url.path.split('/') if part]

    if hostname in {'youtube.com', 'm.youtube.com', 'music.youtube.com'}:
        if parsed_url.path == '/watch':
            video_id = parse_qs(parsed_url.query).get('v', [''])[0]
        elif path_parts and path_parts[0] in {'embed', 'shorts', 'live'} and len(path_parts) > 1:
            video_id = path_parts[1]
    elif hostname == 'youtu.be' and path_parts:
        video_id = path_parts[0]

    if video_id:
        return f'https://www.youtube.com/embed/{video_id}'

    if hostname == 'vimeo.com' and path_parts and path_parts[0].isdigit():
        return f'https://player.vimeo.com/video/{path_parts[0]}'

    return normalized_url


class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    @property
    def progress(self):
        modules = self.modules.all()
        if not modules.exists():
            return 0
        completed = modules.filter(completed=True).count()
        return int((completed / modules.count()) * 100)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    content = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    order = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def video_embed_url(self):
        return get_video_embed_url(self.video_url)
