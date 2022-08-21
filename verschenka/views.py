from django.shortcuts import render


from django.views import generic
from .models import Item, Category
from django.views.generic import ListView, DetailView, CreateView
from helfa_aux_dev.ViewController import ViewControllerSupport
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



class ItemDetailView(DetailView, ViewControllerSupport):
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
        self.init_ctrl()
        self.object = self.get_queryset()
        self.template_name = 'items/item_detail.html'

        self.context.update(self.get_context_data())
        return self.render()




class CategoryListView(ListView, ViewControllerSupport):
    model = Category


class CategoryListView(ListView):
    model = Category
    template_name = "items/category_list.html"

class ItemsByCategoryView(ListView):
    ordering = 'id'
    paginate_by = 10
    template_name = 'items/items_by_category.html'

    def get_queryset(self):
        # https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-display/#dynamic-filtering
        # the following category will also be added to the context data
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Item.objects.filter(category=self.category)
         # need to set ordering to get consistent pagination results
        queryset = queryset.order_by(self.ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


