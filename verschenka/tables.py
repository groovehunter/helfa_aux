from djflow.FlowBaseTable import FlowBaseTable
from .models import Item
import django_tables2 as tables



class ItemTable(FlowBaseTable):
    name = tables.Column(linkify=True)
    #link = tables.Column()
    class Meta:
        model = Item
        exclude = ['id']


## methode eines tables gewesen??
def render_labelterm(self, value):
    return format_html('<a class="text-blue-700 underline" href="/video/topic/%s">%s</a>' %(value,value))
