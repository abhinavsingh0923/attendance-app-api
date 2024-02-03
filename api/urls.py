from django.urls import path
from .views import *

urlpatterns = [
    path('faces/', faces.as_view(), name='faces'),
    # path('match_face/<int:batch_id>/<int:branch_id>/', match_face.as_view(), name='match_face'),
    path('students/<int:branch_id>/<int:batch_id>/', StudentList.as_view(), name='student-list'),
    path('attendance/<int:lecture_id>/', AttendanceAPIView.as_view(), name='attendance'),
    path('batches/', AllBatches.as_view(), name='all_batches'),
    path('branches/', AllBranchs.as_view(), name='all_branches'),
    path('courses/', AllCourses.as_view(), name='all_courses'),
    path('coursebyteacher/',AllCoursesbyTeacher.as_view(), name='teachercourse' ),
    path('course_attendance/<int:course_id>/<int:batch_id>/<int:branch_id>/', CourseAttendanceAPIView.as_view(), name='course_attendance'),
]
