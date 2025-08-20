from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# from .models import QRPaymentMethod  # if QRPaymentMethod is in the same app

#Token access
class AccessToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()



# Create your models here.

class Logo(models.Model):
    logo = models.ImageField(upload_to='logos/', default='logos/default_logo.png')

    def __str__(self):
        return "Logo"
    
class Bannershow(models.Model):
    title = RichTextField(max_length=100, default='Slideshow Title')
    smalltittle = RichTextField(max_length=100, default='Slideshow Small Title')
    image = models.ImageField(upload_to='slideshows/', default='slideshows/default_slideshow.png')
    description = RichTextField(default='Slideshow Description')

    def __str__(self):
        return "Slideshow"
    

class BannerProduct(models.Model):
    title = RichTextField(max_length=255)
    image = models.ImageField(upload_to='bannersProduct/')
    link = models.URLField(default="#" , null=True, blank=True)
    position_class = models.CharField(max_length=100, blank=True, help_text="e.g. banner__item--middle")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    def get_col_width(self):
        if "Accessories" in self.title:
            return 5
        return 7

    def __str__(self):
        return self.title






class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class PriceRange(models.Model):
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        if self.min_price and self.max_price:
            return f"${self.min_price} - ${self.max_price}"
        elif self.min_price:
            return f"${self.min_price}+"
        return "Price range"

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name
    



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rating = models.IntegerField(default=0)  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_hot_sale = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price_range = models.ForeignKey(PriceRange, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    label = models.CharField(max_length=50, blank=True, null=True)  # e.g. New, Hot
    sizes = models.JSONField(default=list, blank=True)  # example: ["S", "M", "L", "XL"]
    colors = models.JSONField(default=list, blank=True) # example: ["c-1", "c-2", "c-3"]
    image = models.ImageField(upload_to='products/')  # main image
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    is_main = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"




# poat and comm Model


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    featured_image = models.ImageField(upload_to='blog/', verbose_name="Featured Image")
    # content = RichTextField(verbose_name="Content")
    content = RichTextField(verbose_name="Content")
    excerpt = RichTextField(blank=True, verbose_name="Excerpt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    is_published = models.BooleanField(default=False, verbose_name="Published")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    # comment = CKEditor5Field(verbose_name="Comment")
    comment = RichTextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    approved = models.BooleanField(default=False, verbose_name="Approved")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"



# payment

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    cart = models.ForeignKey(Cart, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='completed')

    def __str__(self):
        return f"Payment {self.amount} for Cart {self.cart.id}"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = RichTextField(verbose_name="Shipping Address", blank=True, null=True)
    email = models.EmailField()
    payment_method = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    qr_method = models.ForeignKey('QRPaymentMethod', null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"Order {self.id} by {self.email}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # protect so products can't be deleted if ordered
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
    # @property
    def get_total_price(self):
        return (self.price or 0) * (self.quantity or 0)
    

from django.db import models


class QRPaymentMethod(models.Model):
    name = models.CharField(max_length=100)  # e.g., ABA, Wing
    qr_image = models.ImageField(upload_to='qr_codes/')
    # description = CKEditor5Field(blank=True, null=True)
    description = RichTextField(blank=True, null=True)


    def __str__(self):
        return self.name


    



    








class InstagramSection(models.Model):
    title = models.CharField(max_length=100, default='Instagram')
    description = CKEditor5Field()
    hashtag = models.CharField(max_length=100, default='#Male_Fashion')

    def __str__(self):
        return self.title


class InstagramImage(models.Model):
    section = models.ForeignKey(InstagramSection, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='instagram_images/')

    def __str__(self):
        return f"Image for {self.section.title}"




#blog page 
class LatestNews(models.Model):
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('tech', 'Tech'),
        ('sport', 'Sport'),
        # add more categories as needed
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fashion')
    image = models.ImageField(upload_to='news_images/')
    date = models.DateField(auto_now_add=True)
    button_text = models.CharField(max_length=100, default='Read More')

    def __str__(self):
        return self.title 
    


# about page

class AboutUs(models.Model):
    main_image = models.ImageField(upload_to='about_us/')
    title1 = models.CharField(max_length=100)
    content1 = RichTextField()
    title2 = models.CharField(max_length=100)
    content2 = RichTextField()
    title3 = models.CharField(max_length=100)
    content3 = RichTextField()
    def __str__(self):
        return self.title1
    
class Testimonial(models.Model):
    quote = RichTextField()
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100)
    # author_title = models.CharField()
    author_image = models.ImageField(upload_to='testimonials/')
    background_image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return f"Testimonial by {self.author_name} "
    
# Meet Our Team
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)  # For sorting team members

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    





# footer 

class FooterWidget(models.Model):
    title = models.CharField(max_length=100)  # ex: "Shopping", "Newsletter"
    widget_type = models.CharField(
        max_length=50,
        choices=[('link_list', 'Link List'), ('newsletter', 'Newsletter')],
        default='link_list'
    )

    def __str__(self):
        return self.title


class NewsletterText(models.Model):
    widget = models.OneToOneField(FooterWidget, on_delete=models.CASCADE, limit_choices_to={'widget_type': 'newsletter'})
    description = RichTextField()

    def __str__(self):
        return f"Newsletter: {self.widget.title}"


class FooterLink(models.Model):
    widget = models.ForeignKey(FooterWidget, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)  # ex: "Clothing Store"
    url = models.URLField(default="#")        # ex: "/clothing/"

    def __str__(self):
        return f"{self.label} ({self.widget.title})"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"