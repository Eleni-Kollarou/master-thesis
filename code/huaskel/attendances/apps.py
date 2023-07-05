from django.apps import AppConfig

class AttendancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendances'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            from django.contrib.auth.models import Group, Permission
            from django.contrib.contenttypes.models import ContentType

            from .models import Course, CourseEvent

            print("Creating teacher group")
            restricted_group, _ = Group.objects.get_or_create(name='Teacher')

            # Assign permissions to the restricted group for Course
            content_type_course = ContentType.objects.get_for_model(Course)
            permissions_course = Permission.objects.filter(content_type=content_type_course)
            # restricted_group.permissions.set(permissions_course)

            # Assign permissions to the restricted group for CourseEvent
            content_type_course_event = ContentType.objects.get_for_model(CourseEvent)
            permissions_course_event = Permission.objects.filter(content_type=content_type_course_event)
            restricted_group.permissions.set(permissions_course | permissions_course_event)

 

