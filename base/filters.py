import django_filters
from django_filters import CharFilter

from django.contrib.auth.models import User

class Userfilter(django_filters.FilterSet):
    note = CharFilter(field_name='username', lookup_expr='icontains', label="Search")
    class Meta:
        model = User
        fields = ['note']
        
