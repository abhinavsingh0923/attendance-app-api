import ast
from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# import face_recognition
# from PIL import Image
import numpy as np


def extract_face_vector(data):
    # Assuming data is a list of OrderedDict objects
    face_vector_list = [entry['face_vector'] for entry in data]

    # Extracting the first face vector (assuming there is only one in the list)
    face_vector = face_vector_list[0]

    return face_vector

def clean_face_vector(vector_str):
    # Assuming it's a list of floats represented as a string
    if vector_str:
        try:
            # Convert the string to a list
            vector_list = ast.literal_eval(vector_str.replace('\r\n', ''))
            # Convert the list to a NumPy array
            vector_array = np.array(vector_list)
            return vector_array
        except (SyntaxError, ValueError):
            # Handle the case where the conversion fails
            return np.array([])
    else:
        # Return an empty NumPy array or handle it based on your needs
        return np.array([])


class faces(APIView):
    def get(self, request):
        known_faces = StudentFaceModel.objects.all()
        serialzier=FaceModelSerializer(known_faces,many=True)
        inputdata = serialzier.data
        for item in inputdata:
            item['face_vector'] = clean_face_vector(item['face_vector'])
        return Response(data=inputdata)

class match_face(APIView):
    def post(self, request, batch_id, branch_id):
        user_image = request.FILES['image']

        known_faces = StudentFaceModel.objects.filter(batch_id=batch_id, branch_id=branch_id)
        if not known_faces:
            return Response({'error': 'No known faces found for the provided batch and branch'}, status=status.HTTP_404_NOT_FOUND)

        serialzier = FaceModelSerializer(known_faces, many=True)
        known_faces_data = serialzier.data

        for item in known_faces_data:
            item['face_vector'] = clean_face_vector(item['face_vector'])

        user_image_data = Image.open(user_image)
        user_face_locations = face_recognition.face_locations(np.array(user_image_data))
        user_face_encodings = face_recognition.face_encodings(np.array(user_image_data), user_face_locations)

        if not user_face_encodings:
            return Response({'error': 'No faces found in the provided image'}, status=status.HTTP_400_BAD_REQUEST)

        user_face_vector = user_face_encodings[0]

        for known_face in known_faces_data:
            known_face_vector = known_face['face_vector']
            match_result = face_recognition.compare_faces([known_face_vector], user_face_vector, tolerance=0.6)[0]

            if match_result:
                return Response({'match': True, 'name': known_face['name']}, status=status.HTTP_200_OK)

        return Response({'match': False, 'error': 'No match found'}, status=status.HTTP_404_NOT_FOUND)

class StudentList(APIView):
    def get(self, request, branch_id, batch_id):
        students = StudentFaceModel.objects.filter(branch_id=branch_id, batch_id=batch_id)
        serializer = StudentsNameSerializer(students, many=True)
        return Response(data=serializer.data , status=status.HTTP_200_OK)


class AllBatches(APIView):
    def get(self, request):
        data = Batch.objects.all()
        serializer = BatchSerializer(data ,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


class AllBranchs(APIView):
    def get(self, request):
        data = Branch.objects.all()
        serializer = BatchSerializer(data ,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class AllCourses(APIView):
    def get(self , request):
        data = Course.objects.all()
        serializer = CourseSerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class AllCoursesbyTeacher(APIView):
     def get(self, request):
        # Retrieve the teacher's profile associated with the logged-in user
        try:
            teacher_profile = request.user.teacher_profile
        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # If the teacher profile exists, fetch the courses associated with it
        if teacher_profile:
            courses = teacher_profile.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No courses found for this teacher"}, status=status.HTTP_404_NOT_FOUND)
        
class CourseAttendanceAPIView(APIView):
    def get(self, request, course_id, batch_id, branch_id):
        # Retrieve the Course, Batch, and Branch objects
        course = get_object_or_404(Course, id=course_id)
        batch = get_object_or_404(Batch, id=batch_id)
        branch = get_object_or_404(Branch, id=branch_id)

        # Get the lectures for the specified course, batch, and branch
        lectures = Lecture.objects.filter(course=course, batch=batch, branch=branch)

        # Get the list of all students in the batch and branch
        students = StudentFaceModel.objects.filter(batch=batch, branch=branch)

        # Create a list to store attendance data for each student
        attendance_data = []

        # Loop through each student
        for student in students:
            # Create a dictionary to store attendance data for each lecture
            student_attendance = []

            # Counters for attendance calculation
            total_lectures = 0
            present_lectures = 0

            # Loop through each lecture
            for lecture in lectures:
                # Get the attendance record for the student and lecture
                attendance_record = Attendance.objects.filter(lecture=lecture, student=student).first()

                # Increment the total lectures
                total_lectures += 1

                # Check if the student is present and increment present_lectures
                if attendance_record and attendance_record.is_present:
                    present_lectures += 1

                # Append the attendance data for the lecture to the list
                student_attendance.append({
                    'lecture': lecture.id,
                    'is_present': attendance_record.is_present if attendance_record else False,
                })

            # Calculate the attendance percentage for the student
            attendance_percentage = (present_lectures / total_lectures) * 100 if total_lectures > 0 else 0

            # Append the attendance data for the student to the main list
            attendance_data.append({
                'student': {
                    'name': student.name,
                    'id_number': student.id_number,
                },
                'attendance': student_attendance,
                'attendance_percentage': attendance_percentage,
            })

        # Serialize the data using the CourseAttendanceSerializer
        serializer = CourseAttendanceSerializer(attendance_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAttendanceAPIView(APIView):
    def post(self, request, lecture_id, format=None):
        student_ids = request.data.get('student_ids', [])

        try:
            lecture = Lecture.objects.get(pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({"error": "Lecture does not exist"}, status=status.HTTP_404_NOT_FOUND)

        students_not_found = []
        for student_id in student_ids:
            try:
                student = StudentFaceModel.objects.get(pk=student_id)
            except StudentFaceModel.DoesNotExist:
                students_not_found.append(student_id)
                continue

            # Check if attendance for this student and lecture already exists
            attendance_exists = Attendance.objects.filter(lecture=lecture, student=student).exists()
            if attendance_exists:
                return Response({"error": f"Attendance for student {student_id} for this lecture already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Create new attendance record
            Attendance.objects.create(lecture=lecture, student=student, is_present=True)

        if students_not_found:
            return Response({"error": f"Students with IDs {', '.join(map(str, students_not_found))} do not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Attendance marked successfully"}, status=status.HTTP_201_CREATED)

class LectureCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateLectureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetLectureListAPIView(APIView):
    def get(self, request, course_id, branch_id, batch_id, *args, **kwargs):
        lectures = Lecture.objects.filter(course_id=course_id, branch_id=branch_id, batch_id=batch_id)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)