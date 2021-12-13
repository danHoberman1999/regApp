# Data models for the registration app
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse, reverse_lazy

# data model for a Person
class Person(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    idnumber = models.PositiveBigIntegerField()
    email = models.EmailField(blank=True)
    # auto_now_add=True -> filled automatically when new data added
    datecreated = models.DateTimeField(blank=True, auto_now_add=True)
    # auto_now=True -> filled automatically when data modified
    datemodified = models.DateTimeField(blank=True, auto_now=True)

    # getter for the Person's full name
    @property # tells python that this is a 'getter'
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    # used to declare abstract class
    class Meta:
        abstract = True # declares class is abstract

    def __str__(self):
        return f'Name:{self.full_name}, Id Number: {self.idnumber}, \
            email: {self.email}'

# data model for a Student
class Student(Person):
    # lookup table for schoolyear (to prevent unexpected input)
    YEAR_IN_SCHOOL = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate')
    ]
    # lookup table for major
    MAJORS = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('SCI', 'Science'),
        ('BUS', 'Business'),
        ('LAW', 'Law'),
        ('NUR', 'Nursing'),
        ('MAT', 'Math'),
    ]

    schoolyear = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL)
    major = models.CharField(max_length=3, choices=MAJORS)
    gpa = models.FloatField(blank=True, max_length=4)

    def __str__(self):
        return f'Student Id: {self.id} - \
            {super(Student, self).__str__()} Year in School: \
            {self.schoolyear}, Major: {self.major}, GPA: {self.gpa}'

    def get_absolute_url(self):
        return reverse_lazy('regApp:students')
