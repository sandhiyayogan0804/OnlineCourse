from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Enrollment, Submission, Choice


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.get(
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_choices = request.POST.getlist("choice")

    for choice_id in selected_choices:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)

    return HttpResponseRedirect(
        reverse(
            "onlinecourse:show_exam_result",
            args=(course.id, submission.id)
        )
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    selected_choices = submission.choices.all()

    total_questions = course.lesson_set.count()
    correct_answers = selected_choices.filter(
        is_correct=True
    ).count()

    score = 0
    if total_questions > 0:
        score = int(
            correct_answers / total_questions * 100
        )

    context = {
        "course": course,
        "submission": submission,
        "selected_choices": selected_choices,
        "score": score,
    }

    return render(
        request,
        "onlinecourse/exam_result.html",
        context
    )
