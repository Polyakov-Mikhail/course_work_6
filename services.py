from django.core.cache import cache
from config.settings import CACHE_ENABLED
from django.conf import settings

from messaging.models import Mailing, Client


def get_models_from_cache(model):
    """
    Получает продукт из кэша, если кэш пустой, получает данные из БД
    """

    if not CACHE_ENABLED:
        return model.objects.all()

    # Получение имени модели из имени класса
    name_model = model.__name__.lower()
    # Получение ключа для кэширования для моделей для общего списка ("модель_list")
    key = f"{name_model}_list"

    models_cache = cache.get(key)

    # Если кэш не пустой, возвращаем данные из кэша
    if models_cache is not None:
        return models_cache

    # Если кэш пустой, получаем данные из БД и добавляем их в кэш
    models_cache = model.objects.all()
    cache.set(key, models_cache)
    return models_cache


def get_cache_mailing_active():
    if settings.CACHE_ENABLED:
        key = 'mailing_quantity_active'
        mailing_quantity_active = cache.get(key)
        if mailing_quantity_active is None:
            mailing_quantity_active = Mailing.objects.filter(status='launched').count()
            cache.set(key, mailing_quantity_active)
    else:
        mailing_quantity_active = Mailing.objects.filter(status='launched').count()
    return mailing_quantity_active


def get_mailing_count_from_cache():
    if settings.CACHE_ENABLED:
        key = 'mailing_quantity'
        mailing_quantity = cache.get(key)
        if mailing_quantity is None:
            mailing_quantity = Mailing.objects.all().count()
            cache.set(key, mailing_quantity)
    else:
        mailing_quantity = Mailing.objects.all().count()

    return mailing_quantity


def get_cache_unique_quantity():
    if settings.CACHE_ENABLED:
        key = 'clients_unique_quantity'
        clients_unique_quantity = cache.get(key)
        if clients_unique_quantity is None:
            clients_unique_quantity = len(list(set(Client.objects.all())))
            cache.set(key, clients_unique_quantity)
    else:
        clients_unique_quantity = len(list(set(Client.objects.all())))

    return clients_unique_quantity
