# import sys
# from PIL import Image
# from io import BytesIO

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    # MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = (800, 800)
    # MAX_IMAGE_SIZE = 3145728

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Photo')
    description = models.TextField(verbose_name='Text', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     # image = self.image
    #     # img = Image.open(image)
    #     # min_height, min_width = self.MIN_RESOLUTION
    #     # max_height, max_width = self.MAX_RESOLUTION
    #     # if img.height < min_height and img.width < min_width:
    #     #     raise MinResolutionErrorException('Upload image size less than min size!')
    #     # if img.height > max_height and img.width > max_width:
    #     #     raise MaxResolutionErrorException('Upload image size bigger than max size!')
    #     # super().save(*args, **kwargs)
    #     image = self.image
    #     img = Image.open(image)
    #     new_image = img.convert('RGB')
    #     resized_new_img = new_image.resize((200, 200), Image.ANTIALIAS)
    #     filestream = BytesIO()
    #     resized_new_img.save(filestream, 'JPEG', quility=90)
    #     filestream.seek(0)
    #     name = '{}'.format(self.image.name.split('.'))
    #     self.image = InMemoryUploadedFile(
    #         filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    #     )
    #     super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return f'Product: {self.product.title}'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Owner', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name='Total price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='User orders', related_name='related_customer')

    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOISES = (
        (STATUS_NEW, 'New Order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Completed'),
    )

    BUYING_TYPE = (
        (BUYING_TYPE_SELF, 'Customer'),
        (BUYING_TYPE_DELIVERY, 'Delivery'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Customer', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    phone = models.CharField(max_length=255, verbose_name='Phone')
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address')
    status = models.CharField(max_length=1024, verbose_name='Status', choices=STATUS_CHOISES, default=STATUS_NEW)
    buying = models.CharField(max_length=1024, verbose_name='Buying', choices=BUYING_TYPE, default=BUYING_TYPE_DELIVERY)
    comment = models.TextField(verbose_name='Comment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Add to database')
    order_date = models.DateField(verbose_name='Data will complete', default=timezone.now)

    def __str__(self):
        return str(self.id)
