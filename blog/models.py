from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='materials/', verbose_name='превью', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name='Активно')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
