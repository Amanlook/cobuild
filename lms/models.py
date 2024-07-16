from django.db import models

from users.models import User

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='section'


class SubSection(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='sub_section'

class Skill(models.Model):
    skill=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
            db_table ='skills'

class SubSkill(models.Model):
    skill=models.ForeignKey(to=Skill,null=True,blank=True,on_delete=models.CASCADE,related_name="sub_skills")
    sub_skill=models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    
    class Meta:
            db_table ='sub_skills'
    

class BloomsTaxonomy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class QuestionBank(models.Model):

    QUESTION_TYPE_CHOICE = (
        ('mcq', 'mcq'),
        ('lq', 'lq'),
        ('tf', 'tf'),
        ('sa','sa'),
    )
    DIFFICULTY_LEVEL=(
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )

    question_type = models.CharField(max_length=255, choices=QUESTION_TYPE_CHOICE, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.IntegerField(default=0)
    time = models.IntegerField(default=0) # in seconds
    difficulty_level=models.CharField(default="easy", choices=DIFFICULTY_LEVEL,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    skills=models.ManyToManyField(Skill)
    sub_skills=models.ManyToManyField(SubSkill)
    blooms_taxonomy=models.ManyToManyField(BloomsTaxonomy)

    class Meta:
        db_table ='question_bank'

class Option(models.Model):
    option = models.TextField(null=True, blank=True)
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='option'


class Quiz(models.Model):
    
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=0)
    passing_marks = models.IntegerField(default=0)
    number_of_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_time_bound = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    price = models.FloatField(null=True, blank=True)

    class Meta:
        db_table ='quiz'


class QuizSection(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    number_of_questions = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    time = models.IntegerField(default=0) # in seconds
    is_deleted=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table ='quiz_section'

class SectionQuestion(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.IntegerField(default=0)
    time = models.IntegerField(default=0) # in seconds
    is_deleted=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table ='section_question'

class QuizEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    marks = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    is_attempted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table ='section_enrollment'

class UserQuizQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, null=True, blank=True)
    user_answer = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table ='user_quiz_question'

class CourseCategory(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table ='course_category'

class Course(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='course/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_payable = models.BooleanField(default=True)
    amount = models.FloatField(default=True)

    class Meta:
        db_table ='course'

class CourseSection(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        db_table ='course_section'


class CourseContent(models.Model):

    course_section = models.ForeignKey(CourseSection, null=True, blank=True, on_delete=models.SET_NULL)
    decription = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='course_content'

class CourseContentFile(models.Model):

    course_content = models.ForeignKey(CourseContent, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(null=True, blank=True, upload_to='course_content_file/')
    status = models.BooleanField(default=True)
    id_delete = models.BooleanField(default=False)

    class Meta:
        db_table ='course_content_file'

class CourseEnrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table ='course_enrollment'