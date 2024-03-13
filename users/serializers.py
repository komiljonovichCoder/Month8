from rest_framework import serializers
from .models import *
from .utils import *
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class SignUpSerializer(serializers.ModelSerializer):
    auth_type = serializers.CharField(required=False, read_only=True)
    auth_status = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('auth_type', 'auth_status')

    def validate_email_phone(self, email_phone):
        user = User.objects.filter(Q(email=email_phone) | Q(phone_number=email_phone))
        if user.exists():
            data = {'status': False, 'message': "Ushbu foydalanuvchi oldin ro'yhatdan o'tgan!"}
            raise ValidationError(data)
        return email_phone

    def validate(self, data):
        user_input = data.get('email_phone')
        email_or_phone = check_email_or_phone_number(user_input)

        if email_or_phone == 'Phone Number':
            data = {'auth_type':VIA_PHONE, 'phone_number': user_input}

        elif email_or_phone == 'Email Address':
            data = {'auth_type':VIA_EMAIL, 'email': user_input}

        else:
            data = {'status': False, 'message': 'Your data is incorrect!'}
            raise ValidationError(data)
        return data
    
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print(user)
        auth_type = validated_data.get('auth_type')
        if auth_type == VIA_EMAIL:
            code = user.create_confirmation_code(VIA_EMAIL)
            send_sms(code)
        elif auth_type == VIA_PHONE:
            code = user.create_confirmation_code(VIA_PHONE)
            send_sms(code)
        else: 
            data = {'status': False, 'message': 'Code yuborishda xatolik yuz berdi!'}
            raise ValidationError(data)
        return user
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data['access'] = instance.token()['access']
        data['refresh'] = instance.token()['refresh']
        return data