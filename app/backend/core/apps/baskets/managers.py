from django.db import models


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        """Сумма стоимостей всех услуг в корзине через аннотацию"""
        return self.annotate(
            price=models.F('project_service__price')
        ).aggregate(total=models.Sum('price'))['total'] or 0

    def total_quantity(self):
        """Количество элементов в корзине через COUNT()"""
        return self.count()

    def for_user_or_session(self, user, session_key):
        """Фильтрация корзины по пользователю или сессии"""
        if user and user.is_authenticated:
            return self.filter(user=user)
        return self.filter(session_key=session_key, user__isnull=True)

class BasketManager(models.Manager):
    def get_queryset(self):
        return BasketQuerySet(self.model, using=self._db)

    def total_sum(self):
        return self.get_queryset().total_sum()

    def total_quantity(self):
        return self.get_queryset().total_quantity()

    def for_user_or_session(self, user, session_key):
        return self.get_queryset().for_user_or_session(user, session_key)