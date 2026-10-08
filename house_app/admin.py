from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Property, PropertyImage, Review, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone_number', 'role', 'preferred_language')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('phone_number', 'role', 'preferred_language')}),
    )
    list_display = ('username', 'email', 'role', 'preferred_language')
    list_filter = ('role',)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'property_type', 'city', 'price', 'currency', 'seller', 'is_approved', 'created_at')
    list_filter = ('property_type', 'deal_type', 'is_approved', 'region')
    search_fields = ('title', 'city', 'address')

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.init.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'seller', 'rating', 'created_at')