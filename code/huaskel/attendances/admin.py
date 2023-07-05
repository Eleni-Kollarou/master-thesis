from django.contrib import admin
from .models import Course, CourseEvent, Attendance, Enrollment
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', '_course_attendants')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("<int:pk>/studentdata/", self.admin_site.admin_view(self.course_students_view))]
        return my_urls + urls

    def _course_attendants(self, obj):
        link = "<a href='{0}/studentdata'>Course Attendants</a>"
        return format_html(link, obj.id)

    def course_students_view(self, request, pk):
        # ...
        course_obj = Course.objects.get(pk=pk)
        print(course_obj)
        course_students = course_obj.students.all()
        print(course_students)
        # course_events = course_obj.course_events_set.get()
        course_events = CourseEvent.objects.filter(course=course_obj)
        print(course_events)

        res = []
        for student in course_students:
            attendances = 0
            for course_event in course_events:
                if course_event.get_user_attendance(student) is not None:
                    attendances += 1

            res.append({'student': student, 'attendances': attendances})

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            course_obj=course_obj,
            total_course_events=len(course_events),
            student_data=res
        )
        return TemplateResponse(request, "course_students.html", context)


class CourseEventAdmin(admin.ModelAdmin):
    list_filter = ["course"]

# Register your models here.
# admin.site.register(Course)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEvent, CourseEventAdmin)
admin.site.register(Attendance)
admin.site.register(Enrollment)
