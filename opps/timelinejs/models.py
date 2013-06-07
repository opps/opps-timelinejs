# coding: utf-8

from jsonfield import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Timeline(models.Model):
    headline = models.CharField(
        max_length=200,
        help_text=_(u'Headline for timeline')
    )
    type = models.CharField(
        max_length=50,
        default="default"
    )
    start_date = models.DateField(
        blank=True,
        help_text=_(u'Timeline start date')
    )
    text = models.TextField(
        blank=True,
        help_text=_(u'Description of timeline')
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
        d['startDate'] = self.start_date.strftime('%Y,%m,%d')
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


class TimelineEvent(models.Model):
    timeline = models.ForeignKey(Timeline)
    start_date = models.DateField(help_text='Event start date')
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text=_(u'Event end date')
    )
    headline = models.CharField(
        max_length=200,
        blank=True,
        help_text=_(u'Headline for event')
    )
    text = models.TextField(
        blank=True,
        help_text=_(u'Text description of event')
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
        d['startDate'] = self.start_date.strftime('%Y,%m,%d')
        d['endDate'] = self.end_date.strftime('%Y,%m,%d') if self.end_date else d['startDate']
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
        help_text=_(u'Width of timeline DIV')
    )
    height = models.CharField(
        max_length=10,
        default='600',
        help_text=_(u'Height of timeline DIV')
    )
    embed_id = models.CharField(
        max_length=20,
        blank=True,
        help_text=_(u'ID of timeline DIV')
    )
    start_at_end = models.BooleanField(
        default=False,
        help_text=_(u'Set to true to start the timeline on the last date.'
                    u' default is false')
    )
    start_at_slide = models.IntegerField(
        default=0,
        help_text=_(u'You can tell TimelineJS to start at a specific slide'
                    u' number default is 0')
    )
    start_zoom_adjust = models.IntegerField(
        default=0,
        help_text=_(u'This will tweak the default zoom level. Equivalent'
                    u' to pressing the zoom in or zoom out button the '
                    u'specified number of times. Negative numbers zoom out. '
                    u'default is 0')
    )
    hash_bookmark = models.BooleanField(
        default=False,
        help_text=_(u'set to true to allow bookmarking slides using the hash '
                    u'tag default is false')
    )
    font = models.CharField(
        max_length=50,
        choices=FONT_CHOICES,
        default='Bevan-PotanoSans',
        help_text=_(u'Font combination options')
    )
    debug = models.BooleanField(
        default=False,
        help_text=_(u'Will log events etc to the console. default is false')
    )
    lang = models.CharField(
        max_length=6,
        choices=LANG_CHOICES,
        default='en',
        help_text=_(u'Localization options. default is English')
    )
    maptype = models.CharField(
        max_length=50,
        choices=MAP_CHOICES,
        default='watercolor',
        help_text=_(u'google maps api needed [todo]')
    )

    class Meta:
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