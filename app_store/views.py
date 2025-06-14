from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category  # Импортируем filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


@login_required(login_url='app_login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(id_product, username)
        if result:
            return redirect("app_store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")


@login_required(login_url='app_login:login_view')
def cart_remove_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_cart(id_product, username)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("app_store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True},
        "coupon_old": {
            "discount": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        # TODO Проверьте, что name_coupon есть в DATA_COUPON среди ключей, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)
        if name_coupon in DATA_COUPON:
            return JsonResponse(DATA_COUPON.get(name_coupon))
        return HttpResponseNotFound("Неверный купон")
        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 90},
            "Санкт-Петербург": {"price": 78},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if data_county := DATA_PRICE.get(country):
            if data_city := data_county.get(city):
                return JsonResponse(data_city)
            return JsonResponse({"price": data_county["fix_price"]})
        return HttpResponseNotFound("Неверные данные")
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")


@login_required(login_url='app_login:login_view')
def cart_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)[username]  # Получаем корзину пользователя username

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # Получаем информацию о продукте
            # TODO в словарь product под ключом "quantity" запишите текущее значение количества товара в корзине
            product["quantity"] = quantity
            # TODO в словарь product под ключом "price_total" посчитайте и запишите общую стоимость товара как произведение
            #  его количества в корзине на цену с учетом скидки ('price_after'). Значение цены "price_total" приведите к формату
            #  2 символов после запятой
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            # TODO добавьте словарь product в конец списка products
            products.append(product)

        return render(request, "app_store/cart.html", context={"products": products})


@login_required(login_url='app_login:login_view')
def cart_view_json(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)  # TODO Вызвать ответственную за это действие функцию view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


@login_required(login_url='app_login:login_view')
def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(
            id_product, username)  # TODO Вызвать ответственную за это действие функцию add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


@login_required(login_url='app_login:login_view')
def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_cart(
            id_product, username)  # TODO Вызвать ответственную за это действие функцию remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
            reverse = request.GET.get("reverse")
            if reverse and reverse.lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)  # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=True
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          False)  # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=False
        else:
            data = filtering_category(DATABASE,
                                      category_key)  # TODO Использовать filtering_category и провести фильтрацию с параметрами category
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    data_other_products = [product for product in DATABASE.values() if product['category'] == data['category'] and product['id'] != data['id']][:5]  # TODO Переделать по заданию
                    return render(request, 'app_store/product.html', context={'product': data,
                                                                              'other_products': data_other_products})

        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                data_other_products = [product for product in DATABASE.values() if product['category'] == data['category'] and product['id'] != data['id']][:5]  # TODO Переделать по заданию
                return render(request, 'app_store/product.html', context={'product': data,
                                                                          'other_products': data_other_products})

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data,
                               "category": category_key})
