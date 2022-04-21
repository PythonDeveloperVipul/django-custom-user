from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import User


class UserView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users_data'


class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_create_update.html'
    fields = ['first_name', 'last_name', 'email', 'password']
    success_url = reverse_lazy('user_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Add User'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list_view')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_create_update.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('user_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Update User'
        return context



