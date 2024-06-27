from django.db import models
from users.models import User

# Create your models here.

class ObservationCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='observation_category'

class ObservationKey(models.Model):

    observation_category = models.ForeignKey(ObservationCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='observation_key'

class Rating(models.Model):

    key = models.CharField(max_length=255, null=True, blank=True)
    remark = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        db_table ='rating'

class ObservationReport(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    observation_category = models.ForeignKey(ObservationCategory, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table ='observation report'

class ObservationReportKey(models.Model):

    observation_report = models.ForeignKey(ObservationReport, on_delete=models.CASCADE, null=True, blank=True)
    key = models.ForeignKey(ObservationKey, on_delete=models.CASCADE)
    max_marks = models.FloatField(default=0)
    min_marks = models.FloatField(default=0)
    
    class Meta:
        db_table ='observation_report_key'

class UserReportEnrollment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    observation_report = models.ForeignKey(ObservationReport, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.FloatField(default=0)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='user_report_enrollment'


class UserReportKeyPoint(models.Model):

    user_report_enrollment = models.ForeignKey(UserReportEnrollment, on_delete=models.CASCADE, null=True, blank=True)
    observation_report_key = models.ForeignKey(ObservationReportKey, on_delete=models.CASCADE, null=True, blank=True)
    observation_report_key_text = models.TextField(null=True, blank=True)
    rating_text = models.TextField(null=True, blank=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table ='user_report_key_point'