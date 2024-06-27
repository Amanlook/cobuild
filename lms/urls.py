from django.urls import include, path
from .views import *

urlpatterns = [
    path("section/",SectionList.as_view()),
    path("section/<pk>/",SectionDetailed.as_view()),
    path("sub-section/",SubSectionList.as_view()),
    path("sub-section/<pk>/",SubSectionDetailed.as_view()),
    path("question-bank/",QuestionBankList.as_view()),
    path("question-bank/<pk>/",QuestionBankDetailed.as_view()),
    path("option/",OptionList.as_view()),
    path("option/<pk>/",OptionDetailed.as_view()),
    path("quiz/",QuizList.as_view()),
    path("quiz/<pk>/",QuizDetailed.as_view()),
    path("quiz-section/",QuizSectionList.as_view()),
    path("quiz-section/<pk>/",QuizSectionDetailed.as_view()),
    path("section-question/",SectionQuestionList.as_view()),
    path("section-question/<pk>/",SectionQuestionDetailed.as_view()),
    path("quiz-enrollment/",QuizEnrollmentList.as_view()),
    path("quiz-enrollment/<pk>/",QuizEnrollmentDetailed.as_view()),
    path("user-quiz-question/",UserQuizQuestionList.as_view()),
    path("user-quiz-question/<pk>/",UserQuizQuestionDetailed.as_view()),
    
    path("course-category/",CourseCategoryList.as_view()),
    path("course-category/<pk>/",CourseCategoryDetailed.as_view()),
    path("course/",CourseList.as_view()),
    path("course/<pk>/",CourseDetailed.as_view()),
    path("course-section/",CourseSectionList.as_view()),
    path("course-section/<pk>/",CourseSectionDetailed.as_view()),
    path("course-content/",CourseContentList.as_view()),
    path("course-content/<pk>/",CourseContentDetailed.as_view()),
    path("course-content-file/",CourseContentFileList.as_view()),
    path("course-content-file/<pk>/",CourseContentFileDetailed.as_view()),
    path("course-enrollment/",CourseEnrollmentList.as_view()),
    path("course-enrollment/<pk>/",CourseEnrollmentDetailed.as_view()),
    
    
    
    
    
    
     
]