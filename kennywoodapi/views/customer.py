from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name = 'customer',
            lookup_field = 'id'
        )
        fields = ('id', 'family_members', 'user_id')

class Customers(ViewSet):
    
    def create(self, request):
        customer = Customer()
        customer.family_members = request.data['family_members']

        customer.save()

        serializer = CustomerSerializer(customer, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        try:
            customer = Customer.objects.get(pk = pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk = None):
        customer = Customer.objects.get(pk = pk)
        customer.family_members = request.data['family_members']

        customer.save()

        return Response({}, status = status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk = None):
        try:
            customer = Customer.objects.get(pk = pk)
            customer.delete()

            return Response({}, status = status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status = status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(
            customer, many = True, context = {'request': request}
        )

        return Response(serializer.data)