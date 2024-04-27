from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MailingMessageListView, MailingMessageCreateView, MailingMessageDetailView, MailingMessageUpdateView, \
    MailingMessageDeleteView, MailingSettingsListView, MailingSettingsCreateView, MailingSettingsDetailView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, HomePage

app_name = ClientConfig.name

urlpatterns = [
    path('list_client/', ClientListView.as_view(), name='list_client'),
    path('create/', ClientCreateView.as_view(), name='create_client'),
    path('detail/<int:pk>/', ClientDetailView.as_view(), name='detail_client'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('message_list/', MailingMessageListView.as_view(), name='message_list'),
    path('message_create/', MailingMessageCreateView.as_view(), name='message_create'),
    path('message_detail/<int:pk>/', MailingMessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>/', MailingMessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='message_delete'),

    path('settings_list/', MailingSettingsListView.as_view(), name='settings_list'),
    path('settings_create/', MailingSettingsCreateView.as_view(), name='settings_create'),
    path('settings_detail/<int:pk>/', MailingSettingsDetailView.as_view(), name='settings_detail'),
    path('settings_update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='settings_update'),
    path('settings_delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='settings_delete'),

    path('', cache_page(60)(HomePage.as_view()), name='home_page'),

]
