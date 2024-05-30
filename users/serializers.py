from rest_framework import serializers
from users.models import Role, User



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class TokenUserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer()
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'contact', 'is_active', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.name = validated_data.get(
            'name', instance.name)
        instance.email = validated_data.get(
            'email', instance.email)

        instance.save()
        return instance
    
class UserLoginSerializer(serializers.Serializer):
    contact = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class UserLoginGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "role", "dob", "contact", "avtar", "email")

class UserSerializerDetailed(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "role", "dob", "contact", "avtar", "email")


class UserGerSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True, source="role")

    class Meta:
        model = User
        fields = ('id', 'contact', 'email', 'first_name', 'last_name', 'roles')