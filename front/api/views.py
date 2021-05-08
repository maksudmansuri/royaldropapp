from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status

from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response

from accounts.models import CustomUser,AdminHOD,Staffs,Customers as Students
from front.models import Product,Product_Modules,Product_Session,ProductCategory,ProductSubCategory,viewed
from front.api.serializers import ProductDatailSerializer,ProductDetailUpdateSerializer,ProductDetailCreateSerializer,ProductModuleDatailSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import (
# 	AllowAny,
# 	)

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_product_view(request,slug):
	try:
		crs = Product.objects.get(product_slug=slug)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = ProductDatailSerializer(crs)
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_product_view(request,slug):
	try:
		crs = Product.objects.get(product_slug=slug)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if crs.teacher != Staffs.objects.get(admin=request.user):
		return Response({'response': 'you dont have permisssion to edit that'})

	if request.method == "PUT":
		serializer = ProductDetailUpdateSerializer(crs,data=request.data,partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = crs.pk
			data['product_name'] = crs.product_name
			data['product_fee'] = crs.product_fee
			data['product_duration'] = crs.product_duration
			data['product_level'] = crs.product_level
			data['product_desc'] = crs.product_desc
			data['product_slug'] = crs.product_slug
			image_url = str(request.build_absolute_uri(crs.product_image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['product_image'] = image_url
			data['username'] = crs.teacher.admin.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_teacher_of_product(request, slug):
	try:
		crs = Product.objects.get(product_slug=slug)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if crs.teacher.admin != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_product_view(request,slug):
	try:
		crs = Product.objects.get(product_slug=slug)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if crs.teacher != Staffs.objects.get(admin=request.user):
		return Response({'response': 'you dont have permisssion to Delete that'})

	if request.method == "DELETE":
		oparetion = crs.delete()
		data = {}
		if oparetion:
			data["success"] = "deleted Successful"
		else:
			data["failure"] = "delete failed"

		return Response(data=data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_product_view(request):

	if request.method == 'POST':

		data = request.data
		data['teacher'] = Staffs.objects.get(admin=request.user).pk
		data['product_category'] = ProductCategory.objects.get(id=1).pk
		data['product_subcategory'] = ProductSubCategory.objects.get(id=1).pk
		print(data)
		serializer = ProductDetailCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			product_detail = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = product_detail.pk
			data['product_name'] = product_detail.product_name
			data['product_desc'] = product_detail.product_desc
			data['product_slug'] = product_detail.product_slug
			data['product_duration'] = product_detail.product_duration
			data['product_level'] = product_detail.product_level
			data['product_fee'] = product_detail.product_fee
			image_url = str(request.build_absolute_uri(product_detail.product_image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['product_image'] = image_url
			data['username'] = product_detail.teacher.admin.username
			data['product_subcategory'] = product_detail.product_subcategory.subcategory
			data['product_category'] = product_detail.product_category.category
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET',])
# @permission_classes((IsAuthenticated,))
class ApiProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDatailSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('product_name','product_fee','product_level','teacher__admin__username')

class ApiProductModuleListView(generics.ListAPIView):
	queryset = Product_Modules.objects.all()
	serializer_class = ProductModuleDatailSerializer

	def get(self,request,*args,**kwargs):
		# try:
		crs_id = Product.objects.get(id=self.kwargs.get('id'))
		mdl = self.queryset.filter(product=crs_id)
		response_data = self.get_serializer(mdl,many=True)
		return Response(
			{
				"data" : response_data.data
			}
		)
		# except Product.DoesNotExist:
		# 	raise serializers.V ValidationError(_("Product Does not Exist"))
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	

