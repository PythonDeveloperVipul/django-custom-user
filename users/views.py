from django.urls import reverse_lazy
from django.views import generic
from .models import User


class UserView(generic.ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users_data'


class UserCreateView(generic.CreateView):
    model = User
    template_name = 'users/user_create.html'
    fields = ['first_name', 'last_name', 'email', 'password']
    success_url = reverse_lazy('user_list_view')


class UserDeleteView(generic.DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list_view')


class UserUpdateView(generic.UpdateView):
    model = User
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('user_list_view')

 



