"""
FIXME: Once the the pt-br translations for the django contrib humanize app is fixed, remove this code.
"""

from django.utils.translation import gettext_lazy, ngettext_lazy, npgettext_lazy


class NaturalTimeFormatter:
    time_strings = {
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        "past-day": gettext_lazy("%(delta)s ago"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "past-hour": ngettext_lazy("an hour ago", "%(count)s hours ago", "count"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "past-minute": ngettext_lazy("a minute ago", "%(count)s minutes ago", "count"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "past-second": ngettext_lazy("a second ago", "%(count)s seconds ago", "count"),
        "now": gettext_lazy("now"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "future-second": ngettext_lazy("a second from now", "%(count)s seconds from now", "count"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "future-minute": ngettext_lazy("a minute from now", "%(count)s minutes from now", "count"),
        # Translators: please keep a non-breaking space (U+00A0) between count
        # and time unit.
        "future-hour": ngettext_lazy("an hour from now", "%(count)s hours from now", "count"),
        # Translators: delta will contain a string like '2 months' or '1 month, 2 weeks'
        "future-day": gettext_lazy("%(delta)s from now"),
    }
    past_substrings = {
        # Translators: 'naturaltime-past' strings will be included in '%(delta)s ago'
        "year": npgettext_lazy("naturaltime-past", "%d year", "%d years"),
        "month": npgettext_lazy("naturaltime-past", "%d month", "%d months"),
        "week": npgettext_lazy("naturaltime-past", "%d week", "%d weeks"),
        "day": npgettext_lazy("naturaltime-past", "%d day", "%d days"),
        "hour": npgettext_lazy("naturaltime-past", "%d hour", "%d hours"),
        "minute": npgettext_lazy("naturaltime-past", "%d minute", "%d minutes"),
    }
    future_substrings = {
        # Translators: 'naturaltime-future' strings will be included in '%(delta)s from now'
        "year": npgettext_lazy("naturaltime-future", "%d year", "%d years"),
        "month": npgettext_lazy("naturaltime-future", "%d month", "%d months"),
        "week": npgettext_lazy("naturaltime-future", "%d week", "%d weeks"),
        "day": npgettext_lazy("naturaltime-future", "%d day", "%d days"),
        "hour": npgettext_lazy("naturaltime-future", "%d hour", "%d hours"),
        "minute": npgettext_lazy("naturaltime-future", "%d minute", "%d minutes"),
    }
