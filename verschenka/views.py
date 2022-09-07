from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.conf import settings
from .models import Item, Category
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import FormView, UpdateView
from djflow.ViewController import ViewControllerSupport, DjMixin
from djflow.Controller import Controller
from .tables import ItemTable
from .forms import ItemForm
from django.shortcuts import render
from helfa_aux_dev_bot.bot import bot

import logging
import os
import urllib3
lg = logging.getLogger('root')
#lg = logging.getLogger(__name__)

chat_id = '-1001763189703'
def tg_post(item):
  msg = 'post item'
  result = bot.sendMessage(chat_id, msg)
  lg.debug(result)

from requests_toolbelt import MultipartEncoder
import requests


#r = requests.post('http://httpbin.org/post', data=m,
#                  headers={'Content-Type': m.content_type})

#class ItemPostView...
def tg_now(request, slug):
  msg = 'NOW post item'
  item = Item.objects.filter(slug=slug).first()
  msg = '*'+item.name + '* \n ' + item.descr
  furl = 'https://helfa99.loca.lt/static/img/JBL-TLX-30.jpg'
  res2 = bot.sendPhoto(chat_id, photo=furl, caption=item.name)
  result = bot.sendMessage(chat_id,
      text=msg,
      parse_mode=bot.PARSE_MODE_MARKDOWN)
  #fn = os.path.join(settings.BASE_DIR, 'verschenka/JBL-TLX-30.jpg')
  lg.debug(result)
  lg.debug(res2)
  return HttpResponse('OK DONE')

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
    """
    def get_object(self, **kwargs):
        lg.debug('get_object', kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = None
        if pk is not None:
            queryset = queryset.filter(pk=pk)
            obj = queryset.get()
            tg_post(obj)
        self.obj = obj
        return obj
    """

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
            #return self.access_denied()
            pass
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
#        tg_post(self.object)
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
        context.update(self.get_user_context())
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
