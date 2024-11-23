from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from messaging.forms import ClientForm, MessageForm, MailingCreateForm, MailingForm
from messaging.models import Mailing, Message, Client, Start, Attempt
from blog.models import Blog
from services import get_cache_mailing_active, get_mailing_count_from_cache, get_cache_unique_quantity
from users.models import User


class ClientListView(ListView):
    model = Client
    success_url = reverse_lazy('messaging:client_list')

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Возвращаем только клиентов, принадлежащих текущему пользователю
            return Client.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Client.objects.none()


class ClientDetailView(DetailView):
    model = Client
    template_name = 'messaging/client_detail.html'
    success_url = reverse_lazy('messaging:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'messaging/client_form.html'
    success_url = reverse_lazy('messaging:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание клиента'
        return context

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Client.objects.all()


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'messaging/client_form.html'
    success_url = reverse_lazy('messaging:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_item = self.get_object()
        context['title'] = client_item.first_name
        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'messaging/client_confirm_delete.html'
    success_url = reverse_lazy('messaging:client_list')


class MessageListView(ListView):
    model = Message
    success_url = reverse_lazy('messaging:message_list')

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Возвращаем только клиентов, принадлежащих текущему пользователю
            return Message.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Message.objects.none()


class MessageDetailView(DetailView):
    model = Message
    template_name = 'messaging/message_detail.html'
    success_url = reverse_lazy('messaging:message_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messaging:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание сообщения'
        return context

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messaging:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('messaging:message_list')


class MailingListView(ListView):
    model = Mailing
    success_url = reverse_lazy('messaging:mailing_list')

    def get_queryset(self):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='manager').exists():
                # Возвращаем все рассылки
                return Mailing.objects.all()
            # Возвращаем только рассылки, принадлежащих текущему пользователю
            return Mailing.objects.filter(owner=self.request.user)
        # Возвращаем пустой queryset для неаутентифицированных пользователей
        return Mailing.objects.none()


def toggle_activation(request, mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    mailing.is_active = not mailing.is_active
    mailing.save()

    action = 'активирован' if mailing.is_active else 'деактивирован'
    messages.success(request, f'Пользователь {mailing.title} был {action}.')

    return redirect('messaging:mailing_detail', pk=mailing.id)  # Перенаправляем обратно в список пользователей


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'messaging/mailing_detail.html'
    success_url = reverse_lazy('messaging:mailing_form')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     mailing_item = self.get_object()
    #     context['title'] = mailing_item.time_sending
    #     return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'messaging/mailing_form.html'
    success_url = reverse_lazy('messaging:mailing_list')
    permission_required = 'messaging.mailing_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рассылки'
        return context

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        return form

    def get_queryset(self):
        return Mailing.objects.all()


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('messaging:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        return form


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('messaging:mailing_list')


class StartListView(ListView):
    model = Blog
    template_name = 'messaging/start_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_quantity_active'] = get_cache_mailing_active()
        context['mailing_quantity'] = get_mailing_count_from_cache()
        context['clients_unique_quantity'] = get_cache_unique_quantity()
        context['records'] = Blog.objects.order_by('?')[:3]
        return context


def mailing_status(request):
    mailings = Mailing.objects.prefetch_related('attempts').all()
    return render(request, 'messaging/mailing_status.html', {'mailings': mailings})

