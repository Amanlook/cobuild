from .models import *
from rest_framework import serializers


class ObservationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationCategory
        fields = '__all__'
        

class ObservationKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationKey
        fields = '__all__'
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ObservationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationReport
        fields = '__all__'
        
class ObservationReportKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservationReportKey
        fields = '__all__'

class UserReportEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReportEnrollment
        fields = '__all__'
        

class  UserReportEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReportKeyPoint
        fields = '__all__'
        

        
        


        
        

        
