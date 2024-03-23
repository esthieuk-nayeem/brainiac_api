from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from course.permissions import IsAdminUserPermission
from course import forms
from ..models import *
from ..serializers.serializers import *
import json
from django.core.exceptions import ObjectDoesNotExist  
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.serializers import DashboardSerializer, BatchSerializer
from ..models import Batch, StudentFee
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

# @swagger_auto_schema(
#     security=[{"Bearer": []}]
# )
class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUserPermission]
    def get(self, request):
        total_course = Course.objects.all().count()
        total_batch = Batch.objects.filter(active=True).count()
        total_student = User.objects.filter(groups=1).count()
        total_teacher = User.objects.filter(groups=2).count()
        student_fee = StudentFee.objects.filter(fee_status="Pending").count()
        teacher_payment = Payment.objects.filter(payment_status="Pending").count()

        context = {
            'total_active_course': total_course,
            'total_active_batch': total_batch,
            'active_students': total_student,
            'active_teachers': total_teacher,
            'pending_student_fee': student_fee, 
            'pending_payment': teacher_payment,
            
        }

        serializer = DashboardSerializer(context)
        data = serializer.data
        return Response(data)

class CourseView(APIView):
    def get(self, request):
        try:
            # Course calculation
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            course_data = serializer.data
            response = []

            for i in range(len(course_data)):
                t_batch = Batch.objects.filter(assigned_course=courses[i].id).count()
                t_month = courses[i].month.count()
                print(t_month)

                c_data = {
                    "id": courses[i].id,
                    "name": courses[i].course_name,
                    "t_batches": t_batch,
                    "t_month": t_month
                }

                response.append(c_data)

            logger.info('Course data retrieved successfully.')
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f'An error occurred: {str(e)}')
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def post(self, request):
        post_data = request.data
        serializer = CourseSerializer(data=post_data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data

        course_id = data.get("id")
        course_name = data.get("name")

        try:
            course = Course.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            return Response({"message": f"Updated the course name to {course_name}"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": f"Course with id {course_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        data = request.data
        course_id = data.get("id")

        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": f"Course with id {course_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)          



class BatchView(APIView):

    def get(self, request):
        try:
            batch = Batch.objects.all()

            serializer = BatchSerializer(batch,many=True)
            batch_data = serializer.data

            response = []

            for i in range(len(batch_data)):

                try:
                    t_assigned = User.objects.filter(t_assigned_batches=batch_data[i]['id'])
                    t_assigned_serializer = SubUserSerializer(t_assigned, many=True)
                    t_data = t_assigned_serializer.data

                    print(s_data)
                except ObjectDoesNotExist:
                    t_data = []
                    print("No users found for the batch.")
                except Exception as e:
                    logger.error(f"An error occurred while fetching student enrollments: {e}")
                    print(f"An error occurred: {e}")


                try:
                    s_enrolled = User.objects.filter(s_enrolled_batches=batch_data[i]['id'])
                    s_enrolled_serializer = SubUserSerializer(s_enrolled, many=True)
                    s_data = s_enrolled_serializer.data
                    logger.info('users found in batch successfully!')

                    print(s_data)
                except ObjectDoesNotExist:
                    s_data = []
                    logger.warning(f"No users found for the batch with id {batch.id}.")

                    print("No users found for the batch.")
                except Exception as e:
                    print(f"An error occurred: {e}")

                try:
                    total_fee = []
                    fee_data = []
                    s_fees = StudentFee.objects.filter(batch= batch_data[i]['id'])
                    for fee in s_fees:

                        if fee.fee_status == "Paid":
                            total_fee.append(fee.amount)


                        _data = {
                                "student_name": fee.student.full_name,
                                "month":fee.month.month_name,
                                "amount":fee.amount,
                                "fee_status":fee.fee_status
                            }

                        fee_data.append(_data)
                        logger.info(f"Student fees fetched successfully for batch.")


                except:
                    logger.error(f"An error occurred while fetching student fees")
                    fee_data = []

                try:
                    total_payment = []
                    payment_data = []
                    t_payment = Payment.objects.filter(batch= batch_data[i]['id'])
                    for payment in t_payment:

                        if payment.payment_status == "Paid":
                            total_payment.append(payment.amount)

                        _data = {
                                "teacher_name": payment.user.full_name,
                                "month":payment.month.month_name,
                                "amount":payment.amount,
                                "fee_status":payment.payment_status
                            }

                        payment_data.append(_data)
                        logger.info(f"Teacher payments fetched successfully for batch.")



                except:
                    logger.error(f"An error occurred while fetching teacher payments: {e}")
                    payment_data = []



                i_data = {
                    "batch_id":batch_data[i]['id'],
                    "batch_name": batch_data[i]['batch_name'],
                    "assigned_course":batch_data[i]['assigned_course'],
                        "created_at": batch_data[i]['created_at'],
                        "active": batch_data[i]['active'],
                        "month": batch[i].month.month_name,
                        "t_assigned": t_data,
                        "s_enrolled": s_data,
                        "s_fee": fee_data,
                        "t_payment": payment_data,
                        "total_payment":sum(total_payment),
                        "total_fee":sum(total_fee),
                        "profit_loss": sum(total_fee) - sum(total_payment)

                        }
                response.append(i_data)
            logger.info('Batch data retrieved successfully.')
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred while processing batch data: {e}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        post_data = request.data
        serializer = BatchSerializer(data=post_data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        data = request.data

        batch_id = data.get("id")
        batch_name = data.get("batch_name")
        batch_month = data.get("month")
        assigned_course = data.get("assigned_course")
        active_stat = data.get("active")

        ins_month = Month.objects.get(id=batch_month)
        ins_course = Course.objects.get(id=assigned_course)
    

        try:
            batch = Batch.objects.get(id=batch_id)
            batch.batch_name = batch_name
            batch.month = ins_month
            batch.assigned_course = ins_course
            batch.active = active_stat 
            batch.save()
            
            return Response({"message": f"Updated the Batch {batch_name}"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": f"Batch with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)



    def delete(self, request):
        data = request.data
        batch_id = data.get("id")

        try:
            batch = Batch.objects.get(id=batch_id)
            batch.delete()
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": f"Course with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)          



class AddStudentToBatch(APIView):


    def put(self, request):
        data = request.data

        user_id = data.get("id")
        batch_id = data.get("batch")

        try:
            user = User.objects.get(id=user_id)
            print(user.full_name)
            batch = Batch.objects.get(id=batch_id)
            print(batch.batch_name)
            user.s_enrolled_batches.add(batch)
            user.save()
            return Response({"message": f"Enrolled student {user_id} to the batch {batch_id}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Batch.DoesNotExist:
            return Response({"error": f"Batch with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)




class AddTeacherToBatch(APIView):


    def put(self, request):
        data = request.data

        user_id = data.get("id")
        batch_id = data.get("batch")

        try:
            user = User.objects.get(id=user_id)
            print(user.full_name)
            batch = Batch.objects.get(id=batch_id)
            print(batch.batch_name)
            user.t_assigned_batches.add(batch)
            user.save()
            return Response({"message": f"Enrolled student {user_id} to the batch {batch_id}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"User with id {user_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Batch.DoesNotExist:
            return Response({"error": f"Batch with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)




class MonthView(APIView):
    def get(self, request):

        batch = Month.objects.all()
        serializer = MonthSerializer(batch,many=True)

        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)




class StudentListView(APIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone', 'full_name']  

    def get(self, request):
        
        students = User.objects.filter(groups__id=1)
        query = request.query_params.get('search', None)
        if query is not None:
            students = students.filter(phone__icontains=query) | students.filter(full_name__icontains=query)
       

        serializer = UserSerializer(students, many=True)
        data = serializer.data
      
        response = []
        for i in range(len(data)):


            try:
                if data[i]['s_enrolled_batches']:
                    batch_id = data[i]['s_enrolled_batches'][0]
                    enrolled_batch = Batch.objects.get(id=batch_id)

                    batch_name = enrolled_batch.batch_name
                    batch_month = enrolled_batch.month.month_name
                else:
                    # Handle the case where 's_enrolled_batches' list is empty
                    # You might want to define default values for batch_name and batch_month or take other appropriate actions.
                    batch_name = ''
                    batch_month = ''

            except IndexError:
                return Response({"error": "Index out of range"}, status=status.HTTP_400_BAD_REQUEST)

            except Batch.DoesNotExist:
                return Response({"error": f"Batch with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

            print(data[i]["id"])
            print(students[i])
        
            fee = StudentFee.objects.filter(student_id=data[i]["id"])

            f_serializer = FeeSerializer(fee, many=True)
            f_data = f_serializer.data

            print(f_data)


            i_data = {"id":data[i]['id'],
                     "full_name": data[i]['full_name'],
                      "phone": data[i]['phone'],
                      "whatsapp_num": data[i]['whatsapp_num'],
                      "email": data[i]['email'],
                      "s_status": data[i]['s_status'],
                      "s_fees": data[i]['s_fees'],
                      "created_at": data[i]['created_at'],
                      "last_login": data[i]['last_login'],
                      "batch": batch_name,
                      "months": batch_month,
                      "payments": f_data
                      }
            response.append(i_data)

        return Response(response, status=status.HTTP_200_OK)





class TeacherListView(APIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone', 'full_name']  


    def get(self, request):
        
        teacher = User.objects.filter(groups__id=2)
        query = request.query_params.get('search', None)
        if query is not None:
            teacher = teacher.filter(phone__icontains=query) | teacher.filter(full_name__icontains=query)
       
        serializer = UserSerializer(teacher, many=True)
        data = serializer.data
      
        response = []
        for i in range(len(data)):
            try:
                if data[i]['t_assigned_batches']:
                    batch_id = data[i]['t_assigned_batches'][0]
                    assigned_batch = Batch.objects.get(id=batch_id)

                    batch_name = assigned_batch.batch_name if assigned_batch.batch_name is not None else ''
                    batch_month = assigned_batch.month.month_name if assigned_batch.month is not None else ''
                else:
                    # Handle the case where 't_assigned_batches' list is empty
                    # You might want to define default values for batch_name and batch_month or take other appropriate actions.
                    batch_name = ''
                    batch_month = ''

            except IndexError:
                return Response({"error": "Index out of range"}, status=status.HTTP_400_BAD_REQUEST)

            except Batch.DoesNotExist:
                return Response({"error": f"Batch with id {batch_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

            print(data[i]["id"])
            print(teacher[i])
        
            fee = Payment.objects.filter(user_id=data[i]["id"])

            t_serializer = PaymentSerializer(fee, many=True)
            t_data = t_serializer.data
            print(t_data)

            i_data = {
                      "id":data[i]['id'],
                      "full_name": data[i]['full_name'],
                      "phone": data[i]['full_name'],
                      "whatsapp_num": data[i]['whatsapp_num'],
                      "email": data[i]['email'],
                      "s_status": data[i]['s_status'],
                      "s_fees": data[i]['s_fees'],
                      "created_at": data[i]['created_at'],
                      "last_login": data[i]['last_login'],
                      "batch": batch_name,
                      "months": batch_month,
                      "payments": t_data
                      }
            response.append(i_data)
        
        return Response(response, status=status.HTTP_200_OK)




class AttendanceView(APIView):
    def post(self,request):
        post_data = request.data
        batch_id = post_data.get('batch')

        distinct_dates = Attendance.objects.filter(batch=batch_id).values_list('created_at', flat=True).distinct()

        res_data = []

        for date in distinct_dates:
            # Filter Attendance objects for each date
            attendance_objects = Attendance.objects.filter(batch=batch_id, created_at=date)
            serializer = AttendanceSerializer(attendance_objects, many=True)
            res_data.append(serializer.data)

        return Response(res_data, status=status.HTTP_200_OK)




# def Admin_take_attendance(request,batch_id):
   
#     students = Batch.objects.filter(enrolled_batches=batch_id)
#     student_count = Batch.objects.filter(enrolled_batches=batch_id).count()
#     batch = Batch.objects.filter(id = batch_id)
#     attendance_count = Attendance.objects.filter(batch=batch_id).count()
#     month = Month.objects.all()
#     aform = forms.AttendanceForm()
   
#     if request.method == 'POST':
#         form = forms.AttendanceForm(request.POST)
#         if form.is_valid():
#             attendances = request.POST.getlist('present_status')
#             topic = request.POST.getlist('topic')
#             for i in range(len(attendances)):
#                 AttendanceModel = Attendance()
#                 AttendanceModel.batch = batch[0]
#                 AttendanceModel.present = True if attendances[i] == "Present" else False
#                 AttendanceModel.student = students[i]
#                 AttendanceModel.topic = topic[0]

#                 AttendanceModel.save()
            
#             if attendance_count == student_count * 12 :
#                 for i in range(len(attendances)):

#                     st_fee = students[i].fees


#                     StudentFeeModel = StudentFee()
#                     StudentFeeModel.batch = batch[0]
#                     StudentFeeModel.student = students[i]
#                     StudentFeeModel.amount = st_fee
#                     StudentFeeModel.month = month[1]
#                     StudentFeeModel.fee_status = "Pending"
#                     StudentFeeModel.save()
                    

#             return redirect('admin_attendance')
#         else:
#             print('form invalid')


#     context = {'students' : students, 'aform':aform}
#     return render(request, 'course/admin_take_attendance.html', context)




# def Admin_view_attendance(request, batch_id):
    
#     # Filter distinct dates for a specific batch
#     distinct_dates = Attendance.objects.filter(batch=batch_id).values_list('created_at', flat=True).distinct()
   
#     count_dates = Attendance.objects.filter(batch=batch_id).values_list('created_at', flat=True).distinct().count()

#     # Filter students enrolled in the batch
#     dt_students = User.objects.filter(s_enrolled_batches=batch_id)
#     count_students = User.objects.filter(s_enrolled_batches=batch_id).count()

#     # Filter attendance based on batch and distinct dates
#     dt_attendance = Attendance.objects.filter(batch=batch_id, created_at__in=distinct_dates)
  


#     context = {'dates' : distinct_dates,
#                'students':dt_students,
#                'attendances' : dt_attendance,
#                'limit':count_students
            
#                }
#     return render(request, 'course/admin_view_attendance.html', context)



# def Admin_CreateBatch(request):
#     aform = forms.CreateBatchForm()

#     if request.method == 'POST':
#         form = forms.CreateBatchForm(request.POST)

#         if form.is_valid():
#             batch_name = form.cleaned_data['batch_name']
#             assigned_course = form.cleaned_data['assigned_course']
            
#             batch_model = Batch()
#             batch_model.batch_name = batch_name
#             batch_model.assigned_course = assigned_course
#             batch_model.active = True
#             batch_model.save()

#             return redirect('admin_dashboard')

#     context = {
#         'aform': aform
#     }
#     return render(request, 'course/admin_createbatch.html', context)


# def AdminStudentView(request):
#     student = User.objects.filter(s_status=True).count()
#     pending_fee = StudentFee.objects.filter(fee_status='Pending').count()

#     from django.db.models import Count, Prefetch, Max, Sum
    

#     students_data = (
#         User.objects
#         .annotate(
#             num_attendances=Count('attendance'),
#             latest_attendance_date=Max('attendance__created_at'),
#             total_fees=Sum('studentfee__amount'),
#             latest_fee_month=Max('studentfee__month'),
#             latest_fee_status=Max('studentfee__fee_status'),
        
#         )
#         .prefetch_related(
#             Prefetch('attendance_set', queryset=Attendance.objects.order_by('-created_at')),
#             Prefetch('studentfee_set', queryset=StudentFee.objects.order_by('-month__name'))
#         )
#         .values('id','name', 'mobile', 'fees', 'status','enrolled_batches__batch_name',
#                 'num_attendances', 'latest_attendance_date', 'total_fees',
#                  'latest_fee_status')
#     )

#     students_list = list(students_data)


#     print(students_data)
#     print(students_list)


#     context = {'t_students' : student,
#                't_pending_fee':pending_fee,
#                'st_data': students_data,
#                'st_datalist': students_list}
#     return render(request, 'course/admin_student_dashboard.html', context)



# def Admin_CreateStudentView(request):
#     aform = forms.CreateStudentForm()

#     if request.method == 'POST':
#         form = forms.CreateStudentForm(request.POST)

#         if form.is_valid():
#             st_name = form.cleaned_data['name']
#             enrolled_batches = form.cleaned_data['enrolled_batches']
#             mobile = form.cleaned_data['mobile']
#             fees = form.cleaned_data['fees']
            
#             st_model = Student()
#             st_model.name = st_name
#             st_model.mobile = mobile
#             st_model.fees = fees
#             st_model.save()

#             st_model.enrolled_batches.set(enrolled_batches)

#             return redirect('admin_student_dashboard')

#     context = {
#         'aform': aform
#     }
#     return render(request, 'course/admin_createstudent.html', context)




# def AdminTeacherView(request):
#     teacher = Teacher.objects.filter(status=True).count()
#     pending_payment = Payment.objects.filter(payment_status='Pending').count()
    
#     from django.db.models import Count, Sum,Subquery, Max, F, OuterRef,Prefetch,  Case, When, IntegerField
    
    
#     batch_count_subquery = (
#     Teacher.objects
#     .filter(user=OuterRef('user'))
#     .values('user')
#     .annotate(batch_count=Count('assigned_batches'))
#     .values('batch_count')
# )


#     teacher_data = (
#         Teacher.objects
#         .annotate(
#             total_payment=Sum( 
#                 Case(
#                 When(payment__payment_status='Paid', then=F('payment__amount')),
#                 default=0,
#                 output_field=IntegerField()
#             )),
#             total_pending_payment_count=Count(
#             Case(
#                 When(payment__payment_status='Pending',then=1),
#                 default=None,
#                 output_field=IntegerField()
#             )
#         ),
#             latest_payment_status=Max('payment__payment_status'),
#             batch_count=Subquery(batch_count_subquery)
            
#         )
#         .prefetch_related(
#             Prefetch('payment_set', queryset=Payment.objects.order_by('-month__name'))
#         )
#         .values(
#             'id',
#             'user__username',
#             'salary',
#             'status',
#             'batch_count',
#             'total_pending_payment_count',
#             'total_payment',
#             'latest_payment_status',
#         )
       
#     )


#     teacher_list = list(teacher_data)


#     print(teacher_data)


#     context = {'t_teacheer' : teacher,
#                't_pending_payment':pending_payment,
#                'tr_data': teacher_data,
#                'tr_datalist': teacher_list}
#     return render(request, 'course/admin_teacher_dashboard.html', context)


