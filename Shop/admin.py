from django.contrib import admin
from django.db.models import fields
from .models import *
# Register your models here.

# admin.site.register(Comment)
# admin.site.register(Category)
# admin.site.register(Comment)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets += (
    ('فیلد های خاص من', {
        "fields": (
            'special_user',
            'verify_phone',
            'verify_phone_code',
            'count_sms',
        ),
    }),
)

UserAdmin.list_display += ('is_special_user',)

admin.site.register(User, UserAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = ('title', "author")
    search_fields = ("title",)


admin.site.register(Comment, admin_class=CommentAdmin)


class ImageAdmin(admin.ModelAdmin):
    fields = ('photo', 'image_tag', 'title_for_photo')
    list_display = ("image_tag",)

    readonly_fields = ['image_tag']


admin.site.register(Image, admin_class=ImageAdmin)


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("image", "comment", "Specification", "category")
    search_fields = ("title",)


admin.site.register(Product, admin_class=ProductAdmin)


class SpecificationAdmin(admin.ModelAdmin):
    fields = ("title", "body",)
    search_fields = ("title",)


admin.site.register(Specification, admin_class=SpecificationAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Order, admin_class=OrderAdmin)


class CategoryAdmin(admin.ModelAdmin):
    # filter_horizontal=('main_category',)
    list_display = ("title", "id", "is_main_page")
    search_fields = ("title",)


admin.site.register(Category, admin_class=CategoryAdmin)


class Single_OrderAdmin(admin.ModelAdmin):
    filter_horizontal=('order',)



admin.site.register(Single_Order, admin_class=Single_OrderAdmin)



class heder_imageAdmin(admin.ModelAdmin):
    list_display = ("id", "photo",)


admin.site.register(heder_image, admin_class=heder_imageAdmin)


class heder_left_imageAdmin(admin.ModelAdmin):
    list_display = ("id", "photo",)


admin.site.register(heder_left_image, admin_class=heder_left_imageAdmin)


