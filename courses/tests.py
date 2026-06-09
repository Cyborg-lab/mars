from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Course, Lesson, Module, get_video_embed_url, normalize_video_url


class VideoUrlTests(TestCase):
    def test_normalizes_urls_without_scheme(self):
        self.assertEqual(
            normalize_video_url('youtube.com/watch?v=abc123'),
            'https://youtube.com/watch?v=abc123',
        )

    def test_converts_youtube_watch_url_to_embed_url(self):
        self.assertEqual(
            get_video_embed_url('https://www.youtube.com/watch?v=abc123'),
            'https://www.youtube.com/embed/abc123',
        )

    def test_converts_youtube_short_url_to_embed_url(self):
        self.assertEqual(
            get_video_embed_url('https://youtu.be/abc123'),
            'https://www.youtube.com/embed/abc123',
        )


class LessonViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='password123')
        self.instructor = User.objects.create_user(username='teacher', password='password123')
        self.course = Course.objects.create(
            title='Python',
            description='Python course',
            level='Beginner',
            instructor=self.instructor,
        )
        self.module = Module.objects.create(course=self.course, title='Intro', order=1)
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='Start',
            lesson_type='video',
            video_url='https://www.youtube.com/watch?v=abc123',
            order=1,
        )
        self.course.students.add(self.user)

    def test_lesson_view_uses_embed_url(self):
        self.client.login(username='student', password='password123')

        response = self.client.get(
            reverse('lesson_view', args=[self.course.pk, self.module.pk, self.lesson.pk])
        )

        self.assertContains(response, 'https://www.youtube.com/embed/abc123')

    def test_post_marks_lesson_and_module_complete(self):
        self.client.login(username='student', password='password123')

        response = self.client.post(
            reverse('lesson_view', args=[self.course.pk, self.module.pk, self.lesson.pk])
        )

        self.assertRedirects(
            response,
            reverse('lesson_view', args=[self.course.pk, self.module.pk, self.lesson.pk]),
        )
        self.lesson.refresh_from_db()
        self.module.refresh_from_db()
        self.assertTrue(self.lesson.completed)
        self.assertTrue(self.module.completed)
