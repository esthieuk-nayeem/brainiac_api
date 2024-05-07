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
import datetime

logger = logging.getLogger(__name__)


class TeacherBatchView(APIView):

    def post(self, request):
        try:
            data = request.data

            user_id = data.get("id")
            user = User.objects.get(id=user_id)

            batch = user.t_assigned_batches.all()
        

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
                    logger.info(f'{datetime.datetime.now()}users found in batch successfully!')

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
                                "id":fee.id,
                                "student_name": fee.student.full_name,
                                "month":fee.month.month_name,
                                "amount":fee.amount,
                                "fee_status":fee.fee_status
                            }

                        fee_data.append(_data)
                        logger.info(f"{datetime.datetime.now()}Student fees fetched successfully for batch.")


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
                                "id": payment.id,
                                "teacher_name": payment.user.full_name,
                                "month":payment.month.month_name,
                                "amount":payment.amount,
                                "fee_status":payment.payment_status
                            }

                        payment_data.append(_data)
                        logger.info(f"{datetime.datetime.now()}Teacher payments fetched successfully for batch.")



                except:
                    logger.error(f"{datetime.datetime.now()}An error occurred while fetching teacher payments: {e}")
                    payment_data = []



                i_data = {
                    "batch_id":batch_data[i]['id'],
                    "batch_name": batch_data[i]['batch_name'],
                    "assigned_course":batch_data[i]['assigned_course'],
                        "created_at": batch_data[i]['created_at'],
                        "active": batch_data[i]['active'],
                        "month": [{
                            "id": batch[i].month.id,
                            "name":batch[i].month.month_name
                                   }],
                        "t_assigned": t_data,
                        "s_enrolled": s_data,
                        "s_fee": fee_data,
                        "t_payment": payment_data,
                        "total_payment":sum(total_payment),
                        "total_fee":sum(total_fee),
                        "profit_loss": sum(total_fee) - sum(total_payment)

                        }
                response.append(i_data)
            logger.info(f'{datetime.datetime.now()}Batch data retrieved successfully.')
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An error occurred while processing batch data: {e}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
