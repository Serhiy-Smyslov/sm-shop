from PIL import Image

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import *


class LaptopAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color: red; font-size: 12px;">Upload files '
            'in max size({} x {}) or they will be change.</span>'.format(
                *Product.MAX_RESOLUTION))

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Upload image volume bigger than 3 Mb!')
    #     if img.height < min_height and img.width < min_width:
    #         raise ValidationError('Upload image size less than min size!')
    #     if img.height > max_height and img.width > max_width:
    #         raise ValidationError('Upload image size bigger than max size!')
    #     return image


class LaptopAdmin(admin.ModelAdmin):
    form = LaptopAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='laptop'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Customer)
