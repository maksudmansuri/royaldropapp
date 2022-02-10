from django.db.models import fields
from rest_framework import serializers
from accounts.models import Merchants

from front.models import Product,ProductAbout,ProductCategory, ProductChildSubCategory, ProductDetails, ProductDiscount, ProductReviews, ProductSizeWeight, ProductStockManage,ProductSubCategory, ProductTag, productGst, productMedia
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import os
from django.core.files.storage import default_storage,FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_COURSENAME_LENGTH = 5
MIN_COURSEDECS_LENGTH = 50
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError

from front.utils import is_image_size_valid



class MerchantSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Merchants
		fields = "__all__"

class ProductTagSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductTag
		fields = "__all__"
class ProductReviewsSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductReviews
		fields = "__all__"
class ProductDiscountSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductDiscount
		fields = "__all__"
class ProductAboutSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductAbout
		fields = "__all__"

class ProductDetailsSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductDetails
		fields = "__all__"

class ProductStockManageSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductStockManage
		fields = "__all__"

class ProductSizeWeightSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ProductSizeWeight
		fields = "__all__"

class productGstSerializer(serializers.ModelSerializer):
	class Meta: 
		model = productGst
		fields = "__all__"

class ProductMediaSerializer(serializers.ModelSerializer):
	class Meta: 
		model = productMedia
		fields = "__all__"

	def validate_product_image_url(self, Product):
		crs_imge = productMedia.media_content
		new_url = crs_imge.url
		print(crs_imge)
		if "?" in new_url:
			new_url = crs_imge.url[:crs_imge.url.rfind("?")]
		return new_url


class ProductsDetailSerializer(serializers.ModelSerializer):
	# productmedia = ProductMediaSerializer(many=True)
	productgst = productGstSerializer(many=True)
	productsizeweight = ProductSizeWeightSerializer(many=True)
	productstockmanage = ProductStockManageSerializer(many=True)
	productdetails = ProductDetailsSerializer(many=True)
	productabout = ProductAboutSerializer(many=True)
	productdiscount = ProductDiscountSerializer(many=True)
	productreviews = ProductReviewsSerializer(many=True)
	producttag = ProductTagSerializer(many=True)
	class Meta: 
		model = Product
		fields = ['pk','product_name','product_sku','product_subcategory','product_childsubcategory','product_slug','product_image','product_category','product_mrp','product_selling_price','added_by_merchant','product_brand','product_model_number','product_desc','product_l_desc','is_active','productgst','productsizeweight','productstockmanage','productdetails','productabout','producttag','productreviews','productdiscount']

	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['merchant'] = MerchantSerializer(instance.added_by_merchant).data
		return response

class ChildSubCategorySerializer(serializers.ModelSerializer):
	productchildcat = ProductsDetailSerializer(many=True)
	class Meta: 
		model = ProductChildSubCategory
		fields = ['pk','title','thumbnail','description','created_date','is_active','productchildcat']

class SubCategorySerielizer(serializers.ModelSerializer):
	childcategories = ChildSubCategorySerializer(many=True)
	productsubcat = ProductsDetailSerializer(many=True)
	class Meta: 
			model = ProductSubCategory
			fields = ['pk','title','thumbnail','description','created_date','is_active','childcategories','productsubcat']

class CategorySerializer(serializers.ModelSerializer):
	subcategory = SubCategorySerielizer(many=True)
	productcat = ProductsDetailSerializer(many=True)
	class Meta: 
		model = ProductCategory
		fields = ['pk','title','thumbnail','description','created_date','is_active','subcategory','productcat']

"""
OLD Serielzer
"""

# class ProductDatailSerializer(serializers.ModelSerializer):

#     # username = serializers.SerializerMethodField('get_username_from_staffs')
#     # product_image = serializers.SerializerMethodField('validate_product_image_url')

#     class Meta: 
#         model = Product 
#         fields = ['pk','product_name','product_sku','product_subcategory','product_childsubcategory','product_slug','product_image','product_category','product_mrp','product_selling_price','added_by_merchant','product_brand','product_model_number','product_desc','product_l_desc','is_active']

#     # def get_username_from_staffs(self,Product):
#     #     username = Product.teacher.admin.username
#     #     return username

#     # def validate_product_image_url(self, Product):
#     #     crs_imge = Product.product_image
#     #     new_url = crs_imge.url
#     #     if "?" in new_url:
#     #         new_url = crs_imge.url[:crs_imge.url.rfind("?")]
#     #     return new_url

class ProductCategoriesSerializer(serializers.ModelSerializer):

	# username = serializers.SerializerMethodField('get_username_from_staffs')
	# product_image = serializers.SerializerMethodField('validate_product_image_url')

	class Meta: 
		model = ProductCategory
		fields ="__all__"

	# def get_username_from_staffs(self,Product):
	# 	username = Hospitals.admin
	# 	return username

	def validate_product_image_url(self, Product):
		crs_imge = ProductCategory.thumbnail
		new_url = crs_imge.url
		if "?" in new_url:
			new_url = crs_imge.url[:crs_imge.url.rfind("?")]
		return new_url



    # def get_username_from_staffs(self,Product):
    #     username = Product.teacher.admin.username
    #     return username

    # def validate_product_image_url(self, Product):
    #     crs_imge = Product.product_image
    #     new_url = crs_imge.url
    #     if "?" in new_url:
    #         new_url = crs_imge.url[:crs_imge.url.rfind("?")]
    #     return new_url
  

class ProductDetailUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ['product_name','product_fee','product_duration','product_level','product_desc','product_image']

	def validate(self, crs):
		try:
			product_name = crs['product_name']
			if len(product_name) < MIN_COURSENAME_LENGTH:
				raise serializers.ValidationError({"response": "Enter a product_name longer than " + str(MIN_COURSENAME_LENGTH) + " characters."})
			
			product_desc = crs['product_desc']
			if len(product_desc) < MIN_COURSEDECS_LENGTH:
				raise serializers.ValidationError({"response": "Enter a product_desc longer than " + str(MIN_COURSEDECS_LENGTH) + " characters."})
			
			product_image = crs['product_image']
			url = os.path.join(settings.TEMP , str(product_image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in product_image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return crs


class ProductDetailCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ['product_name','product_fee','product_duration','product_level','product_desc','teacher','product_image','product_category','product_subcategory']
                                                                                                                                         
	def save(self):
		
		try:
			product_image = self.validated_data['product_image']
			product_name = self.validated_data['product_name']
			if len(product_name) < MIN_COURSENAME_LENGTH:
				raise serializers.ValidationError({"response": "Enter a product_name longer than " + str(MIN_COURSENAME_LENGTH) + " characters."})
			
			product_desc = self.validated_data['product_desc']
			if len(product_desc) < MIN_COURSEDECS_LENGTH:
				raise serializers.ValidationError({"response": "Enter a product_desc longer than " + str(MIN_COURSEDECS_LENGTH) + " characters."})
			
			product_detail = Product(
								teacher=self.validated_data['teacher'],
								product_name=product_name,
								product_desc=product_desc,
								product_image=product_image,
                                product_fee=self.validated_data['product_fee'],
                                product_duration=self.validated_data['product_duration'],
                                product_level=self.validated_data['product_level'],
								# product_slug=self.validated_data['product_slug'],
								product_subcategory=self.validated_data['product_subcategory'],
								product_category=self.validated_data['product_category'],
								is_appiled = True,
								)

			url = os.path.join(settings.TEMP , str(product_image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in product_image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			product_detail.save()
			return product_detail
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a product_name, some content, and an image."})

