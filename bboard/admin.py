from django.contrib import admin

from .models import Bb
from .models import Rubric, Img

class BbInline(admin.StackedInline):
    model = Bb

class RubricAdmin(admin.ModelAdmin):
    inlines = [BbInline]

class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(Bb, BbAdmin)
#admin.site.register(Rubric)
admin.site.register(Img)
admin.site.register(Rubric, RubricAdmin)
