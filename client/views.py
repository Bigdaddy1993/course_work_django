import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from client.forms import MailingSettingsModeratorForm, MessageForm
from client.models import Client, MailingMessage, MailingSettings


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'client/client_form.html'
    fields = ('email', 'name', 'comment')
    success_url = reverse_lazy('client:list_client')
    login_url = reverse_lazy('user_app:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание клиента'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'
    fields = ('email', 'name', 'comment')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client_detail.html'
    success_url = reverse_lazy('client:detail_client')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('email', 'name', 'comment')
    login_url = reverse_lazy('user_app:login')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:detail_client', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:list_client')
    login_url = reverse_lazy('user_app:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MailingMessageListView(ListView):
    model = MailingMessage
    template_name = 'client/mailingmessage_list.html'
    success_url = reverse_lazy('client:message_list')


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('client:message_create')
    login_url = reverse_lazy('user_app:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание сообщения'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingMessageDetailView(DetailView):
    model = MailingMessage
    template_name = 'client/mailingmessage_detail.html'
    success_url = reverse_lazy('client:message_detail')


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    fields = ('subject', 'message')
    login_url = reverse_lazy('user_app:login')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:message_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('client:message_list')
    login_url = reverse_lazy('user_app:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MailingSettingsListView(ListView):
    model = MailingSettings
    template_name = 'client/mailingsettings_list.html'
    success_url = reverse_lazy('client:settings_list')


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    template_name = 'client/mailingsettings_form.html'
    success_url = reverse_lazy('client:settings_create')
    fields = '__all__'
    login_url = reverse_lazy('user_app:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsDetailView(DetailView):
    model = MailingSettings
    template_name = 'client/mailingsettings_detail.html'
    success_url = reverse_lazy('client:settings_detail')


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    fields = '__all__'
    login_url = reverse_lazy('user_app:login')

    def get_success_url(self):
        from django.urls import reverse
        return reverse('client:settings_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('client:settings_list')
    login_url = reverse_lazy('user_app:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class MailingSettingsModerator(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsModeratorForm
    success_url = reverse_lazy('client:settings_list')
    permission_required = 'client.set_is_active'


class HomePage(ListView):
    model = MailingSettings
    template_name = 'client/home_page.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['count_mailing'] = len(MailingSettings.objects.all())
        context_data['active_mailing'] = len(MailingSettings.objects.filter(status='started'))
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['client'] = len(Client.objects.all())
        return context_data
