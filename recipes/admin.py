from django.contrib import admin
from recipes.models import User, UserProfile, Recipe, Review, Category, Like

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Like)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved', 'created_by')
    list_editable = ('is_approved',)
    actions = ['approve_categories']
    
    def save_model(self, request, obj, form, change):
        if request.user.is_staff:
            obj.is_approved = True
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)
    
    def approve_categories(self, request, queryset):
        queryset.update(is_approved=True, approved_by=request.user)
    approve_categories.short_description = "Approve selected categories"