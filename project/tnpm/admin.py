from django.contrib import admin
from django.utils.html import format_html

from tnpm.models.admin import *


class Review(admin.TabularInline):
    model = TnpmElementFilter


@admin.register(TnpmTrapLookupRules)
class LookupNameAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", "is_enabled", "description", "show_sub_list")
    save_on_top = True
    save_as = True
    list_editable = ("is_enabled",)
    change_form_template = 'admin/button_preview.html'
    fieldsets = (
        ('Advanced options', {

            'fields': ('name', 'profile', 'description', 'is_enabled')
        }),
        ('Формирование lookup', {
            'fields': (
                'metric_name', 'lookup_type')
        }),

    )
    inlines = [Review]

    def show_sub_list(self, obj):
        return format_html(f"<a href=/preview/{obj.id} target='_blank'>Предпросмотр</a>", url=obj.name)

    #
    show_sub_list.short_description = "Список сабэлементов"


admin.site.register(ProbeManager)


@admin.register(TnpmProbeManager)
class AdminTnpmProbeManager(admin.ModelAdmin):
    list_display = ("manager",)
