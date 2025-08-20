# from django.contrib import admin
# from .models import *
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

# # Register your models here.\

# admin.site.site_header = "E-Commerce Admin By Smos5"
# admin.site.site_title = "E-Commerce Admin Portal"   
# admin.site.index_title = "Welcome to E-Commerce Admin Portal"







# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email', 'total', 'payment_method', 'created_at']
#     search_fields = ['first_name', 'last_name', 'email']
#     list_filter = ['created_at', 'payment_method']
#     inlines = [OrderItemInline]

#     def order_total(self, obj):
#         return obj.total
#     order_total.short_description = 'Total'



# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order', 'product', 'quantity', 'price']
#     list_filter = ['order', 'product']
#     search_fields = ['order__id', 'product__name']


# @admin.register(AccessToken)
# class AccessTokenAdmin(admin.ModelAdmin):
#     list_display = ['id', 'token', 'is_active']
#     list_filter = ['is_active']
#     search_fields = ['token']



# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1

# # @admin.register(Product)
# # class ProductAdmin(admin.ModelAdmin):
# #     inlines = [ProductImageInline]

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageInline]
#     list_display = ('name', 'category', 'price', 'rating')
#     search_fields = ('name', 'category')




# class FooterLinkInline(admin.TabularInline):
#     model = FooterLink
#     extra = 1

# @admin.register(FooterWidget)
# class FooterWidgetAdmin(admin.ModelAdmin):
#     inlines = [FooterLinkInline]

# admin.site.register(NewsletterText)


# admin.site.register(Logo)
# admin.site.register(Bannershow)
# admin.site.register(InstagramSection)
# admin.site.register(InstagramImage)
# admin.site.register(LatestNews)
# admin.site.register(AboutUs)
# admin.site.register(Testimonial)
# admin.site.register(TeamMember)
# admin.site.register(Brand)
# admin.site.register(Category)
# admin.site.register(PriceRange)
# admin.site.register(Tag)

# admin.site.register(QRPaymentMethod)

# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'created_at')
#     search_fields = ('name', 'email', 'message')
#     list_filter = ('created_at',)

    
# # admin.site.register(Product)
# # admin.site.register(ProductCategory)
# # admin.site.register(ProductImage)


# @admin.register(BannerProduct)
# class BannerProductAdmin(admin.ModelAdmin):
#     list_display = ['title', 'order', 'position_class']
#     list_editable = ['order', 'position_class']




# # BlockDetails 
# class CommentInline(admin.TabularInline):  # or admin.StackedInline
#     model = Comment
#     extra = 1
#     readonly_fields = ('created_at',)
#     fields = ('name', 'email', 'comment', 'approved', 'created_at')

# @admin.register(BlogPost)
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
#     list_filter = ('is_published', 'created_at', 'author')
#     search_fields = ('title', 'content', 'excerpt')
#     prepopulated_fields = {'slug': ('title',)}
#     inlines = [CommentInline]  # Shows comments inline with blog post
#     date_hierarchy = 'created_at'
    
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'slug', 'author', 'is_published')
#         }),
#         ('Content', {
#             'fields': ('featured_image', 'excerpt', 'content')
#         }),
#         ('Dates', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
#     readonly_fields = ('created_at', 'updated_at')  # Add this line

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'post', 'created_at', 'approved')
#     list_filter = ('approved', 'created_at')
#     search_fields = ('name', 'email', 'comment')
#     list_editable = ('approved',)  # Allows bulk approval
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(approved=True)
#     approve_comments.short_description = "Approve selected comments"




from django.contrib import admin
from .models import *

# Global admin site headers
admin.site.site_header = "E-Commerce Admin By Smos5"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "Welcome to E-Commerce Admin Portal"


# Inline classes for related objects

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('name', 'email', 'comment', 'approved', 'created_at')


# ModelAdmin classes

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total', 'payment_method', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['created_at', 'payment_method']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__id', 'product__name']


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'is_active']
    list_filter = ['is_active']
    search_fields = ['token']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'price', 'rating', 'brand', 'is_best_seller', 'is_new_arrival', 'is_hot_sale']
    list_filter = ['category', 'brand', 'is_best_seller', 'is_new_arrival', 'is_hot_sale']
    search_fields = ['name', 'category__name', 'brand__name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    list_display = ['min_price', 'max_price']
    list_filter = ['min_price', 'max_price']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Bannershow)
class BannerShowAdmin(admin.ModelAdmin):
    list_display = ['title', 'smalltittle']
    search_fields = ['title']


@admin.register(BannerProduct)
class BannerProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'position_class']
    list_editable = ['order', 'position_class']


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at', 'is_published']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    list_editable = ['approved']

    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_key']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'amount', 'payment_date', 'payment_method', 'status']
    list_filter = ['payment_method', 'status']
    search_fields = ['cart__id', 'payment_method']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'added_at']
    list_filter = ['added_at']
    search_fields = ['cart__id', 'product__name']


@admin.register(QRPaymentMethod)
class QRPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(InstagramSection)
class InstagramSectionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(InstagramImage)
class InstagramImageAdmin(admin.ModelAdmin):
    list_display = ['section', 'image']
    search_fields = ['section__title']


@admin.register(LatestNews)
class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'button_text']
    list_filter = ['category', 'date']
    search_fields = ['title']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title1']
    search_fields = ['title1']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'author_title']
    search_fields = ['author_name', 'author_title']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order']
    list_editable = ['order']
    search_fields = ['name', 'position']


@admin.register(FooterWidget)
class FooterWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'widget_type']
    inlines = [FooterLinkInline]


@admin.register(NewsletterText)
class NewsletterTextAdmin(admin.ModelAdmin):
    list_display = ['widget']


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['label', 'widget', 'url']
    search_fields = ['label']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_filter = ['created_at']



from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Customize user admin if needed
admin.site.unregister(User)
admin.site.register(User, UserAdmin)