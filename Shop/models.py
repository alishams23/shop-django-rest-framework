from tabnanny import verbose
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BigIntegerField, BooleanField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.utils.html import mark_safe
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class User(AbstractUser):
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name="کاربر ویژه")
    verify_phone = models.BooleanField(
        verbose_name="تایید شماره تلفن", blank=True, null=True)
    verify_phone_code = models.BigIntegerField(
        verbose_name="کد تایید", blank=True, null=True)
    count_sms = models.IntegerField(verbose_name="تعداد پیامک", default=0)

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean = True
    is_special_user.short_description = 'کاربر ویژه'

    class Meta:
        verbose_name = "یوزر"
        verbose_name_plural = "یوزر ها"


# Create your models here.

class Category(models.Model):
    is_main_page = BooleanField(
        verbose_name="آیا در صفحه ی اصلی قرار بگیرد؟", default=False)
    title = models.TextField()
    hide=models.BooleanField(default=False,verbose_name="مخفی کردن")
    hide_stock= models.BooleanField(default=False)
    hide_people_product= models.BooleanField(default=False)
    hide_product= models.BooleanField(default=False)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f"{self.pk}--{self.title}"


class Image(models.Model):
    title_for_photo = models.TextField(blank=True, verbose_name="متن برای عکس")
    photo = models.ImageField(verbose_name="عکس")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="نویسنده",blank=True,null=True)

    def image_tag(self):
        return mark_safe('<img src="%s"  height="100" />' % (self.photo.url))
    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['-pk']
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"

    def __str__(self):
        return f"{self.pk}--{self.photo}"


class Comment(models.Model):
    title = models.TextField(verbose_name="متن")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="نویسنده")

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"
        # ordering = ["-createdAdd"]

    def __str__(self):
        return f"{self.pk}--{self.title}"


class Specification(models.Model):
    title = models.TextField(verbose_name="متن")
    body = models.TextField(verbose_name="متن یدنه")

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویؤگی ها"

    def __str__(self):
        return f"{self.pk}--{self.title}"




class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name="دسته بندی", blank=True)
    title = models.TextField(verbose_name="متن", blank=True)
    price = models.BigIntegerField(verbose_name="قیمت")
    description = models.TextField(verbose_name="توضوعات")
    image = models.ManyToManyField(Image, verbose_name="عکس", blank=True)
    comment = models.ManyToManyField(Comment, verbose_name="نظر", blank=True)
    Specification = models.ManyToManyField(
        Specification, verbose_name="ویژگی ها", blank=True)
    amount = models.IntegerField(default=1, verbose_name="موجودی")
    discount = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)], verbose_name="تخفیف")
    is_stock = models.BooleanField(default=False, verbose_name="استوک")
    is_people = models.BooleanField(default=False, verbose_name="محصول مردم")
   
    hide = models.BooleanField(default=False,verbose_name="مخفی کردن")

    def __str__(self):
        return f"{self.pk}--{self.title}"

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"




class Order(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="محصول ")
    count = models.IntegerField(default=1, verbose_name="تعداد")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="نویسنده")

    def __str__(self):
        return f"{self.pk} {self.product}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"


class Single_Order(models.Model):
    order = models.ManyToManyField(Order, verbose_name="دسته بندی", blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name="نویسنده")
    ispayed = BigIntegerField(default=False, verbose_name="پرداخت شده ")
    isfinisheds = BooleanField(default=False, verbose_name="تحویل داده شده")
    created_add = models.DateTimeField(
        auto_now_add=True, verbose_name="زما ساخنه شده")
    updated_add = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید ها"


class heder_image(models.Model):
    photo = models.ImageField(verbose_name="عکس")
    link = models.TextField(verbose_name="لینک", blank=True)

    class Meta:
        verbose_name = "عکس هدر"
        verbose_name_plural = "عکس های هدر"


class heder_left_image(models.Model):
    photo = models.ImageField(verbose_name="عکس")
    link = models.TextField(verbose_name="لینک", blank=True)

    class Meta:
        verbose_name = "عکس سمت چپ"
        verbose_name_plural = "عکس های سمت چپ"
