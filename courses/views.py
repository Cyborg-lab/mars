from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson


def course_list(request):
    level = request.GET.get('level', '')
    courses = Course.objects.all()
    
    if level:
        courses = courses.filter(level=level)
    
    context = {
        'courses': courses,
        'levels': ['Beginner', 'Intermediate', 'Advanced'],
        'selected_level': level,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    modules = course.modules.all()
    is_enrolled = request.user in course.students.all() if request.user.is_authenticated else False
    
    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user not in course.students.all():
        course.students.add(request.user)
        messages.success(request, f'You have enrolled in {course.title}')
    else:
        messages.info(request, 'You are already enrolled in this course')
    return redirect('course_detail', pk=pk)


@login_required
def lesson_view(request, course_pk, module_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    module = get_object_or_404(Module, pk=module_pk, course=course)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, module=module)
    
    is_enrolled = request.user in course.students.all()
    
    if not is_enrolled:
        messages.error(request, 'You must be enrolled in this course')
        return redirect('course_detail', pk=course_pk)
    
    context = {
        'course': course,
        'module': module,
        'lesson': lesson,
        'modules': course.modules.all(),
    }
    return render(request, 'courses/lesson_view.html', context)
