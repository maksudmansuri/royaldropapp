from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination


from rest_framework import status

from rest_framework.response import Response

from accounts.models import CustomUser,AdminHOD,Staffs,Customers as Customers
from front.models import Product,Product_Modules,ProductCategory, ProductChildSubCategory,ProductSubCategory,viewed
from front.api.serializers import CategorySerializer, ChildSubCategorySerializer, ProductDetailUpdateSerializer,ProductDetailCreateSerializer, ProductModuleDatailSerializer, ProductsDetailSerializer, SubCategorySerielizer

from rest_framework.authentication import TokenAuthentication

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


# @api_view(['GET',])
# @permission_classes((IsAuthenticated,))

class ApiCategoriesListView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# queryset = ProductCategory.objects.all()
	# serializer_class = CategorySerializer
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('product_name','product_subcategory','product_childsubcategory','product_category','product_mrp','product_desc','added_by_merchant',)
	
	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(ProductCategory,id = id,is_active = True)
			# hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
			# serializer = HospitalDoctorsViewSerializer(hospitalDoctors)
			# return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
			serializer = CategorySerializer(hospital)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = ProductCategory.objects.all()
		serializer = CategorySerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ApiSubCategoriesListView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# queryset = ProductCategory.objects.all()
	# serializer_class = CategorySerializer
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('product_name','product_subcategory','product_childsubcategory','product_category','product_mrp','product_desc','added_by_merchant',)
	
	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(ProductSubCategory,id = id,is_active = True)
			# hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
			# serializer = HospitalDoctorsViewSerializer(hospitalDoctors)
			# return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
			serializer = SubCategorySerielizer(hospital)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = ProductSubCategory.objects.all()
		serializer = SubCategorySerielizer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ApiChildCategoriesListView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# queryset = ProductCategory.objects.all()
	# serializer_class = CategorySerializer
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('product_name','product_subcategory','product_childsubcategory','product_category','product_mrp','product_desc','added_by_merchant',)
	
	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(ProductChildSubCategory,id = id,is_active = True)
			# hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
			# serializer = HospitalDoctorsViewSerializer(hospitalDoctors)
			# return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
			serializer = ChildSubCategorySerializer(hospital)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = ProductChildSubCategory.objects.all()
		serializer = ChildSubCategorySerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ApiProductDtailsListView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# queryset = ProductCategory.objects.all()
	# serializer_class = CategorySerializer
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('product_name','product_subcategory','product_childsubcategory','product_category','product_mrp','product_desc','added_by_merchant',)
	
	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(Product,id = id,is_active = True)
			# hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital)
			# serializer = HospitalDoctorsViewSerializer(hospitalDoctors)
			# return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
			serializer = ProductsDetailSerializer(hospital)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = Product.objects.all()
		serializer = ProductsDetailSerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

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
	

