from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *



@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(StudentFaceModel)
class StudentFaceModelAdmin(admin.ModelAdmin):
    list_display = ['id_number', 'name', 'batch', 'branch']
    search_fields = ['name', 'id_number']
    list_filter = ['batch', 'branch']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'year', 'batch']
    search_fields = ['name', 'code']
    list_filter = ['batch']

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['date', 'course', 'batch', 'branch']
    list_filter = ['course', 'batch', 'branch']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['lecture', 'student', 'is_present']
    list_filter = ['lecture', 'is_present']
    search_fields = ['student__name', 'lecture__course__name']

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_courses']

    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])
    get_courses.short_description = 'Courses'