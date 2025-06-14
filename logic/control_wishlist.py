import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'  # Путь до файла избранного


def view_in_wishlist(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое wishlist.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}  # Пустое избранное для пользователя

    if os.path.exists(PATH_WISHLIST):  # Если файл с избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем избранное
            if username not in wishlist:  # Если пользователя нет в избранном, то создаем запись с пустым избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с избранным нет
        wishlist = {username: empty_user_wishlist}

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем избранное
        json.dump(wishlist, f)

    return wishlist  # Возвращаем содержимое избранного


def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)

    if id_product not in DATABASE:
        return False

    user_wishlist = wishlist[username]["products"]
    if id_product not in user_wishlist:
        user_wishlist.append(id_product)

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return True


def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist()

    user_wishlist = wishlist[username]["products"]

    if id_product not in user_wishlist:
        return False

    user_wishlist.remove(id_product)

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return True