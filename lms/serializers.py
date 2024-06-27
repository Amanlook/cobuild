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

class CourseCategorySerliazer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields = '__all__'
        
class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseSection
        fields = '__all__'

class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseContent
        fields = '__all__'

class CourseContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseContentFile
        fields = '__all__'

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseEnrollment
        fields = '__all__'




        

    