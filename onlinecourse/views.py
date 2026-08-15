from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Enrollment, Submission, Choice, Question


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

    selected_ids = list(
        submission.choices.values_list("id", flat=True)
    )

    questions = Question.objects.filter(
        lesson__course=course
    )

    total_score = 0

    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += 1

    possible_score = questions.count()

    grade = 0
    if possible_score > 0:
        grade = int(
            total_score / possible_score * 100
        )

    possible = grade >= 70

    context = {
        "course": course,
        "submission": submission,
        "selected_ids": selected_ids,
        "total_score": total_score,
        "possible_score": possible_score,
        "grade": grade,
        "possible": possible,
        "score": grade,
        "passed": possible,
        "selected_choices": submission.choices.all(),
    }

    return render(
        request,
        "onlinecourse/exam_result.html",
        context
    )