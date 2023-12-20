from rest_framework import serializers
from .models import CustomUser
import random, string
from django.contrib.postgres.fields import JSONField
def generate_random_string(length=15):
    letters = string.ascii_letters  # includes uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))
class UserRegistrationSerializer(serializers.ModelSerializer):
      """ 
      This serializer will help to create new user's registration data and validate the password.
      """
      password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
      class Meta:
          model = CustomUser
          fields = (
                  '__all__'
              )

      def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if len(password) <= 7: raise serializers.ValidationError("Password's Length should be minimum 8 ")
        if password != password2:
          raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        return attrs


      def create(self, validated_data):
        created_user =CustomUser.objects.create_user(
            username = generate_random_string(),
            email = validated_data.get('email'),
            first_name = validated_data.get('first_name'),
            password= validated_data.get('password')
          )
        return created_user

class UserLoginSerializer(serializers.ModelSerializer):
  """ 
  A serializer for login user
  """
  email = serializers.EmailField(max_length=255)
  class Meta:
      model = CustomUser
      fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    """ 
    Get a login user's data and send data
    """
    class Meta:
        model = CustomUser
        fields =['email','first_name','is_user_verified','credit']

class UserChangePasswordSerializer(serializers.Serializer):
    """ 
    To change a password for user if they forget password
    """
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
