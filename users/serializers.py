from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password # django의 기본 패스워드 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token   # Token 모델
from rest_framework.validators import UniqueValidator   # 이메일 중복 방지를 위한 검증도구


class RegisterSerializer(serializers.ModelSerializer):
    '''
        회원가입 시리얼라이저  -> RegisterSerializer
        기존 User 테이블에 username, email, password 를 필수 항목으로 설정
    '''
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())], # 이메일에 대한 중복 검사
    )
    
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],  # 비밀번호에 대한 검증
    )
    
    '''
        비밀번호 확인을 위한 필드
    '''
    password2 = serializers.CharField(
        write_only = True,
        required = True,
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': '비밀번호가 서로 일치 하지 않습니다'}
            )
        return data
    
    def create(self, validated_data):
        '''
            Create 요청에 대해 Create 메서드 오버라이딩, User 을 생성하고 토큰을 생성함.
        '''
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user