from apps.medistore.models.category_model import Category
from django.shortcuts import get_object_or_404

def get_all_category():
    return Category.objects.filter(is_active=True)

def get_category(category_id):
    return get_object_or_404(Category, id=category_id, is_active=True)

def get_all_slug():
    return Category.objects.values_list('slug')