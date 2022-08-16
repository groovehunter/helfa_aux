from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .settings import TMPPATH, DEBUG, DEBUG2, FORCE_SCRIPT_NAME
from .BaseCtrl import BaseCtrl
from .telegram import prepare_login_widget
import logging
lg = logging.getLogger('root')


class Controller(BaseCtrl):

    def __init__(self, request):
        self.context = {}
        #if DEBUG: self.init_logging()
        if DEBUG2:
            self.context['debug2'] = True
        self.request = request
        # correct location to check user?
        self.check_user()
        self.init_ctrl()

    def check_user(self):
        lg.debug('check_user')
        lg.debug(self.request.user)
        if self.request.user.is_authenticated:
          self.context['logged_in'] = True
          self.context['username'] = self.request.user.username
        else:
          self.prepare_tg_widget()

    def prepare_tg_widget(self):
        widget = prepare_login_widget()
        self.context['telegram_login_widget'] = widget        


    def init_ctrl(self):
        self.msg = ''
        self.context['show_nav'] = True   # show navbar by default
        self.yaml_load()
        self.yamlmenu()

        if self.request.GET:
            GET = self.request.GET
            if 'msg' in GET:
                self.context['msg'] = GET['msg']


    def render(self):
        t = loader.get_template(self.template_name)
        html = t.render(self.context, request=self.request)
        if self.msg:
            self.context['msg'] = self.msg
        self.response = HttpResponse( )
        #self.response['Cache-Control'] = 'no-cache'
        self.response.write(html)
        return self.response

    def redirect(self, url, msg=''):
        if msg:
            url = FORCE_SCRIPT_NAME + url + '?msg=' + msg
        return HttpResponseRedirect(url)

