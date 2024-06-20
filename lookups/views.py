from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Industry, Country, State, City, Designation, Department, Source, DegreeType, EmployeeType, JobType, Relation, Skill, Language
from .serializers import IndustrySerializer, CountrySerializer, StateSerializer, CitySerializer, DesignationSerializer, DepartmentSerializer, SourceSerializer, DegreeTypeSerializer, EmployeeTypeSerializer, JobTypeSerializer, RelationSerializer, SkillSerializer, LanguageSerializer


class LookupBaseViewSet(viewsets.ModelViewSet):
    """
    Base viewset for lookup tables.
    """
    queryset = None  # To be overridden in subclasses
    serializer_class = None  # To be overridden in subclasses

    def get_queryset(self):
        if self.queryset is None:
            raise AssertionError("queryset is not set")
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": f"{self.serializer_class.Meta.model.__name__} added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": f"{self.serializer_class.Meta.model.__name__} updated successfully", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"{self.serializer_class.Meta.model.__name__} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class IndustryViewSet(LookupBaseViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class CountryViewSet(LookupBaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(LookupBaseViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class CityViewSet(LookupBaseViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DesignationViewSet(LookupBaseViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class DepartmentViewSet(LookupBaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class SourceViewSet(LookupBaseViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class DegreeTypeViewSet(LookupBaseViewSet):
    queryset = DegreeType.objects.all()
    serializer_class = DegreeTypeSerializer

class EmployeeTypeViewSet(LookupBaseViewSet):
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer

class JobTypeViewSet(LookupBaseViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class RelationViewSet(LookupBaseViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer

class SkillViewSet(LookupBaseViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class LanguageViewSet(LookupBaseViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer