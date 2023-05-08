from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'description_start', 'created_at', 'updated_at', 'image', 'thumbnail', 'likes_count']
    readonly_fields = ['thumbnail', 'created_at', 'updated_at']
    filter_horizontal = ['likes']
    search_fields = ['author', 'description']
    sortable_by = ['author', 'created_at', 'updated_at']
    fieldsets = (
        ('Author', {'fields': ('author',)}),
        ('Image', {'fields': ('image', 'thumbnail')}),
        ('Description', {'fields': ('description',)}),
        ('Status', {'fields': ('is_archive',)}),
        ('Created/Updated', {'fields': ('created_at', 'updated_at')}),
        ('Likes', {'fields': ('likes',)})
    )
    
    def likes_count(self, obj):
        return obj.likes.all().count()
    
    def description_start(self, obj):
        return obj.description[:21]

