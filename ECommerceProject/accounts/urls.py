from django.conf import settings
from django.db import router
from django.urls import include, path

from ECommerceProject.views import ProtectedAPIView
# from accounts.serializers import AboutusSerializer, BrandSerializer, CategorySerializer, FooterLinkSerializer, FooterWidgetSerializer, InstagramImageSerializer, InstagramSectionSerializer, QRPaymentMethodSerializer, TagSerializer, TestimonialSerializer
from . import views  # Import views from the current app
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import AboutUsViewSet, BannerProductViewSet, BannershowViewSet, BlogPostViewSet, CategoryViewSet, CommentViewSet, FooterLinkViewSet, FooterWidgetViewSet, InstagramImageViewSet, InstagramSectionViewSet, LAstNewsViewSet, OrderViewSet, PriceRangeViewSet, ProductInventoryViewSet, QRPaymentMethodViewSet, TagViewSet, TeamMemberViewSet, TestimonialViewSet, inventory_report_page, logoSerializer, payment_summary_page, payment_summary_report, place_order, product_sales_report, productViewSet


router = DefaultRouter()

router.register(r'posts', BlogPostViewSet)
router.register(r'comments', CommentViewSet, basename='comment') 

router.register(r'products',productViewSet)

# router.register(r'blogPage ',LAstNewsViewSet , basename='blogPage')
router.register(r'blogPage', LAstNewsViewSet, basename='blogPage')


router.register(r'orders', OrderViewSet)
router.register(r'logo', logoSerializer, basename='logo')  #  logo 
router.register(r'Bannershow', BannershowViewSet, basename='Bannershow')  

router.register(r'bannerProduct', BannerProductViewSet, basename='bannerProduct')  # BannerProductViewSet
router.register(r'aboutus', AboutUsViewSet, basename='aboutus')  # About us 
# router.register(r'brand', BrandViewSet, basename='Brand')  # Brand 
router.register(r'category', CategoryViewSet, basename='Category')  # Category 
router.register(r'priceRange', PriceRangeViewSet, basename='PriceRange')  # Category 
router.register(r'tag', TagViewSet, basename='Tag')  # Tag 
router.register(r'qRPaymentMethod', QRPaymentMethodViewSet, basename='QRPaymentMethod')
router.register(r'instagramSection', InstagramSectionViewSet, basename='InstagramSection')  # Instagram section 
router.register(r'instagramImage', InstagramImageViewSet, basename='InstagramImage')  # Instagram
router.register(r'testimonial', TestimonialViewSet, basename='Testimonial')  # Testimonial 

router.register(r'teamMember', TeamMemberViewSet, basename='TeamMember')  # TeamMember

router.register(r'footerLink', FooterLinkViewSet, basename='FooterLink')  # Footer link 

router.register(r'FooterWidget', FooterWidgetViewSet, basename='FooterWidget')  # Footer


# report

router.register(r'inventory-report', ProductInventoryViewSet, basename='inventory')

# api seairelizer
from .views import OrderViewSet, ReportOrder, order_payment_view , ProductListAPIView



urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='homepage'),

   
#   place order
    path('api/place/', place_order, name='place-order'), 


    # Define your app's URL patterns here
    path('signinacccount/',views.SIgninAccount,name='SIgninAccountpage'),
    path('about/', views.about, name='aboutpage'),
    path('contact/', views.contact, name='contactpage'),
    path('shop/', views.shop, name='shoppage'),# current route

    # path('shop/category/<int:category_id>/', views.shop, name='shoppage'),

    path('shop/category/<int:category_id>/', views.shop_by_category, name='shop_by_category'),  # category_id to same shop view
    path('brand/<int:brand_id>/', views.shop_by_brand, name='shop_by_brand'),
    path('price_range/<int:price_range_id>/', views.shop_by_price_range, name='shop_by_price_range'),
    path('tag/<int:tag_id>/', views.shop_by_tag, name='shop_by_tag'),


    path('shop_details/<int:pk>/', views.shop_details, name='shop_detailspage'),

    path('blogdetails/<slug:slug>/', views.blogdetails, name='blogdetailspage'), # block not have page for detaiks


    path('blog/', views.blog, name='blogpage'),




# // Cart Management

    path('shopping-cart/', views.shopping_cart_view, name='shopping_cartpage'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),

   
# // Checkout and Order Placement

    path('cart/', views.shopping_cart_view, name='shopping_cartpage'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkoutpage'),
    # replace
    path('place-order/', views.place_order, name='place_order'),
    path('api/place/', place_order, name='place-order'),


    # ordersuccess
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # qrcode payment
    path('order/<int:order_id>/qr-instructions/', views.qr_payment_instructions, name='qr_payment_instructions'),
    # qrpage
    path('order/<int:order_id>/submit-qr-payment/', views.submit_qr_payment, name='submit_qr_payment'),
    # pagethank you
    path('order/<int:order_id>/qr-thank-you/', views.qr_thank_you, name='qr_thank_you'),

    # invoicedownloads
    path('order/<int:order_id>/download-invoice/', views.download_invoice, name='download_invoice'),



    # seairelizer product ulr bro


    path('blogs/', views.blog_list_api, name='blog_list_page'),

    path('blogs/detail/<int:pk>/', views.blog_detail_template, name='blog-detail-template'),


    # api
    path('api/products/', ProductListAPIView.as_view(), name='product-list-api'),
    # show aip in templates
    path('products/', views.product_list_view, name='product-list'),
    # show product by id with api
    path('products/<int:pk>/', views.product_detail_view, name='product-detail'),
    # add card with api
    path('cart/add/<int:product_id>/',views. add_to_cart_view, name='add-to-cart'),

    # update more crud
    path('ProductCrud/', views.product_crud, name='product_crud'),
    
    # paymentbtqrtemplates
    path('order/<int:order_id>/', order_payment_view, name='order_payment'),


# order report
    path('ReportOrder/', ReportOrder, name='ReportOrder'),

    # path('inventory-report/', inventory_report_page, name='inventory_report_page'),

    # path('api/inventory-report/', inventory_report_api),
    path('report-products/', inventory_report_page, name='inventory_report_page'),

    path('report/inventory/', views.inventory_report_page, name='inventory_report_page'),

    # Products Sale Report api
    path('api/product-sales-report/', product_sales_report, name='product_sales_report'),
    # payment report
    path('api/payment-summary-report/', payment_summary_report),
    path('report/payment-summary/', payment_summary_page, name='payment_summary_page'),

    # path('api/payment-summary-report/', payment_summary_api, name='payment_summary_api'),







    # api login and register

    path('api/register/', views.register_user, name='api_register'), # register api normal

    path('api/login/', views.login_user, name='api_login'), #  login api normal
    
    path('api/protected/', views.protected_api, name='api_protected'), # protected api

    path('register-login/', views.register_login_page, name='register_login_page'), # register and login template 
    path('register/', views.registerApi, name='register_page_template'),  # changed from 'registerApi/'



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)