from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.inclusion_tag('timeline_template.html', takes_context=True)
def timeline(context, src=None, **config):
    if src is None:
        instance = context['timeline']
        src = instance.source or instance.json or instance.pk
    if isinstance(src, (int, long)):
        config['src'] = '%s?format=json' % reverse('timelinejs:timelineview', kwargs={'pk': int(src)})
    else:
        try:
            # `src` might be a string that can be coerced into a long
            config['src'] = '%s?format=json' % reverse('timelinejs:timelineview', kwargs={'pk': long(src)})
        except ValueError:
            config['src'] = src
    # if context.has_key('options'):
    if 'options' in context:
        options = context['options']
        options.__dict__.update(config)
    else:
        options = config

    return {'context': context, 'config': options, 'src': config['src']}
