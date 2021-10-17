from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django import forms

from .models import (
    Tag,
    Post,
    Category,
    User,
    Tour,
    TourSchedules,
    TourImages,
    Rating,
    CommentTour,
    CommentPost,
    ActionPost
)

from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Post
        fields = '__all__'

class TagInline(admin.TabularInline):
    model = Post.tags.through

class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }
        js = ('/static/js/script.js', )

    form = PostForm
    inlines = (TagInline, )
    list_display = ["id", "title", "active", "created_date", "category", "user"]
    search_fields = ["title", "active", "user__username", "active", "category__name"]
    list_filter = ["title", "category"]
    readonly_fields = ["avatar"]

    def avatar(self, post):
        return mark_safe("<img src='/{url_img}' alt='{alt}' width='160px'/>".format(url_img=post.image.name, alt=post.title))

class PostInline(admin.StackedInline):
    model = Post
    fk_name = 'category'

class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline, )
    list_display = ["id", "name"]
    search_fields = ["name"]

class TourAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "tour_type", "image", "tour_days",
                "tour_nights", "adults_price", "children_price", "created_date",
                "updated_date", "start_date", "end_date", "active"]
    search_fields = ["name"]

class TourSchedulesAdmin(admin.ModelAdmin):
    list_display = ["id", "tour", "departure", "destination", "start_date", "end_date"]
    search_fields = ["departure", "destination"]

class TourImagesAdmin(admin.ModelAdmin):
    list_display = ["id", "tour", "image"]
    search_fields = ["id", "tour"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "email", "is_staff", "is_superuser", "is_active"]
    list_filter = ["id", "username", "first_name", "last_name", "is_staff"]
    search_fields = ["id", "username", "first_name", "last_name"]
    readonly_fields = ["image"]

    def image(self, user):
        return mark_safe("<img src='/{img_url}' alt='{alt}' width='150px' />".format(img_url=user.avatar.name, alt=user.first_name))


class TravelMSAppAdminSite(admin.AdminSite):
    site_header = 'Travel Management System'

    def get_urls(self):
        return [
            path('travel-stats/', self.travel_stats)
        ] + super().get_urls()

    def travel_stats(self, request):

        post_count = Post.objects.count()
        stats = Category.objects.annotate(count=Count('post')).values("id", "name", "count")
        return TemplateResponse(request, 'admin/travel-stats.html', {
            'post_count': post_count,
            'stats': stats
        })


admin_site = TravelMSAppAdminSite('My app travel')


# Register your models here.
# admin.site.register(Tag, TagAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Category, CategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Post, PostAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Tour, TourAdmin)
admin_site.register(TourSchedules, TourSchedulesAdmin)
admin_site.register(TourImages, TourImagesAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Permission)
admin_site.register(Group)
