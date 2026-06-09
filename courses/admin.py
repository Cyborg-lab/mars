from django.contrib import admin
from django import forms
from django.core.validators import URLValidator
from .models import Course, Module, Lesson, normalize_video_url


class LessonAdminForm(forms.ModelForm):
    video_url = forms.CharField(
        required=False,
        label='Video URL',
        help_text='YouTube yoki Vimeo linkini kiriting. Masalan: youtube.com/watch?v=...',
    )

    class Meta:
        model = Lesson
        fields = '__all__'

    def clean_video_url(self):
        video_url = normalize_video_url(self.cleaned_data.get('video_url'))
        if video_url:
            URLValidator()(video_url)
        return video_url


class LessonInline(admin.TabularInline):
    model = Lesson
    form = LessonAdminForm
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'instructor', 'price']
    list_filter = ['level', 'created_at']
    search_fields = ['title', 'description']
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ['title', 'module', 'lesson_type', 'order']
    list_filter = ['lesson_type', 'module__course']
    search_fields = ['title', 'description', 'video_url']
