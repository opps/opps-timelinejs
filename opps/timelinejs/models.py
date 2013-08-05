# coding: utf-8

from jsonfield import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings


app_namespace = getattr(settings, 'OPPS_TIMEINEJS_URL_NAMESPACE', 'timelinejs')


class Timeline(models.Model):
    headline = models.CharField(
        max_length=200,
        help_text=_(u'Headline for timeline'),
        verbose_name=_(u'Headline'),
    )
    type = models.CharField(
        max_length=50,
        default="default",
        verbose_name=_(u'type'),
    )
    # start_date = models.DateField(
    #     blank=True,
    #     verbose_name=_(u'Start Date'),
    #     help_text=_(u'Timeline start date'),
    # )
    start_date = models.CharField(
        _(u'Start Date'),
        help_text=_(u"""
            Event end date:<br />
            If you enter 2000 in the date column, it will read as 2000.<br>
            01/2000 will read as January, 2000 and <br>
            12/31/2000 will read as December 31st, 2000.
        """),
        max_length=10 # 01/01/2000
    )
    text = models.TextField(
        blank=True,
        verbose_name=_(u'Text'),
        help_text=_(u'Description of timeline'),
    )
    asset_media = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('media'),
        help_text=_(u'Media to add to even info: Picutre link, YouTube, Wikipedia, etc.')
    )
    asset_credit = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('credit'),
        help_text=_(u'Media credits here')
    )
    asset_caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('caption'),
        help_text=_(u'Caption for media')
    )

    json = JSONField(
        _(u"Timeline Json"),
        blank=True,
        null=True,
        help_text=_(
            u'Optional JSON for timelinejs if not provided'
            u' you should add items or google spreadsheet'
        )
    )
    source = models.URLField(
        _(u"Source URL"),
        blank=True,
        null=True,
        help_text=_(
            u'Optional Google Spreadsheet or json URL for timelinejs '
            u' if not provided you should add items or json'
        )
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    posts = models.ManyToManyField(
        'articles.Post',
        null=True,
        blank=True,
        related_name='timeline_post',
        through='TimelinePost'
    )

    def to_dict(self):
        d = {}
        d['startDate'] = self.start_date
        d['type'] = self.type
        d['headline'] = self.headline
        d['text'] = self.text
        d['asset'] = {'media': self.asset_media,
                      'credit': self.asset_credit,
                      'caption': self.asset_caption}
        events = []
        for e in self.timelineevent_set.all():
            events.append(dict([(attr, getattr(e, attr)) for attr in [f.name for f in e._meta.fields]]))
        if self.timelineevent_set.filter(type='date').exists():
            d['date'] = [e.to_dict() for e in self.timelineevent_set.filter(type='date')]
        if self.timelineevent_set.filter(type='era').exists():
            d['era'] = [e.to_dict() for e in self.timelineevent_set.filter(type='era')]
        if self.timelineevent_set.filter(type='title').exists():
            d['title'] = [e.to_dict() for e in self.timelineevent_set.filter(type='title')]
        if self.timelineevent_set.filter(type='chart').exists():
            d['chart'] = [e.to_dict() for e in self.timelineevent_set.filter(type='chart')]
        timeline = {'timeline': d}
        return timeline

    def __str__(self):
        return "%s - %s" % (self.start_date, self.headline)

    class Meta:
        verbose_name = _(u'Timeline')
        verbose_name_plural = _(u'Timelines')

    def get_absolute_url(self):
        return reverse(
            '{0}:timelineview'.format(app_namespace),
            kwargs={'pk': self.pk}
        )

    def get_thumb(self):
        return self.asset_media

    @property
    def search_category(self):
        return _("Timeline")


class TimelinePost(models.Model):
    post = models.ForeignKey(
        'articles.Post',
        verbose_name=_(u'Timeline Post'),
        null=True,
        blank=True,
        related_name='timelinepost_post',
        on_delete=models.SET_NULL
    )
    timeline = models.ForeignKey(
        'timelinejs.Timeline',
        verbose_name=_(u'Timeline'),
        null=True,
        blank=True,
        related_name='timelinepost_timeline',
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.timeline.slug, self.post.slug)


    class Meta:
        verbose_name = _(u'Timeline Post')
        verbose_name_plural = _(u'Timeline Posts')


class TimelineEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    # start_date = models.DateField(verbose_name=_(u'Start Date'),
    #                               help_text=_('Event start date'))
    # end_date = models.DateField(
    #     blank=True,
    #     null=True,
    #     help_text=_(u'Event end date'),
    #     verbose_name=_(u'End Date'),
    # )
    start_date = models.CharField(
        _(u'Start Date'),
        help_text=_(u"""
            Event end date:<br />
            If you enter 2000 in the date column, it will read as 2000.<br>
            01/2000 will read as January, 2000 and <br>
            12/31/2000 will read as December 31st, 2000.
        """),
        max_length=10 # 01/01/2000
    )
    end_date = models.CharField(
        _(u'End Date'),
        help_text=_(u'Event end date'),
        blank=True,
        null=True,
        max_length=10 # 01/01/2000
    )
    headline = models.CharField(
        max_length=200,
        blank=True,
        help_text=_(u'Headline for event'),
        verbose_name=_(u'Headline'),
    )
    text = models.TextField(
        blank=True,
        help_text=_(u'Text description of event'),
        verbose_name=_(u'Text'),
    )
    asset_media = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('media'),
        help_text=_(u'Media to add to even info: Picture link, YouTube, '
                    u'Wikipedia, etc.')
    )
    asset_credit = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('credit'),
        help_text=_(u'Media credits here')
    )
    asset_caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_(u'caption'),
        help_text=_(u'Caption for media')
    )
    asset_thumbnail = models.CharField(
        _(u"Media thumbnail"),
        max_length=500,
        blank=True,
        null=True,
        help_text=_(u'Optional 32x32 thumbnail')
    )

    type = models.CharField(
        _(u"Item type"),
        max_length=255,
        blank=True,
        null=True,
        default='date',
        help_text=_(
            u'Use "date",  "era", "title" or "chart"'
            u' Note: Only one can be "title"'
            u' and "era" displays only headline and dates'
        )
    )

    classname = models.CharField(
        _(u"Classname"),
        max_length=255,
        null=True,
        blank=True
    )

    value = models.CharField(
        _(u"Chart Value"),
        max_length=140,
        null=True,
        blank=True,
        help_text=_(u'This is only used for "chart" type')
    )

    tag = models.CharField(
        _(u"Tag"),
        max_length=140,
        null=True,
        blank=True
    )

    def to_dict(self):
        d = {}
        d['startDate'] = self.start_date
        d['endDate'] = self.end_date or d['startDate']
        d['headline'] = self.headline
        d['tag'] = self.tag

        if self.type == 'chart':
            d['value'] = self.value

        d['classname'] = self.classname
        d['text'] = self.text
        d['asset'] = {'media': self.asset_media,
                      'credit': self.asset_credit,
                      'thumbnail': self.asset_thumbnail,
                      'caption': self.asset_caption}
        return d

    def __str__(self):
        return "%s - %s %s" % (self.start_date, self.end_date, self.headline)

    class Meta:
        verbose_name = _(u'Timeline Event')
        verbose_name_plural = _(u'Timeline Events')


class TimelineOptions(models.Model):
    FONT_CHOICES = (
        ('Arvo-PTSans', 'Arvo-PTSans'),
        ('Merriweather-NewsCycle', 'Merriweather-NewsCycle'),
        ('PoiretOne-Molengo', 'PoiretOne-Molengo'),
        ('PTSerif-PTSans', 'PTSerif-PTSans'),
        ('DroidSerif-DroidSans', 'DroidSerif-DroidSans'),
        ('Lekton-Molengo', 'Lekton-Molengo'),
        ('NixieOne-Ledger', 'NixieOne-Ledger'),
        ('AbrilFatface-Average', 'AbrilFatface-Average'),
        ('PlayfairDisplay-Muli', 'PlayfairDisplay-Muli'),
        ('Rancho-Gudea', 'Rancho-Gudea'),
        ('Bevan-PotanoSans', 'Bevan-PotanoSans'),
        ('BreeSerif-OpenSans', 'BreeSerif-OpenSans'),
        ('SansitaOne-Kameron', 'SansitaOne-Kameron'),
        ('Pacifico-Arimo', 'Pacifico-Arimo')
    )
    LANG_CHOICES = (
        ('en', u'English'),
        ('fr', u'Français'),
        ('es', u'Español'),
        ('de', u'Deutsch'),
        ('it', u'Italiano'),
        ('pt-br', u'Português Brazil'),
        ('pt', u'Português'),
        ('nl', u'Dutch'),
        ('cz', u'Czech'),
        ('no', u'Norwegian'),
        ('dk', u'Danish'),
        ('id', u'Indonesian'),
        ('pl', u'Polish'),
        ('sl', u'Slovenian'),
        ('ru', u'Russian'),
        ('sk', u'Slovak'),
        ('is', u'Icelandic'),
        ('fo', u'Faroese'),
        ('kr', u'월요일'),
        ('ja', u'日本語'),
        ('zh-ch', u'中文'),
        ('zh-tw', u'Taiwanese Mandarin'),
        ('ta', u'தமிழ் - Tamil'),
        ('ar', u'Arabic')
    )
    MAP_CHOICES = (
        ('Stamen Maps', 'Stamen Maps'),
        ('toner', 'toner'),
        ('toner-lines', 'toner-lines'),
        ('toner-labels', 'toner-labels'),
        ('watercolor', 'watercolor'),
        ('sterrain', 'sterrain'),
        ('Google Maps', 'Google Maps'),
        ('ROADMAP', 'ROADMAP'),
        ('TERRAIN', 'TERRAIN'),
        ('HYBRID', 'HYBRID'),
        ('SATELLITE', 'SATELLITE')
    )
    timeline = models.OneToOneField(Timeline, primary_key=True)
    width = models.CharField(
        max_length=10,
        default='100%',
        help_text=_(u'Width of timeline DIV'),
        verbose_name=_(u'Width'),
    )
    height = models.CharField(
        max_length=10,
        default='600',
        help_text=_(u'Height of timeline DIV'),
        verbose_name=_(u'Height')
    )
    embed_id = models.CharField(
        max_length=20,
        blank=True,
        help_text=_(u'ID of timeline DIV'),
        verbose_name=_(u'Embed ID')
    )
    start_at_end = models.BooleanField(
        default=False,
        verbose_name=_(u'Start at end'),
        help_text=_(u'Set to true to start the timeline on the last date.'
                    u' default is false')
    )
    start_at_slide = models.IntegerField(
        default=0,
        verbose_name=_(u'Start at slide'),
        help_text=_(u'You can tell TimelineJS to start at a specific slide'
                    u' number default is 0')
    )
    start_zoom_adjust = models.IntegerField(
        default=0,
        verbose_name=_(u'Start zoom adjust'),
        help_text=_(u'This will tweak the default zoom level. Equivalent'
                    u' to pressing the zoom in or zoom out button the '
                    u'specified number of times. Negative numbers zoom out. '
                    u'default is 0')
    )
    hash_bookmark = models.BooleanField(
        default=False,
        verbose_name=_(u'Hash bookmark'),
        help_text=_(u'set to true to allow bookmarking slides using the hash '
                    u'tag default is false')
    )
    font = models.CharField(
        max_length=50,
        choices=FONT_CHOICES,
        default='Bevan-PotanoSans',
        verbose_name=_(u'Font'),
        help_text=_(u'Font combination options')
    )
    debug = models.BooleanField(
        default=False,
        verbose_name=_(u'Debug'),
        help_text=_(u'Will log events etc to the console. default is false')
    )
    lang = models.CharField(
        max_length=6,
        choices=LANG_CHOICES,
        default='en',
        verbose_name=_(u'Language'),
        help_text=_(u'Localization options. default is English')
    )
    maptype = models.CharField(
        max_length=50,
        choices=MAP_CHOICES,
        default='watercolor',
        verbose_name=_(u'Map Type'),
        help_text=_(u'google maps api needed [todo]')
    )

    class Meta:
        verbose_name = _(u'Timeline Option')
        verbose_name_plural = _(u'Timeline Options')

#'''JSON Format
#{
#    "timeline":
#    {
#        "headline":"The Main Timeline Headline Goes here",
#        "type":"default",
#        "startDate":"1888",
#        "text":"<p>Intro body text goes here, some HTML is ok</p>",
#        "asset":
#        {
#            "media":"http://yourdomain_or_socialmedialink_goes_here.jpg",
#            "credit":"Credit Name Goes Here",
#            "caption":"Caption text goes here"
#        },
#        "date": [
#            {
#                "startDate":"2011,12,10",
#                "endDate":"2011,12,11",
#                "headline":"Headline Goes Here",
#                "text":"<p>Body text goes here, some HTML is OK</p>",
#                "asset":
#                {
#                    "media":"http://twitter.com/ArjunaSoriano/status/164181156147900416",
#                    "credit":"Credit Name Goes Here",
#                    "caption":"Caption text goes here"
#                }
#            }
#        ]
#    }
#}
#'''
