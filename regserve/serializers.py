from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'firstname', 'lastname', 'idnumber', 'email',
        'schoolyear', 'major', 'gpa', 'datecreated', 'datemodified')
        # read only are not deseriealized client side
        read_only_fields = ('datecreated', 'datemodified')