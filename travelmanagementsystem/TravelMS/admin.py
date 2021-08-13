from django.contrib import admin
from .models import Tag, Post, Category
from django.utils.html import mark_safe

class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }
        js = ('/static/js/script.js', )

    list_display = ["id", "title", "content", "active", "created_date", "category", "user"]
    search_fields = ["title", "active", "user__username", "active", "category__name"]
    list_filter = ["title", "category"]
    readonly_fields = ["avatar"]

    def avatar(self, post):
        return mark_safe("<img src='/static/{url_img}' alt='{alt}' width='160px'/>".format(url_img=post.image.name, alt=post.title))

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]

# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
