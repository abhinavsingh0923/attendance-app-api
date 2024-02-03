from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class FaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFaceModel
        fields = ('id', 'name', 'face_vector')

class StudentsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFaceModel
        fields = ('name',)

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class CourseAttendanceSerializer(serializers.Serializer):
    student = serializers.DictField()
    attendance = serializers.ListField(child=serializers.DictField())

