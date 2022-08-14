
from .PageController import PageController
from django.views.decorators.csrf import ensure_csrf_cookie

import logging
lg = logging.getLogger()



@ensure_csrf_cookie
def page(request, name):
  ctrl = PageController(request)
  ctrl.name = name
  ctrl.context.update( {'name': name} )
  ctrl.template_name = 'page.html'
  return ctrl.render()

def index(request):
  return page(request, 'one')



