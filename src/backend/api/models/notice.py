from django.db import models

from api.models import User


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices', verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название уведомления")
    day_before = models.IntegerField(verbose_name="За сколько дней напоминать", help_text="0 - в тот же день")
    time_send = models.TimeField(verbose_name="Время отправки уведомления")
    creator = models.CharField(max_length=100, blank=True, null=True, verbose_name="Создатель уведомления")

    def __str__(self):
        return f"{self.name} для {self.user.user_name}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"