from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import *
from .serializers import *



# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all() #django ORM --> equals in query like : SELECT * from Instituions
    serializer_class = InstitutionsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        institution_name = request.query_params.get('name', None)
        cache_key = f'institution-trade:{institution_name}' # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
            
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(institution_name)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, institution_name=None):
        queryset = super().get_queryset()

        if institution_name:
            queryset = queryset.filter(
                Q(top_sellers__icontains=[{'name': institution_name}]) |
                Q(top_buyers__icontains=[{'name': institution_name}])
            )               
        return queryset

class MetadataView(ListAPIView):
    queryset = Metadata.objects.all() #django ORM --> equals in query like : SELECT * from Instituions
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        metadata_name = request.query_params.get('sector', None)
        cache_key = f'sector:{metadata_name}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
            
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(metadata_name)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, metadata_name=None):
        queryset = super().get_queryset()
        if metadata_name:
            queryset = queryset.filter(sector__icontains=metadata_name)          
        return queryset


class ReportsView(ListAPIView):
    queryset = Reports.objects.all() #django ORM --> equals in query like : SELECT * from Instituions
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        reports_name = request.query_params.get('sub_sector', None)
        cache_key = f'sub_sector:{reports_name}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
            
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(reports_name)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, reports_name=None):
        queryset = super().get_queryset()
        if reports_name:
            queryset = queryset.filter(sub_sector__icontains=reports_name)          
        return queryset

    

