from .models import *
from rest_framework import serializers

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = '__all__'

class SubSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubSection
        fields = '__all__'

class QuestionBankSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionBank
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'

class QuizSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizSection
        fields = '__all__'

class SectionQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionQuestion
        fields = '__all__'
    
class QuizEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizEnrollment
        fields = '__all__'

class UserQuizQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserQuizQuestion
        fields = '__all__'
