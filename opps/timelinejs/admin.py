from django.contrib.admin import site, ModelAdmin, StackedInline, TabularInline
from .models import Timeline, TimelineEvent, TimelineOptions, TimelinePost


class CommonMedia:
    js = (
        #'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
        #'admin/js/editor.js',
        'admin/js/inlinecollapsed.js',
    )
    css = {
        'all': ('admin/css/editor.css',),
    }


class OptionsInline(StackedInline):
    model = TimelineOptions


class EventsInline(StackedInline):
    model = TimelineEvent


class TimelinePostInline(TabularInline):
    model = TimelinePost
    fk_name = 'timeline'
    raw_id_fields = ['post']
    actions = None
    extra = 1


class TimelineAdmin(ModelAdmin):
    fieldsets = (
        (None, {'fields': (('headline', 'start_date'), 'text')}),
        ('Assets', {
            'classes': ('collapse',),
            'fields': ('asset_media', 'asset_credit', 'asset_caption')
        }),
        ('Source', {
            'classes': ('collapse',),
            'fields': ('source', 'json')
        })
    )
    inlines = [TimelinePostInline, OptionsInline, EventsInline]
    # Media = CommonMedia


class TimelineEventAdmin(ModelAdmin):
    raw_id_fields = ('timeline',)


class TimelineOptionsAdmin(ModelAdmin):
    raw_id_fields = ('timeline',)

site.register(Timeline, TimelineAdmin)
site.register(TimelineEvent, TimelineEventAdmin)
site.register(TimelineOptions, TimelineOptionsAdmin)
