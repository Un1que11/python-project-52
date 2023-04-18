from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import NewStatusCreationForm
from .models import Status


class StatusListView(SuccessMessageMixin, ListView, LoginRequiredMixin):
    model = Status
    template_name = 'statuses/show.html'
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    form_class = NewStatusCreationForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')


class StatusUpdateView(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = Status
    form_class = NewStatusCreationForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class StatusDeleteView(SuccessMessageMixin, DeleteView, LoginRequiredMixin):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('users-list')
    success_message = _('Status successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().status.all().exitsts():
            messages.error(
                    self.request,
                    _('Unable to delete status because it is in use')
                    )
            return redirect('statuses')

        return super().post(request, *args, **kwargs)
