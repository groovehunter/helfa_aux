from django.shortcuts import render


from django.views import generic
from .models import Item, Category
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from helfa_aux_dev.ViewController import ViewControllerSupport
from helfa_aux_dev.Controller import Controller
from .tables import ItemTable

import logging
lg = logging.getLogger('root')

class SomeView(TemplateView):
  template_name = 'about.html'


class VerschenkaController(Controller):
  def __init__(self, request):
    Controller.__init__(request)

  def itemlist(self):
    pass

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
    template_name = "items/category_list.html"

    def get_context_data(self, **kwargs):
        self.fields_noshow = []
        context = super().get_context_data(**kwargs)
        c = self.listview_helper()
        context.update(self.get_user_context())
        context.update(c)
        lg.debug(context)
        return context


class ItemsByCategoryView(ListView, ViewControllerSupport):
    ordering = 'id'
    paginate_by = 10
    template_name = 'items/items_by_category.html'

    def obj_cattree(self):
      self.cat_objlist = Category.objects.all()
      c = {'cat_obj_list' : self.cat_objlist}
      return c

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        #c = self.listview_helper()
        context.update(self.get_user_context())
        #context.update(c)
        context.update(self.obj_cattree())
        return context

    def get_queryset(self):
        self.init_ctrl()
        if not self.request.user.is_authenticated:
            return self.access_denied()
        # the following category will also be added to the context data
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Item.objects.filter(category=self.category)
         # need to set ordering to get consistent pagination results
        queryset = queryset.order_by(self.ordering)
        return queryset
