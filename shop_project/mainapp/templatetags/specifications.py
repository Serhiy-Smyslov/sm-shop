from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone

register = template.Library()

TABLE_HEAD = """
            <table class="table">
                <tbody>
        """

TABLE_TAIL = """
                </tbody>
            </table>
        """

TABLE_CONTENT = """
            <tr>
                <td>{name}</td>
                <td>{value}</td>
            </tr>
        """

PRODUCT_SPEC = {
    'laptop': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'processor_freq': 'processor_freq',
        'RAM': 'ram',
        'Video cart': 'video',
        'Acum': 'time_without_charge',
    },
    'smartphone': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'RAM': 'ram',
        'Resolution': 'resolution',
        'Acum': 'accum_volume',
        'SD': 'sd',
        'SD volume': 'sd_volume_max',
        'Main camera': 'main_cam_mp',
        'Frontal camera': 'frontal_cam_mp',
    },
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('SD volume')
        else:
            PRODUCT_SPEC['smartphone']['SD volume'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
