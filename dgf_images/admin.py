from django.contrib import admin

from .models import ImageGenerator


@admin.register(ImageGenerator)
class ImageGeneratorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': (
                'name',
                'slug',
                'active',
            )}
         ),
    )

    ordering = ('-active', 'name',)
    list_display = ('name', 'slug', 'active')
    list_editable = ('active',)
    search_fields = ('name', 'slug')
