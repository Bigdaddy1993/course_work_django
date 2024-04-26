from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, max_length=150, verbose_name='email')
    name = models.CharField(max_length=100, verbose_name='name')
    comment = models.CharField(max_length=200, verbose_name='comment')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_client',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=300, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело сообщения')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'ежедневная'),
        (PERIOD_WEEKLY, 'еженедельная'),
        (PERIOD_MONTHLY, 'ежемесячная')
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'создана'),
        (STATUS_STARTED, 'запущена'),
        (STATUS_DONE, 'завершена'),
    )

    start_time = models.DateTimeField(verbose_name='время старта')
    end_time = models.DateTimeField(verbose_name='время окончания')
    period = models.CharField(max_length=30, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=30, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    clients = models.ManyToManyField(Client, related_name='mailing_settings')
    is_active = models.BooleanField(default=True, verbose_name='активно')

    def __str__(self):
        return f'{self.start_time} {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
        permissions = [
            ('set_is_activate',
             'can change active')
        ]


class MailingLog(models.Model):
    STATUS_OK = 'ok'

    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )
    last = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, verbose_name='Настройки', **NULLABLE)
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
