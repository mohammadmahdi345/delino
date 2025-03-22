from datetime import datetime

from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator




class City(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Restorant(models.Model):
    name = models.CharField(max_length=15,unique=True)
    description = models.TextField(max_length=200,null=True, blank=True)
    phone_number = models.CharField(max_length=13,unique=True,null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        ('Enter a valid mobile number.'), 'invalid'),
                                          ])

    star = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_time = models.DateTimeField(auto_now=True)
    meno = models.ManyToManyField('Food')
    address = models.TextField(max_length=150)
    min_post_time = models.PositiveIntegerField(default=45)  # حداقل زمان (دقیقه)
    max_post_time = models.PositiveIntegerField(default=120)  # حداکثر زمان (دقیقه)


    def __str__(self):
        return self.name



class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)
    avatar = models.ImageField(upload_to='foods/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

class Like(models.Model):
    res = models.ForeignKey(to='Restorant', on_delete=models.PROTECT, related_name='likes',default=2)
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'res')



# from django.contrib.gis.db import models
# class Location(models.Model):
#     name = models.CharField(max_length=255)
#     coordinates = models.PointField()  # ذخیره مختصات (طول و عرض جغرافیایی)
#
#     def __str__(self):
#         return f"{self.name} - {self.coordinates}"
#


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'در انتظار پرداخت'),
        ('PROCESSING', 'در حال پردازش'),
        ('SHIPPED', 'ارسال شده'),
        ('DELIVERED', 'تحویل داده شده'),
    ]
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    gateway = models.ForeignKey('user.Gateway',on_delete=models.CASCADE)
    res = models.ForeignKey('Restorant',on_delete=models.CASCADE)
    food = models.ForeignKey('Food',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,default='PENDING')
    last_update = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status
            if old_status != self.status:
                self.last_update = datetime.now()
        super().save(*args, **kwargs)

    def total_price(self):
        return self.quantity * self.food.price

    def __str__(self):
        return f"{self.user} ordered {self.quantity}x {self.food.name}"