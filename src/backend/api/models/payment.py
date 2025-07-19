from django.db import models

from api.models import User, Notice


class Payment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='payments', verbose_name="Связанное уведомление")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название платежа")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    day = models.DateField(verbose_name="Дата платежа")

    def __str__(self):
        return f"Платеж {self.name} - {self.cost}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"