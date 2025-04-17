from django.contrib import admin
from .models import HobbyGroup, Hobby

class HobbyInline(admin.TabularInline):
    model = Hobby
    extra = 0

@admin.register(HobbyGroup)
class HobbyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_hobby_ids')
    inlines = [HobbyInline]

    def get_hobby_ids(self, obj):
        return obj.get_hobby_ids()
    get_hobby_ids.short_description = 'ID хобби'