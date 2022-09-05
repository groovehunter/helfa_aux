
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView, DetailView
from users.models import CustomUser

from .forms import CustomUserCreationForm, CustomUserEditForm
from .UserController import UserController
from djflow.ViewController import DjMixin

class UserListView(ListView, DjMixin):
    model = CustomUser
    template_name = 'users/index.html'

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
        context = self.get_context_data()
        """
        fields = ['username', 'email']
        context['fields'] = fields
        """
        context['object_list'] = self.object_list   # XXX DRY !
        return self.render_to_response(context)


class UserDetailView(DetailView, DjMixin):
    model = CustomUser
    template_name = 'users/profile.html'
    pk_url_kwargs = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get_object(self, queryset=None):
        return CustomUser.objects.get(username=self.kwargs.get("username"))


def tg_login(request):
    ctrl = UserController(request)
    return ctrl.tg_login_user()


def login(request):
    ctrl = UserController(request)
    return ctrl.login_user()

def logout(request):
    ctrl = UserController(request)
    return ctrl.logout_user()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('users/login.html')
    else:
        form = AuthenticationForm()
    return render(request,'user/login.html', {'form':form})
