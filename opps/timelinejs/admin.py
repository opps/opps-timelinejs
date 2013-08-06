from django.contrib.admin import site, ModelAdmin, StackedInline, TabularInline
from django.utils.translation import ugettext_lazy as _
from .models import Timeline, TimelineEvent, TimelineOptions, TimelinePost
from opps.core.admin import apply_opps_rules
from opps.images.generate import image_url


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

class HasImageThumb(object):
    def image_thumb(self, obj):
        if obj.asset_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                image_url(obj.asset_image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True


class OptionsInline(StackedInline):
    model = TimelineOptions
    extra = 1
    verbose_name = _("Option")
    verbose_name_plural = _("Options")

class EventsInline(HasImageThumb, StackedInline):
    model = TimelineEvent
    extra = 1
    max_num = None
    verbose_name = _("Event")
    verbose_name_plural = _("Events")
    raw_id_fields = ('asset_image',)
    readonly_fields = ['image_thumb']

    fieldsets = (
        (None, {
            'fields': ['start_date', 'end_date', 'headline', 'text',
            'asset_media', 'asset_image', 'image_thumb', 'asset_credit',
            'asset_caption', 'asset_thumbnail', 'classname']
        }),
    )


class TimelinePostInline(TabularInline):
    model = TimelinePost
    fk_name = 'timeline'
    raw_id_fields = ['post']
    actions = None
    extra = 1


@apply_opps_rules('timelinejs')
class TimelineAdmin(HasImageThumb, ModelAdmin):
    fieldsets = (
        (None, {'fields': (('headline', 'start_date'), 'text')}),
        ('Assets', {
            'classes': ('collapse',),
            'fields': ('asset_media', 'asset_image', 'image_thumb',
                       'asset_credit', 'asset_caption')
        }),
        ('Source', {
            'classes': ('collapse',),
            'fields': ('source',)
        })
    )
    raw_id_fields = ('asset_image',)
    inlines = [TimelinePostInline, OptionsInline, EventsInline]
    readonly_fields = ['image_thumb']
    # Media = CommonMedia


@apply_opps_rules('timelinejs')
class TimelineEventAdmin(HasImageThumb, ModelAdmin):
    raw_id_fields = ('timeline', 'asset_image')
    readonly_fields = ['image_thumb']


@apply_opps_rules('timelinejs')
class TimelineOptionsAdmin(ModelAdmin):
    raw_id_fields = ('timeline',)

site.register(Timeline, TimelineAdmin)
site.register(TimelineEvent, TimelineEventAdmin)
site.register(TimelineOptions, TimelineOptionsAdmin)
