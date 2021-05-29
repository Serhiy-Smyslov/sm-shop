from django.contrib import admin

from specs import models


admin.site.register(models.CategoryFeature)
admin.site.register(models.ProductFeatures)
admin.site.register(models.FeatureValidator)