from django.shortcuts import render


from django.views.generic import ListView, DetailView, CreateView
from helfa_aux_dev.ViewController import ViewControllerSupport
from .models import Item
from .tables import ItemTable

import logging
lg = logging.getLogger('root')

class ItemListView(ListView, ViewControllerSupport):
    model = Item

    def get_context_data(self, **kwargs):
        self.init_ctrl()
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(c)
        #lg.debug(context)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.access_denied()
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        self.init_ctrl()
        table = ItemTable(self.object_list) #, template_name="generic/table.html" )
        self.context['table'] = table
        self.template_name = 'generic/page_djtable.html'
        #self.template_name = 'verschenka/index.html'
        lg.debug(self.template_name)

        self.context.update(self.get_context_data())
        return self.render()


