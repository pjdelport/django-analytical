"""
Hotjar template tags and filters.
"""
from __future__ import absolute_import

import re

from django.template import Library, Node

from analytical.utils import validate_no_args, BaseAnalyticalNode, BaseNumericAnalyticalNode


HOTJAR_TRACKING_CODE = """\
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:%(HOTJAR_SITE_ID)s,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""


register = Library()


@register.tag
def hotjar(parser, token):
    """
    Hotjar template tag.
    """
    validate_no_args(token)
    return HotjarNode()


class HotjarNode(BaseNumericAnalyticalNode):

    setting_prefix = 'HOTJAR'
    setting_name = 'HOTJAR_SITE_ID'
    code_template = HOTJAR_TRACKING_CODE
    code_service_label = 'Hotjar'


def contribute_to_analytical(add_node):
    # ensure properly configured
    HotjarNode()
    add_node('head_bottom', HotjarNode)
