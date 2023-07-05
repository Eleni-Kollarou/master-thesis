from django.db import models
from accounts.models import User
import datetime
from datetime import timezone


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    students = models.ManyToManyField(User, through="Enrollment")

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class CourseEvent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    duration = models.DurationField()

    def is_open(self):
        return self.date <= datetime.datetime.now(timezone.utc) <= (self.date + self.duration)

    def get_user_attendance(self, user):
        try:
            return self.attendance_set.get(user=user)
        except Attendance.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.course.code} event: {self.name}, at {self.date} (duration: {self.duration})"


class Attendance(models.Model):
    course_event = models.ForeignKey(CourseEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_registered = models.DateTimeField(auto_now_add=True)

    @property
    def course(self):
        return self.course_event.course

    def __str__(self):
        return f"{self.user.username} - {self.course_event} - {self.datetime_registered}"
