from django.db import models

class User(models.Model):
    chat_id = models.BigIntegerField(unique=True, verbose_name="ID чата в Telegram")
    user_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя пользователя")
    time_zone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Часовой пояс")

    def __str__(self):
        return f"{self.user_name} (chat_id: {self.chat_id})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"