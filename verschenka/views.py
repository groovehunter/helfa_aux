from django.shortcuts import render


from django.views import generic
from .models import Item, Category
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import FormView, UpdateView
from djflow.ViewController import ViewControllerSupport, DjMixin
from djflow.Controller import Controller
from .tables import ItemTable
from .forms import ItemForm
from django.shortcuts import render


import logging
lg = logging.getLogger('root')

class ItemUpdateView(UpdateView, DjMixin):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = '/verschenka/item/detail'
    pk_url_kwargs = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

class ItemCreateView(CreateView, DjMixin):
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = '/verschenka/item/detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context
"""
    def get(self):
      #if request.method == 'GET':
      # display UserForm
      pass

    def post(self):
      #request.method == 'POST':
      # process form submission
      pass
"""



class MyFormView(FormView, DjMixin): #, ViewControllerSupport):
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = '/verschenka/item/detail'
    pk_url_kwargs = 'slug'

    def get_object(self, **kwargs):
        lg.debug('get_object', kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
        return obj

    def post(self, request, *args, **kwargs):
        lg.debug('ICV post')
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.check_user()
        self.yaml_load()
        menudata = self.yamlmenu()
        menu = {'menudata': menudata}
        context.update(menu)
        context.update(c)
        return context

    def get_form_kwargs(self):
        kwargs = super(MyFormView, self).get_form_kwargs()
        return kwargs







class ItemListView(ListView, DjMixin): #ViewControllerSupport):
    model = Item
    #template_name = 'items/item_list.html'
    template_name = 'items/items_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.access_denied()
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        context = {}
        context['cat_defined'] = False
        #table = ItemTable(self.object_list) #, template_name="generic/table.html" )
        #context['table'] = table
        context.update(self.get_context_data())
        return self.render_to_response(context)

from django.http import Http404

class ItemDetailView(DetailView, DjMixin): #ViewControllerSupport):
    model = Item
    template_name = 'items/item_detail.html'
    pk_url_kwargs = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = None
        if pk is not None:
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
        if not obj:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return self.access_denied()
        context = {'object': self.get_object() }
        #context = {}
        context.update(self.get_context_data())
        lg.debug(context)
        return self.render_to_response(context)



class CategoryListView(ListView, ViewControllerSupport):
    model = Category
    template_name = "items/category_list.html"

    def get_context_data(self, **kwargs):
        self.fields_noshow = []
        context = super().get_context_data(**kwargs)
        lg.debug(context)
        c = self.listview_helper()
        context.update(self.get_user_context())
        context.update(c)
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
