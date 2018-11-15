"""
Clickmap template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node

from analytical.utils import is_internal_ip, disable_html, get_required_setting, validate_no_args, \
    BaseAlphanumericAnalyticalNode


CLICKMAP_TRACKER_ID_RE = re.compile(r'^\w+$')
TRACKING_CODE = """
    <script type="text/javascript">
    var clickmapConfig = {tracker: '%(CLICKMAP_TRACKER_ID)s', version:'2'};
    window.clickmapAsyncInit = function(){ __clickmap.init(clickmapConfig); };
    (function() { var _cmf = document.createElement('script'); _cmf.async = true;
    _cmf.src = document.location.protocol + '//www.clickmap.ch/tracker.js?t=';
    _cmf.src += clickmapConfig.tracker; _cmf.id += 'clickmap_tracker';
    _cmf.src += '&v='+clickmapConfig.version+'&now='+(new Date().getTime());
    if (document.getElementById('clickmap_tracker')==null) {
    document.getElementsByTagName('head')[0].appendChild(_cmf); }}());
    </script>
"""

register = Library()


@register.tag
def clickmap(parser, token):
    """
    Clickmap tracker template tag.

    Renders Javascript code to track page visits.  You must supply
    your clickmap tracker ID (as a string) in the ``CLICKMAP_TRACKER_ID``
    setting.
    """
    validate_no_args(token)
    return ClickmapNode()

class ClickmapNode(BaseAlphanumericAnalyticalNode):

    setting_prefix = 'CLICKMAP'
    setting_name = 'CLICKMAP_TRACKER_ID'
    code_template = TRACKING_CODE
    code_service_label ='Clickmap'


def contribute_to_analytical(add_node):
    ClickmapNode()  # ensure properly configured
    add_node('body_bottom', ClickmapNode)
