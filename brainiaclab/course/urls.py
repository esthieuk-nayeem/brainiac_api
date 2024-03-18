from django.urls import path
from .views.admin_views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view()),
    path('course/', CourseView.as_view()),
    path('batch/', BatchView.as_view()),
    path('all_students/',StudentListView.as_view()),
    path('all_teachers/',TeacherListView.as_view()),
    path('months/',MonthView.as_view()),
    path('addStudenttobatch/',AddStudentToBatch.as_view()),
    path('addTeachertobatch/',AddTeacherToBatch.as_view()),

    # path('admin_take_attendance/<int:batch_id>/', Admin_take_attendance, name='admin_take_attendance'),
    # path('admin_view_attendance/<int:batch_id>/', Admin_view_attendance, name='admin_view_attendance'),

    # path('admin_createbatch/', Admin_CreateBatch, name='admin_createbatch'),
    # path('admin_student_dashboard/', AdminStudentView, name='admin_student_dashboard'),
    # path('admin_createstudent/', Admin_CreateStudentView, name='admin_createstudent'),
    # path('admin_teacher_dashboard/', AdminTeacherView, name='admin_teacher_dashboard'),
    

    

]
