from django.db import models
import numpy as np
from django.core.validators import MaxValueValidator
from account.models import User
# Attendance models of the application 

class Batch(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name

# Assuming your StudentFaceModel model looks something like this
class StudentFaceModel(models.Model):
    id_number = models.IntegerField(validators=[MaxValueValidator(99999)], unique=True)
    name = models.CharField(max_length=255)
    face_vector = models.TextField()  # Assuming the face vector is stored as a string
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def get_face_vector(self):
        return np.array(self.face_vector)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.id_number}"


class Course(models.Model):
    name = models.CharField(unique=True,max_length=100)
    code = models.CharField(unique=True,max_length=10)
    year = models.IntegerField(validators =[MaxValueValidator(5)])
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)


class Lecture(models.Model):
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} - {self.batch} - {self.branch} - {self.date}"

    class Meta:
        unique_together = ('date', 'course', 'batch', 'branch')

class Attendance(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentFaceModel, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.lecture}"

    class Meta:
        unique_together = ('lecture', 'student')

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    courses = models.ManyToManyField('Course', related_name='teachers')

    def __str__(self):
        return self.user.username + "'s Profile"