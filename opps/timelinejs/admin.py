from django.contrib.admin import site, ModelAdmin, StackedInline, TabularInline
from django.utils.translation import ugettext_lazy as _
from .models import Timeline, TimelineEvent, TimelineOptions, TimelinePost
from opps.core.admin import apply_opps_rules


class CommonMedia:
    pass
    # js = (
    #     #'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    #     #'admin/js/editor.js',
    #     'admin/js/inlinecollapsed.js',
    # )
    # css = {
    #     'all': ('admin/css/editor.css',),
    # }



class OptionsInline(StackedInline):
    model = TimelineOptions
    extra = 1
    verbose_name = _("Option")
    verbose_name_plural = _("Options")

class EventsInline(StackedInline):
    model = TimelineEvent
    extra = 1
    max_num = None
    verbose_name = _("Event")
    verbose_name_plural = _("Events")


class TimelinePostInline(TabularInline):
    model = TimelinePost
    fk_name = 'timeline'
    raw_id_fields = ['post']
    actions = None
    extra = 1


@apply_opps_rules('timelinejs')
class TimelineAdmin(ModelAdmin):
    fieldsets = (
        (None, {'fields': (('headline', 'start_date'), 'text')}),
        ('Assets', {
            'classes': ('collapse',),
            'fields': ('asset_media', 'asset_credit', 'asset_caption')
        }),
        ('Source', {
            'classes': ('collapse',),
            'fields': ('source',)
        })
    )
    inlines = [TimelinePostInline, OptionsInline, EventsInline]
    # Media = CommonMedia


@apply_opps_rules('timelinejs')
class TimelineEventAdmin(ModelAdmin):
    raw_id_fields = ('timeline',)


@apply_opps_rules('timelinejs')
class TimelineOptionsAdmin(ModelAdmin):
    raw_id_fields = ('timeline',)

site.register(Timeline, TimelineAdmin)
site.register(TimelineEvent, TimelineEventAdmin)
site.register(TimelineOptions, TimelineOptionsAdmin)
