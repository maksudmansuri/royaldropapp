from django.contrib import admin
from .models import Product,ProductCategory,ProductSubCategory,ProductDetails,Product_Modules,Product_Session,ProductAbout,ProductComments,ProductQuestions,ProductReviews,ProductReviewVoting,ProductTag,ProductTransaction,ProductVariantItems,ProductVarient,ProductWishlist,Customers,CustomUser,OderDeliveryStatus,productMedia

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(productMedia)
admin.site.register(ProductTransaction)
admin.site.register(ProductWishlist)
admin.site.register(ProductDetails)
admin.site.register(ProductAbout)
admin.site.register(ProductTag)
admin.site.register(ProductReviews)
admin.site.register(ProductReviewVoting)
admin.site.register(ProductVarient)
admin.site.register(ProductVariantItems)
# admin.site.register(CustomersOrders)
admin.site.register(OderDeliveryStatus)
