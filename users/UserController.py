from helfa_aux_dev.Controller import Controller
### XXX move all Controllers in parent directory 
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout
from helfa_aux_dev.telegram import verify_tg

from logging import getLogger
lg = getLogger(__name__)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


class UserController(Controller):

    def __init__(self, request):
        Controller.__init__(self, request)

    #method_decorator(csrf_protect)
    def login_user(self):
        lg.debug('login_user')
        request = self.request
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            lg.debug('POST', request.POST.copy())
            if form.is_valid():
                user = form.get_user()
                lg.debug('user', user.username)

                login(request, user)
                return self.redirect('/users/profile')
        else:
            form = AuthenticationForm()
        self.context['form'] = form
        self.template = 'users/login.html'
        return self.render()


    def logout_user(self):
        request = self.request
        logout(request)
        return self.redirect('/', msg='succesful logout')

    def tg_login_user(self):
        request = self.request
        hash1 = request.GET.get('hash')
        lg.debug(hash1)

        result = verify_tg(request.GET)

        res = result['first_name'] 
        lg.debug(res)

        self.template_name = 'users/profile.html'
        return self.render()


    def profile(self):
        user = self.request.user
        self.context['username'] = user.username
        self.template_name = 'users/profile.html'

        return self.render()


