from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length= 68, min_length = 6,write_only = True)

    class Meta:
        model = User
        fields = ['full_name',"phone","whatsapp_num","email","password"]

    def validate(self, attrs):
        email = attrs.get('phone','')
        phone = attrs.get('phone','')

        if not phone.isalnum():
            raise serializers.ValidationError("The phone should only conatain alphanumeric characters!")

        return attrs

    def create(self, validated_data):
    
        student_group, created = Group.objects.get_or_create(name='student')
        user = User.objects.create_user(**validated_data)
        user.save()

        
        user.groups.add(student_group)

        return user


class RegisterTeacherSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length= 68, min_length = 6,write_only = True)
    class Meta:
        model = User
        fields = ['full_name',"phone","whatsapp_num","email","password"]

    def validate(self, attrs):
        email = attrs.get('phone','')
        phone = attrs.get('phone','')

        if not phone.isalnum():
            raise serializers.ValidationError("The phone should only conatain alphanumeric characters!")

        return attrs

    def create(self, validated_data):
    
        teacher_group, created = Group.objects.get_or_create(name='teacher')
        user = User.objects.create_user(**validated_data)
        user.save()

        user.groups.add(teacher_group)

        return user





class RegisterAdminSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length= 68, min_length = 6,write_only = True)
    class Meta:
        model = User
        fields = ['full_name',"phone","whatsapp_num","email","password"]

    def validate(self, attrs):
        email = attrs.get('phone','')
        phone = attrs.get('phone','')

        if not phone.isalnum():
            raise serializers.ValidationError("The phone should only conatain alphanumeric characters!")

        return attrs

    def create(self, validated_data):
    
        admin_group, created = Group.objects.get_or_create(name='admin')
        user = User.objects.create_user(**validated_data)
        user.save()

       
        user.groups.add(admin_group)

        return user





        

class RegisterSuperUser(serializers.ModelSerializer):
    password = serializers.CharField(max_length= 68, min_length = 6,write_only = True)

    class Meta:
        model = User
        fields = ['email','username',"password","phone"]

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):
        admin_group = Group.objects.get_or_create(name="admin")
        print(admin_group)
        user = User.objects.create_superuser(**validated_data)

        user.groups.add(admin_group)
        return user




class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255,min_length=3)
    password = serializers.CharField(max_length = 68, min_length = 6,write_only=True)
    username = serializers.CharField(max_length = 255, min_length=3, read_only = True)
    tokens = serializers.CharField(max_length = 255, min_length=3, read_only = True)
    token = serializers.CharField(max_length = 255, min_length=3, read_only = True)
   



    class Meta:
        model = User
        fields = ["phone", "password",'username','tokens','token']


    def validate(self, attrs):
        phone = attrs.get('phone', '')
        password = attrs.get('password', '')

        _user = User.objects.get(phone=phone)
        
        user = auth.authenticate(phone=phone, password=password)

        

        if not user:
            raise AuthenticationFailed("Invalid Credentials!")

        if not user.is_active:
            raise AuthenticationFailed("Account Disabled, Contact Admin!")

        token = Token.objects.get(user=_user)
        print(token)

        return {
           
            'phone' : user.phone,
            'username': user.username,
            'tokens' : user.tokens(),
            'token': token.key
        }

      

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','is_varified']  # Include the 'phone' and 'is_varified' fields for updating

    



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad token")