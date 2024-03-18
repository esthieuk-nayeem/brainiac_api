from django.db import models
from authentication.models import User



class Day(models.Model):
    day_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.day_name
    


class Month(models.Model):
    month_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    day = models.ManyToManyField(Day)
    
    def __str__(self):
        return self.month_name


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    month = models.ManyToManyField(Month)

    def __str__(self):
        return self.course_name
    

class Batch(models.Model):
    batch_name = models.CharField(max_length=200)
    month = models.ForeignKey(Month, on_delete= models.CASCADE, null = True)
    assigned_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.batch_name    



class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    topic = models.CharField(null=True,max_length=250)

    def __str__(self):
        return f"{self.student.name}-{self.batch}"



class StudentFee(models.Model):
    STATUS_CHOICES = [
        ('Not Ready', 'Not Ready'),
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True, blank=True)
    fee_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Not Ready',
    )

    def __str__(self):
        return self.student.full_name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Not Ready', 'Not Ready'),
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Not Ready',
    )

    def __str__(self):
        return self.payment_status