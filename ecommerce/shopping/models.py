from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from tinymce.models import HTMLField

# Create your models here.
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+?1?\d{9,15}$'
state_choices = [
    ('default', 'Select State'),
    ('andaman_and_nicobar_islands', 'Andaman and Nicobar Islands'),
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('arunachal_pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chandigarh', 'Chandigarh'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('dadra_and_nagar_haveli', 'Dadra and Nagar Haveli'),
    ('daman_and_diu', 'Daman and Diu'),
    ('delhi', 'Delhi'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jammu_and_kashmir', 'Jammu and Kashmir'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('ladakh', 'Ladakh'),
    ('lakshadweep', 'Lakshadweep'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('puducherry', 'Puducherry'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal'),
]


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False,
                            validators=[RegexValidator(regex=name_pattern, message="Please enter a valid name.")])
    phone = models.CharField(max_length=11, blank=False, validators=[
        RegexValidator(regex=phone_pattern, message="Please enter a valid Phone number.")])
    locality = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=False,
                            validators=[RegexValidator(regex=name_pattern, message="Please enter a valid city name.")])
    zipcode = models.IntegerField(blank=False)
    state = models.CharField(choices=state_choices, max_length=50, default='Select State', blank=False)

    def __str__(self):
        return str(self.id)


class category_master(models.Model):
    cat_name = models.CharField(max_length=100, blank=False, validators=[
        RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    status = models.BooleanField(default=True, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images/cat_image/', blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    cat_descr = HTMLField(blank=True, default='')
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    title = models.CharField(max_length=255, blank=False)
    selling_price = models.FloatField(max_length=4)
    discounted_price = models.FloatField(max_length=4)
    short_description = models.TextField()
    description = HTMLField(blank=True, default='')
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(category_master, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product')
    status = models.BooleanField(default=True, null=False)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)



status_choice = [
    ('accepted', 'Accepted'),
    ('packed', 'Packed'),
    ('on_the_way', 'On the way'),
    ('delivered', 'Delivered'),
    ('cancel', 'Cancel'),
]


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=status_choice, default='Pending')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price