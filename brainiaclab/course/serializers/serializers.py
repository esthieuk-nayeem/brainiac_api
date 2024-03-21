from rest_framework import serializers
from ..models import *

class DashboardSerializer(serializers.Serializer):
        total_active_course = serializers.IntegerField()
        total_active_batch = serializers.IntegerField()
        active_students = serializers.IntegerField()
        active_teachers = serializers.IntegerField()
        pending_student_fee = serializers.IntegerField()
        pending_payment = serializers.IntegerField()




class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'month']



class BatchSerializer(serializers.ModelSerializer):
    assigned_course = CourseSerializer()
    class Meta:
        model = Batch
        fields = ['assigned_course','id','batch_name','month','created_at','active']



class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = '__all__'


class SubUserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id','full_name','phone']



class FeeSerializer(serializers.ModelSerializer):
     class Meta:
          model = StudentFee
          fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
     class Meta:
          model = Payment
          fields = '__all__'



class MonthSerializer(serializers.ModelSerializer):
     class Meta:
          model = Month
          fields = '__all__'



