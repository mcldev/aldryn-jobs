

from os.path import splitext

from cms.plugin_rendering import ContentRenderer
from aldryn_search.utils import strip_tags

from django.utils.encoding import force_text
from django.utils.text import smart_split
from django.db import models
from django.urls import reverse, NoReverseMatch
from django.utils.text import get_valid_filename as get_valid_filename_django
from django.template.defaultfilters import slugify
from django.conf import settings

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser


def get_valid_filename(s):
    """
    like the regular get_valid_filename, but also slugifies away umlauts and
    stuff. Copied from django-filer
    """
    s = get_valid_filename_django(s)
    filename, ext = splitext(s)
    filename = slugify(filename)
    ext = slugify(ext)
    if ext:
        return "%s.%s" % (filename, ext)
    else:
        return "%s" % (filename,)


def namespace_is_apphooked(namespace):
    # avoid circular import
    from .urls import DEFAULT_VIEW
    """
    Check if provided namespace has an app-hooked page.
    Returns True or False.
    """
    try:
        reverse('{0}:{1}'.format(namespace, DEFAULT_VIEW))
    except NoReverseMatch:
        return False
    return True


def SALUTATION_CHOICES():
    SALUTATIONS = getattr(settings, "ALDRYN_JOBS_SALUTATIONS", None)
    if SALUTATIONS:
        return SALUTATIONS

    return ((None,'---'),
            ('Mr','Mr'),
            ('Ms','Ms'),
            ('Mrs','Mrs'),
            ('Miss','Miss'),
            ('Dr','Dr'),
            ('Prof','Prof'),
            ('Rev','Rev'),
            ('Lady','Lady'),
            ('Sir','Sir'),
            )


def get_request(language=None):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    request_factory = RequestFactory()
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    request.current_page = None
    request.user = AnonymousUser()
    return request


def render_plugin(request, plugin_instance):
    renderer = ContentRenderer(request)
    context = {'request': request}
    return renderer.render_plugin(plugin_instance, context)


def get_cleaned_bits(data):
    decoded = force_text(data)
    stripped = strip_tags(decoded)
    return smart_split(stripped)


def get_field_value(obj, name):
    """
    Given a model instance and a field name (or attribute),
    returns the value of the field or an empty string.
    """
    fields = name.split('__')

    name = fields[0]

    try:
        obj._meta.get_field(name)
    except (AttributeError, models.FieldDoesNotExist):
        # we catch attribute error because obj will not always be a model
        # specially when going through multiple relationships.
        value = getattr(obj, name, None) or ''
    else:
        value = getattr(obj, name)

    if len(fields) > 1:
        remaining = '__'.join(fields[1:])
        return get_field_value(value, remaining)
    return value


def get_plugin_index_data(base_plugin, request):
    text_bits = []

    plugin_instance, plugin_type = base_plugin.get_plugin_instance()

    if plugin_instance is None:
        # this is an empty plugin
        return text_bits

    search_fields = getattr(plugin_instance, 'search_fields', [])

    if hasattr(plugin_instance, 'search_fulltext'):
        # check if the plugin instance has search enabled
        search_contents = plugin_instance.search_fulltext
    elif hasattr(base_plugin, 'search_fulltext'):
        # now check in the base plugin instance (CMSPlugin)
        search_contents = base_plugin.search_fulltext
    elif hasattr(plugin_type, 'search_fulltext'):
        # last check in the plugin class (CMSPluginBase)
        search_contents = plugin_type.search_fulltext
    else:
        # disabled if there's search fields defined,
        # otherwise it's enabled.
        search_contents = not bool(search_fields)

    if search_contents:
        plugin_contents = render_plugin(request, plugin_instance)
        if plugin_contents:
            text_bits = get_cleaned_bits(plugin_contents)
    else:
        values = (get_field_value(plugin_instance, field) for field in search_fields)

        for value in values:
            cleaned_bits = get_cleaned_bits(value or '')
            text_bits.extend(cleaned_bits)
    return text_bits
