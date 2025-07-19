from django.db import models

from api.models import User, Notice


class Event(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='events', verbose_name="Связанное уведомление")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название события")
    date = models.DateField(verbose_name="Дата события")
    time = models.TimeField(blank=True, null=True, verbose_name="Время события")

    def __str__(self):
        return f"Событие {self.name} - {self.date}"

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"