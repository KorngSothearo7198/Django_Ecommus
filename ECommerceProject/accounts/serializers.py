from decimal import Decimal
import json
from django.forms import DecimalField
from rest_framework import serializers

from .models import *
from accounts.models import *
from accounts.models import LatestNews


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'



# class ProductSerializer(serializers.ModelSerializer):
#     category_id = serializers.IntegerField(source='category.id', allow_null=True)
    
#     class Meta:
#         model = Product
#         fields = [
#             'id', 'name', 'image', 'price', 'old_price', 'rating', 
#             'category_id', 'is_best_seller', 'is_new_arrival', 'is_hot_sale'
#         ]
#         read_only_fields = fields

        


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'is_video', 'video_url']


from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand = serializers.StringRelatedField()
    price_range = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    image = serializers.SerializerMethodField()  # override to get full URL

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'sku',
            'description',
            'price',
            'old_price',
            'rating',
            'category_id',
            'category_name',
            'is_best_seller',
            'is_new_arrival',
            'is_hot_sale',
            'brand',
            'price_range',
            'tags',
            'label',
            'sizes',
            'colors',
            'image',
            'images',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None





# Report and Order show api

class OrderItemSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'productName', 'quantity', 'price', 'get_total_price']

 # order
class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customerName = serializers.SerializerMethodField()
    customerPhone = serializers.SerializerMethodField()
    orderDate = serializers.DateTimeField(source='created_at', read_only=True)
    totalAmount = serializers.DecimalField(source='total', max_digits=10, decimal_places=2, read_only=True)
    QRCodeInvoice = serializers.ImageField(source='qr_method.qr_image', read_only=True)  
    paymentMethod = serializers.CharField(source='payment_method', read_only=True)  


    class Meta:
        model = Order
        fields = ['id', 'customerName', 'customerPhone', 'orderDate', 'totalAmount', 'QRCodeInvoice', 'items','paymentMethod']

    def get_items(self, obj):
        return OrderItemSerializer(obj.items.all(), many=True).data

    def get_customerName(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_customerPhone(self, obj):
        return obj.phone

    def create(self, validated_data):
        request = self.context.get('request')
        items_json = request.data.get('items')
        items_data = json.loads(items_json) if items_json else []

        validated_data.pop('items', None)  # Remove if present

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity')
            price = item_data.get('price')

            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=quantity,
                price=price
            )

        return order
    


# show payment 
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'payment_method', 'status']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product_name', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'payments', 'total_amount']

    def get_total_amount(self, obj):
        total = sum((item.product.price * item.quantity for item in obj.items.all()), Decimal('0.00'))
        return total


# blockPos

from .models import BlogPost, Comment

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

# BlogPost
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



# blog page api
class LastNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestNews
        fields = '__all__'


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = '__all__'



class BannershowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bannershow
        fields = '__all__'

class BannerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerProduct
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class PriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRange
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class QRPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRPaymentMethod
        fields = '__all__'

    def create(self, validated_data):
        # Custom logic for creating an access token if needed
        return super().create(validated_data)

class InstagramSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramSection
        fields = '__all__'

class InstagramImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramImage
        fields = '__all__'

class AboutusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = '__all__'

class FooterWidgetSerializer(serializers.ModelSerializer):
    links = FooterLinkSerializer(many=True, read_only=True)

    class Meta:
        model = FooterWidget
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'







class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # ឬ ProductInventory
        fields = '__all__'




from rest_framework import serializers
from .models import Product, OrderItem
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

class ProductReportSerializer(serializers.ModelSerializer):
    total_sold = serializers.SerializerMethodField()
    count_sale = serializers.SerializerMethodField()
    total_sale_amount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'total_sold', 'count_sale', 'total_sale_amount']

    def get_total_sold(self, obj):
        return OrderItem.objects.filter(product=obj).aggregate(total=Sum('quantity'))['total'] or 0

    def get_count_sale(self, obj):
        return OrderItem.objects.filter(product=obj).values('order').distinct().count()

    def get_total_sale_amount(self, obj):
        return OrderItem.objects.filter(product=obj).aggregate(
            total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField()))
        )['total'] or 0











from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from rest_framework import serializers
from .models import Product, OrderItem

class ProductSalesReportSerializer(serializers.ModelSerializer):
    total_quantity_sold = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    total_sales_amount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'total_quantity_sold', 'order_count', 'total_sales_amount']

    def get_total_quantity_sold(self, product):
        return OrderItem.objects.filter(product=product).aggregate(
            total_qty=Sum('quantity')
        )['total_qty'] or 0

    def get_order_count(self, product):
        return OrderItem.objects.filter(product=product).values('order').distinct().count()

    def get_total_sales_amount(self, product):
        return OrderItem.objects.filter(product=product).aggregate(
            total_amount=Sum(
                ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
            )
        )['total_amount'] or 0





# payment Report 
class PaymentSummarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cart_id = serializers.IntegerField(source='cart.id')

    class Meta:
        model = Payment
        fields = ['id', 'cart', 'user', 'amount', 'payment_date', 'payment_method', 'status']

    def get_user(self, obj):
        user = obj.cart.user
        if user:
            return {'username': user.username, 'email': user.email}
        return None
