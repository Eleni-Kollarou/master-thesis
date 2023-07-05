from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .models import Course, CourseEvent, Attendance, Enrollment
from django.db.models import Q
import logging

# Create your views here.
logger = logging.getLogger('huaskel')

def message_success(msg):
    return {'type': 'success', 'message': msg}

def message_failure(msg):
    return {'type': 'danger', 'message': msg}

@login_required
def index(request):
    """
    Dashboard view
    """
    user = request.user
    username = user.username

    enrolled_courses = user.course_set.all()


    logger.info('User %s has accessed his dashboard' % username)

    return render(request, 'index.html', context = {'user' : user, 'enrolled_courses': enrolled_courses})


@login_required
def courses(request):
    user = request.user

    courses = Course.objects.all()

    return render(request, 'courses.html', context=
                  {'courses': courses,})


@login_required
def course(request, course_code):
    """
    Single course view
    """
    user = request.user
    course = get_object_or_404(Course, code=course_code)
    course_events_data = []
    msg = ""
    action = None
    target_course_event = None

    user_enrolled = user.course_set.filter(pk=course.pk).exists()

    if request.method == "POST":
        action = request.POST.get('course-action')
        target_course_event = request.POST.get('course_event')


    if action == 'enroll' and not user_enrolled:
        Enrollment.objects.create(course=course, user=user)
        user_enrolled = True
        msg = message_success("Εγγραφήκατε με επιτυχία!")
    elif action == 'disenroll' and user_enrolled:
        try:
            enr = Enrollment.objects.get(course=course, user=user)
            enr.delete()
            user_enrolled = False
            msg = message_success("Απεγγραφήκατε από το μάθημα")
        except Enrollment.DoesNotExist:
            pass

    if user_enrolled:
        course_events = CourseEvent.objects.filter(course=course).order_by('date')

        if target_course_event is not None:
            try:
                course_event = CourseEvent.objects.get(pk=target_course_event)
                enrolled = user.course_set.filter(pk=course_event.course.pk).exists()

                if not enrolled:
                    msg = message_failure("Δεν είσαι εγγεγραμένος στο μάθημα")
                elif course_event.get_user_attendance(user) is not None:
                    msg = message_failure("Έχεις ήδη παρουσία σε αυτό το γεγονός")
                else:
                    Attendance.objects.create(course_event=course_event, user=user)

            except CourseEvent.DoesNotExist:
                pass


        course_events_data = [
            {**model_to_dict(ce),
             'attended': ce.get_user_attendance(user),
             'is_open': ce.is_open()
             } for ce in course_events]

    return render(request, 'course.html', context=
                  {'course': course,
                   'user_enrolled': user_enrolled,
                   'course_events_data': course_events_data,
                   'msg': msg})

