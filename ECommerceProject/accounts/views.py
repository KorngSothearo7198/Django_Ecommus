from decimal import Decimal
import json
# from multiprocessing.managers import Token
import token
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages
from requests import Response
from accounts.models import *
from .models import CartItem, Order
from .forms import CheckoutForm, ContactMessageForm


from .forms import CommentForm

from rest_framework import generics
from .models import *
from .serializers import  AboutusSerializer, BannerProductSerializer, BannershowSerializer, BlogPostSerializer, BrandSerializer, CategorySerializer, CommentSerializer, ContactMessageSerializer, FooterLinkSerializer, FooterWidgetSerializer, InstagramImageSerializer, InstagramSectionSerializer, LastNewsSerializer, LogoSerializer, OrderSerializer, PriceRangeSerializer, ProductInventorySerializer, ProductReportSerializer, ProductSerializer, QRPaymentMethodSerializer, TagSerializer, TeamMemberSerializer, TestimonialSerializer 


# token authentication
from rest_framework.permissions import AllowAny
from .authentication import QueryParamAccessTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed



# Fillter By Category

from django.views.generic import ListView
from .models import Product, Category, Brand, PriceRange, Tag


def shop_by_category(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.filter(category_id=category_id)
    current_category = int(category_id)

    context = {
        'categories': categories,
        'products': products,
        'current_category': current_category,
        'brands': Brand.objects.all(),
        'price_ranges': PriceRange.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'accounts/shop.html', context)

def shop_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    products = Product.objects.filter(brand=brand)

    context = {
        'products': products,
        'current_brand': brand_id,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'price_ranges': PriceRange.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'accounts/shop.html', context)

def shop_by_price_range(request, price_range_id):
    price_range = get_object_or_404(PriceRange, id=price_range_id)
    products = Product.objects.filter(price__gte=price_range.min_price, price__lte=price_range.max_price)

    context = {
        'products': products,
        'current_price_range': price_range_id,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'price_ranges': PriceRange.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'accounts/shop.html', context)

def shop_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=tag)

    context = {
        'products': products,
        'current_tag': tag_id,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'price_ranges': PriceRange.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'accounts/shop.html', context)




# report not use with token 

# report
from rest_framework import viewsets
from .models import Order
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # authentication_classes = [QueryParamAccessTokenAuthentication]
    authentication_classes=[]
    permission_classes = [AllowAny]  # or use custom permission



class ProductInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductInventorySerializer




# Report Order
from django.utils.dateparse import parse_date
def get_queryset(self):
    qs = super().get_queryset()
    start_date = self.request.query_params.get('start_date')
    end_date = self.request.query_params.get('end_date')
    time_range = self.request.query_params.get('time_range')

    if start_date:
            qs = qs.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
            qs = qs.filter(created_at__date__lte=parse_date(end_date))
    if time_range:
        if time_range == 'morning':
                qs = qs.filter(created_at__hour__gte=0, created_at__hour__lte=11)
        elif time_range == 'afternoon':
                qs = qs.filter(created_at__hour__gte=12, created_at__hour__lte=17)
        elif time_range == 'evening':
                qs = qs.filter(created_at__hour__gte=18, created_at__hour__lte=23)

        return qs

def get_serializer_context(self):
    context = super().get_serializer_context()
    context.update({"request": self.request})
    return context
    
def ReportOrder(request):
    return render(request, 'Report/ReportOrder.html')



# product report 



# Normal Django view to render the HTML page
def inventory_report_page(request):
    return render(request, 'Report/inventory_report.html')



# from rest_framework.decorators import api_view
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product
# from .serializers import ProductReportSerializer  # ✅ must import this


# @api_view(['GET'])
# def inventory_report_api(request):
#     products = Product.objects.all()
#     serializer = ProductReportSerializer(products, many=True)
#     return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSalesReportSerializer

@api_view(['GET'])
def product_sales_report(request):
    products = Product.objects.all()
    serializer = ProductSalesReportSerializer(products, many=True)
    return Response(serializer.data)





from .models import Payment
from .serializers import PaymentSummarySerializer
@api_view(['GET'])
def payment_summary_report(request):
    payments = Payment.objects.select_related('cart__user')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        payments = payments.filter(payment_date__range=[start_date, end_date])

    serializer = PaymentSummarySerializer(payments, many=True)
    return Response(serializer.data)


def payment_summary_page(request):
    return render(request, 'Report/payment_summary_report.html')







from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# commemnt post
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]  # or use custom permission

    # def get_queryset(self):
    #     token = self.request.query_params.get('token')
    #     if not AccessToken.objects.filter(token=token, is_active=True).exists():
    #         # from django.http import JsonResponse
    #         raise AuthenticationFailed("Invalid or inactive token")
    
    #     queryset = super().get_queryset()
    #     category_id = self.request.query_params.get('categoryID')
    #     if category_id:
    #         queryset = queryset.filter(categoryID_id=category_id)
    #     return queryset



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 

    authentication_classes=[QueryParamAccessTokenAuthentication]
    permission_classes=[AllowAny]
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            # from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
    
    
#proeducts api use ViewSet
from .models import Product
class productViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all() #Model product
    serializer_class = ProductSerializer # is serializer class

    # authentication_classes=[QueryParamAccessTokenAuthentication]
    # permission_classes=[AllowAny]
    # def get_queryset(self):
    #     token = self.request.query_params.get('token')
    #     if not AccessToken.objects.filter(token=token, is_active=True).exists():
    #         # from django.http import JsonResponse
    #         raise AuthenticationFailed("Invalid or inactive token")
    
    #     queryset = super().get_queryset()
    #     category_id = self.request.query_params.get('categoryID')
    #     if category_id:
    #         queryset = queryset.filter(categoryID_id=category_id)
    #     return queryset
# end product



#blog page
class LAstNewsViewSet(viewsets.ModelViewSet):
    queryset = LatestNews.objects.all()
    serializer_class = LastNewsSerializer

    # authentication_classes=[QueryParamAccessTokenAuthentication]
    # permission_classes=[AllowAny]
    # def get_queryset(self):
    #     token = self.request.query_params.get('token')
    #     if not AccessToken.objects.filter(token=token, is_active=True).exists():
    #         # from django.http import JsonResponse
    #         raise AuthenticationFailed("Invalid or inactive token")
    
    #     queryset = super().get_queryset()
    #     category_id = self.request.query_params.get('categoryID')
    #     if category_id:
    #         queryset = queryset.filter(categoryID_id=category_id)
    #     return queryset



# endbolgpos




# show product
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     authentication_classes=[QueryParamAccessTokenAuthentication]
#     permission_classes=[AllowAny]
#     def get_queryset(self):
#         token = self.request.query_params.get('token')
#         if not AccessToken.objects.filter(token=token, is_active=True).exists():
#             # from django.http import JsonResponse
#             raise AuthenticationFailed("Invalid or inactive token")
    
#         queryset = super().get_queryset()
#         category_id = self.request.query_params.get('categoryID')
#         if category_id:
#             queryset = queryset.filter(categoryID_id=category_id)
#         return queryset
    
    


# filtering by category ID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()  
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)
        return qs 



    


# logo serializer
class logoSerializer(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

    authentication_classes=[QueryParamAccessTokenAuthentication]
    permission_classes=[AllowAny]
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            # from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset

# banner serializer
class BannershowViewSet(viewsets.ModelViewSet):
    queryset = Bannershow.objects.all()
    serializer_class = BannershowSerializer    # this is serializer

    authentication_classes = [QueryParamAccessTokenAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
    
    

class BannerProductViewSet(viewsets.ModelViewSet):
    queryset = BannerProduct.objects.all()
    serializer_class = BannerProductSerializer

    authentication_classes=[QueryParamAccessTokenAuthentication]
    permission_classes=[AllowAny]
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            # from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset

# category serializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    authentication_classes=[QueryParamAccessTokenAuthentication]
    permission_classes=[AllowAny]
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            # from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
    

# Brand
# class BrandViewSet(viewsets.ModelViewSet):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer

    
# PriceRange serializer
class PriceRangeViewSet(viewsets.ModelViewSet):
    queryset = PriceRange.objects.all()
    serializer_class = PriceRangeSerializer

    
# Tag serializer
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
# QR Payment Method serializer
class QRPaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = QRPaymentMethod.objects.all()
    serializer_class = QRPaymentMethodSerializer

    authentication_classes=[QueryParamAccessTokenAuthentication]
    permission_classes=[AllowAny]
    def get_queryset(self):
        token = self.request.query_params.get('token')
        if not AccessToken.objects.filter(token=token, is_active=True).exists():
            # from django.http import JsonResponse
            raise AuthenticationFailed("Invalid or inactive token")
    
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('categoryID')
        if category_id:
            queryset = queryset.filter(categoryID_id=category_id)
        return queryset
    

# Instagram Section serializer
class InstagramSectionViewSet(viewsets.ModelViewSet):
    queryset = InstagramSection.objects.all()
    serializer_class = InstagramSectionSerializer

    
# Instagram Image serializer
class InstagramImageViewSet(viewsets.ModelViewSet):
    queryset = InstagramImage.objects.all()
    serializer_class = InstagramImageSerializer

    
# About Us serializer
class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutusSerializer

    
# Testimonial serializer
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    
# Team Member serializer
class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    
    
class FooterLinkViewSet(viewsets.ModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer

class FooterWidgetViewSet(viewsets.ModelViewSet):
    queryset = FooterWidget.objects.all()
    serializer_class = FooterWidgetSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

   

    
    
# Place Order
@api_view(['POST'])
def place_order(request):
    if request.method == 'POST':
        data = request.data
        form = CheckoutForm(data)

        if form.is_valid():
            order = form.save(commit=False)
            order.total = Decimal('0.00')
            order.save()

            for item in order.items.all():
                product_id = item.get('product')
                quantity = item.get('quantity')
                price = item.get('price')

                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=quantity,
                    price=price
                )
                order.total += Decimal(price) * quantity

            order.save()

            return Response({'message': 'Order placed successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
# end place order

    


    
   



# Paymentbyqrtemplate


# order payment view
def order_payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context={
        'order': order,
    }
    return render(request, 'api/order_payment.html', context)




# Product list by category

def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'api/productsList.html',context)





def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'api/product_detail.html',context)



# start 



# crud product
def product_crud(request):
    
    return render(request, 'api/product_crud.html')



def home(request):
    DTlogo = Logo.objects.all()  
    DTslideshow = Bannershow.objects.all()  
    TDbBlogSectionBegin = LatestNews.objects.all()  
    blogs = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3] 
    banners = BannerProduct.objects.all()
    section = InstagramSection.objects.first()
    images = section.images.all() if section else []
    products = Product.objects.all()
    footer_widgets = FooterWidget.objects.all()
    context = {
        'logos': DTlogo,  
        'Bannershows': DTslideshow,
        'LatestNews': TDbBlogSectionBegin,
        'blogs': blogs,
        'insta_section': section,
        'banners': banners,
        'insta_images': images,
        'products': products,
        'footer_widgets': footer_widgets,
      
    }
    return render(request, 'accounts/index.html', context)

def SIgninAccount(request):
    return render(request, 'accounts/SIgninAccount.html')


def about(request):
    DTlogo = Logo.objects.all() 
    TBaboutUS = AboutUs.objects.all()  
    TBTestimonial = Testimonial.objects.all()  
    TBTeamMember = TeamMember.objects.all()  
    blogs = BlogPost.objects.filter(is_published=True)
    footer_widgets = FooterWidget.objects.all()
    context = {
        'logos': DTlogo,  
        'AboutUss': TBaboutUS,
        'Testimonials': TBTestimonial,
        'TeamMembers': TBTeamMember,
        'footer_widgets': footer_widgets,
        'blogs': blogs

    }
    return render(request, 'accounts/about.html',context)


#  Correct (remove ContactForm)
from .forms import CheckoutForm, ContactMessageForm
def contact(request):
    # Get data needed to display on the contact page
    logos = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    blogs = BlogPost.objects.filter(is_published=True)

    if request.method == 'POST':
        form = ContactMessageForm(request.POST)  # Get submitted form data
        if form.is_valid():
            form.save()  # Save the contact message to database
            messages.success(request, "Your message has been sent.")
            return redirect('contactpage')  # Redirect to the same page (or wherever)
    else:
        form = ContactMessageForm()  # Show empty form for GET requests

    # Prepare data for the template
    context = {
        'logos': logos,
        'footer_widgets': footer_widgets,
        'blogs': blogs,
        'form': form,  # The form instance to render in the template
    }

    return render(request, 'accounts/contact.html', context)


def shop_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_images = ProductImage.objects.filter(product=product)
    products = Product.objects.all()
    DTlogo = Logo.objects.all()  #  get all logo objects
    footer_widgets = FooterWidget.objects.all()
    blogs = BlogPost.objects.filter(is_published=True)

    context = {
        'logos': DTlogo,  #  pass queryset, not string
        'product': product,
        'product_images': product_images,
        'footer_widgets': footer_widgets,
        'products': products,
        'blogs': blogs
    }

    return render(request, 'accounts/shopdetails.html', context)


def blogdetails(request, slug):
    # Get logo and footer data
    DTlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    post = get_object_or_404(BlogPost, slug=slug)
    blogs = BlogPost.objects.filter(is_published=True)
    
    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval")
            return redirect('blogdetailspage', slug=post.slug)
    else:
        form = CommentForm()

    # Only show approved comments
    approved_comments = post.comments.filter(approved=True)

    context = {
        'logos': DTlogo,
        'footer_widgets': footer_widgets,
        'post': post,
        'form': form,
        'comments': approved_comments,  # Pass filtered comments to template
        'blogs': blogs
    }
    return render(request, 'accounts/blogdetails.html', context)


# blog 
def blog(request):
    DTlogo = Logo.objects.all()  #  get all logo objects
    TDbBlogSectionBegin = LatestNews.objects.all()  #  get all latest news objects
    footer_widgets = FooterWidget.objects.all()
    blogs = BlogPost.objects.filter(is_published=True)
    context = {
        'logos': DTlogo,  #  pass queryset, not string
        'LatestNews': TDbBlogSectionBegin,
        'footer_widgets': footer_widgets,
        'blogs': blogs
    }
    return render(request, 'accounts/blog.html', context)




# shop view by category, brand, price range
def shop(request, category_id=None,brand_id=None, price_range_id=None ):  
    categories = Category.objects.all()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if brand_id:
        # brand_id = get_object_or_404(Brand, id=brand_id)
        products = products.filter(brand__id=brand_id)
   
    if price_range_id:
        products = Product.objects.filter(price_range__id=price_range_id)
    brands = Brand.objects.all() # this is brand
    price_ranges = PriceRange.objects.all() # this is price range 
    tags = Tag.objects.all()
    products = Product.objects.all()  # or filter by some criteria
    DTlogo = Logo.objects.all()  #  get all logo objects
    footer_widgets = FooterWidget.objects.all()
    blogs = BlogPost.objects.filter(is_published=True)
    context={
            'blogs': blogs,
            'logos': DTlogo,  
            'products': products,
            'footer_widgets': footer_widgets,
            'categories': categories,
            'brands': brands,        
            'price_ranges': price_ranges,
            'tags': tags,
            'selected_category_id': category_id,
            
        }
    return render(request, 'accounts/shop.html',context)


# shop by category and tag
def shop_by_category(request, category_id):
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    categories = Category.objects.all()

    context = {
        'selected_category': selected_category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'accounts/shop.html', context)



def shop_by_tag(request, tag_id):
    selected_tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=selected_tag)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'selected_tag': selected_tag,
        'products': products,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'accounts/shop.html', context)

# end




# blog listapi
from .models import LatestNews
# from .serializers import LastNewsSerializer

def Blog_list_api_test(request):
    blogs = LatestNews.objects.all()  
    serializer = LastNewsSerializer(blogs, many=True)
    return JsonResponse(serializer.data, safe=False)

    
def blog_list_api(request):
    blogs = LatestNews.objects.all()
    context={
        'blogs':blogs
    }
    return render(request, 'api/block_list.html',context)



def blog_detail_template(request, pk):
    blog = get_object_or_404(LatestNews, pk=pk)
    context = {
        'blog_id': pk,      # if you still want to show ID separately
        'blog': blog        # this is required for blog.image.url etc.
    }
    return render(request, 'api/blog_detail.html', context)



def add_to_cart_view(request, product_id):
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    return redirect('shopping_cartpage')  # Redirect to cart page

@require_POST
def update_cart(request):
    cart = request.session.get('cart', {})

    # Update quantities
    for key, value in request.POST.items():
        if key.startswith('qty_'):
            product_id = key.split('_')[1]
            try:
                quantity = int(value)
                if quantity > 0:
                    cart[product_id] = quantity
                else:
                    cart.pop(product_id, None)
            except ValueError:
                continue

    request.session['cart'] = cart
    return redirect('shopping_cartpage')



# create acc and login api start

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'message': 'User created', 'token': token.key})

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_api(request):
    return Response({'message': f'Hello, {request.user.username}. You have access!'})


from django.shortcuts import render

def register_login_page(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context={
        'username': username
    }
    return render(request, 'api/register-login.html',context)

def registerApi(request):
    return render(request, 'api/register.html')

# login end



def checkout(request):
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()

    blogs = BlogPost.objects.filter(is_published=True)

    cart = get_user_cart(request)
    cart_items = cart.items.all()
    total = sum(item.total_price for item in cart_items)

    if not cart_items.exists():
        return redirect('cart')

    context = {
        'cart_items': cart_items,
        'total': total,
        'blogs': blogs,
        'logos': TDlogo,
        'footer_widgets': footer_widgets,
    }
    return render(request, 'accounts/checkout.html', context)








# checkout page


def get_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
        'logos': Logo.objects.all(),
        'footer_widgets': FooterWidget.objects.all(),
    }
    return render(request, 'accounts/cart.html', context)









def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_id_str = str(product.id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    return redirect('shopping_cartpage')


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.success(request, "Item removed from cart")
    return redirect('shopping_cartpage')


@require_POST
def update_cart(request):
    cart = request.session.get('cart', {})
    for key, value in request.POST.items():
        if key.startswith('qty_'):
            product_id = key.split('_')[1]
            try:
                quantity = int(value)
                if quantity > 0:
                    cart[product_id] = quantity
                else:
                    cart.pop(product_id, None)
            except ValueError:
                continue
    request.session['cart'] = cart
    messages.success(request, "Cart updated successfully")
    return redirect('shopping_cartpage')


def shopping_cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    context = {
        'cart_items': cart_items,
        'total': total,
        'logos': Logo.objects.all(),
        'footer_widgets': FooterWidget.objects.all(),
    }
    return render(request, 'accounts/shoppingcart.html', context)


def checkout(request):
    
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('shopping_cartpage')

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        
        'cart_items': cart_items,
        'total': total,
        'logos': TDlogo,
        'footer_widgets': footer_widgets,

    }
    return render(request, 'accounts/checkout.html', context)


def get_cart_items_and_total(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    return cart_items, total


# place order
def place_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not all([first_name, last_name, email, phone, address]):
            messages.error(request, "All fields are required.")
            return redirect('checkoutpage') # have all infocan open checkout

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('shopping_cartpage') 

        total = 0
        cart_items = []
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
            total += total_price

        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price  
            )

         # Clear the cart
        request.session['cart'] = {}

        # Handle different payment methods
        if payment_method == 'qrpay':
            messages.info(request, "Please scan the QR code and send proof of payment.")
            return redirect('qr_payment_instructions', order_id=order.id)

        # request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)

    return redirect('checkoutpage')


def order_confirmation(request, order_id):
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
        'logos': TDlogo,
        'footer_widgets': footer_widgets
    }

    return render(request, 'accounts/order_confirmation.html',context)

# qrpayment

def qr_payment_instructions(request, order_id):
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    order = get_object_or_404(Order, id=order_id)
    qr_methods = QRPaymentMethod.objects.all()

    context={
        'order': order,
        'qr_methods': qr_methods,
        'logos': TDlogo,
        'footer_widgets': footer_widgets,
    }

    return render(request, 'Orders/qr_payment_instructions.html',context)

def submit_qr_payment(request, order_id):
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()
    
    if request.method == 'POST':
        qr_method_id = request.POST.get('qr_method_id')
        order = get_object_or_404(Order, id=order_id)

        if qr_method_id:
            qr_method = get_object_or_404(QRPaymentMethod, id=qr_method_id)
            order.qr_method = qr_method
            order.save()
            return redirect('qr_thank_you', order_id=order.id)
        else:
            # Optional: Handle if no selection
            return redirect('qr_payment_instructions', order_id=order.id)
    context={
        'logos': TDlogo,
        'footer_widgets': footer_widgets,

    }

    return redirect('homepage',context)

def qr_thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    TDlogo = Logo.objects.all()
    footer_widgets = FooterWidget.objects.all()


    context={
        'logos': TDlogo,
        'footer_widgets': footer_widgets,
        'order': order,

    }
    return render(request, 'orders/qr_thank_you.html',context)




# invoice_Downloads

from django.template.loader import render_to_string
from weasyprint import HTML


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    # Render HTML template
    html_string = render_to_string('accounts/invoice_template.html', {
        'order': order,
        'order_items': order_items,
    })
    
    # Create PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    result = html.write_pdf()
    
    # Create response
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Invoice_{order.id}.pdf'
    return response










