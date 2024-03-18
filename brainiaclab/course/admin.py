from django.contrib import admin
from .models import Course, Batch, Month, Day, Attendance,Payment, StudentFee



admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Month)
admin.site.register(Day)
admin.site.register(Attendance)
admin.site.register(Payment)
admin.site.register(StudentFee)