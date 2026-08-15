from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Submission,
    Enrollment,
)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'lesson']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course']


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)