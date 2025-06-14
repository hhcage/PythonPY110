import json
import os
from app_store.models import DATABASE

PATH_CART = 'cart.json'  # Путь до файла корзины


def view_in_cart(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое корзины cart.json, если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'cart.json'
    """
    empty_user_cart = {'products': {}}  # Пустая корзина для пользователя

    if os.path.exists(PATH_CART):  # Если файл с корзиной существует
        with open(PATH_CART, encoding='utf-8') as f:  # Открываем файл
            cart = json.load(f)  # Считываем корзину
            if username not in cart:  # Если пользователя нет в корзине, то создаем запись с пустой корзиной для него
                cart[username] = empty_user_cart
    else:  # Если файла с корзиной нет
        cart = {username: empty_user_cart}

    # Запись словаря cart в cart.json
    with open(PATH_CART, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем корзину
        json.dump(cart, f)

    return cart  # Возвращаем содержимое корзины


def add_to_cart(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart = view_in_cart(username)  # TODO Помните, что у вас есть уже реализация просмотра корзины view_in_cart(username),
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # TODO Проверьте существует ли добавляемый товар с id_product в базе данных DATABASE, если нет, то возвращаем False,
    #  так как добавление в корзину прошло неуспешно.
    if id_product not in DATABASE:
        return False

    user_cart = cart[username]["products"]  # TODO в переменную user_cart запишите данные об товарах пользователя.
    #  Т.е. в user_cart будет словарь из ключа "products" для соответствующего пользователя по username.

    # ! Обратите внимание, что в переменной cart под ключем значения username находится словарь с ключом "products".
    # ! Именно в cart[username]["products"] лежит словарь где по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart[username]["products"][id_product]
    # ! Далее уже сами решайте, как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли товар с id_product в корзине пользователя user_cart, если товар существует,
    #  то увеличиваем его количество в user_cart на 1, иначе товар добавляется в первый раз и его количество равно 1.
    if id_product in user_cart:
        user_cart[id_product] += 1
    else:
        user_cart[id_product] = 1

    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные
    #  и если мы не запишем изменения, то считать измененные данные затем не получится. Так user_cart является частью
    #  словаря cart, то любые изменения в user_cart аналогично отражаются в cart, поэтому достаточно записать
    #  в 'cart.json' словарь из cart

    with open(PATH_CART, mode='w', encoding='utf-8') as f:
        json.dump(cart, f)

    return True


def remove_from_cart(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart = view_in_cart()  # TODO Помните, что у вас есть уже реализация просмотра корзины view_in_cart(), поэтому,
    # чтобы загрузить данные из корзины, не нужно заново писать код.

    # С переменной user_cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart
    user_cart = cart[username]["products"]  # TODO в переменную user_cart запишите данные об товарах пользователя.
    #  Т.е. в user_cart будет словарь из ключа "products" для соответствующего пользователя по username.

    # TODO Проверьте, существует ли товар с id_product в корзине пользователя user_cart, если нет, то возвращаем False.
    if id_product not in user_cart:
        return False

    # TODO Если существует товар, то удаляем ключ 'id_product' у user_cart,
    #  вспомните как удалять ключи у словаря.
    user_cart.pop(id_product)

    # TODO Не забываем записать обновленные данные cart в 'cart.json', аналогично как делали в add_to_cart
    with open(PATH_CART, mode='w', encoding='utf-8') as f:
        json.dump(cart, f)

    return True


if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину

    print('Проверяем корзину', "Ответ:     {'': {'products': {}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 0', 'Ответ:     False', f'Результат: {add_to_cart("0")}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_cart("1")}\n', sep='\n')
    print('Добавляем товар с id = 2', 'Ответ:     True', f'Результат: {add_to_cart("2")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'1': 2, '2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')
    print('Удаляем товар с id = 0', "Ответ:     False", f'Результат: {remove_from_cart("0")}\n', sep='\n')
    print('Удаляем товар с id = 1', "Ответ:     True", f'Результат: {remove_from_cart("1")}\n', sep='\n')
    print('Проверяем корзину', "Ответ:     {'': {'products': {'2': 1}}}", f'Результат: {view_in_cart()}\n', sep='\n')

    if os.path.exists('cart.json'):  # Если файл существует
        os.remove('cart.json')  # Удаляем корзину
