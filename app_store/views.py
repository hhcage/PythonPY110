from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category  # Импортируем filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart

def product_view_json(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False,
                                                                      'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            reverse = request.GET.get("reverse")
            if reverse and reverse.lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                data = filtering_category(DATABASE, category_key, ordering_key, False)
        else:
            data = filtering_category(database=DATABASE, category_key=None)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
            for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
                if data['html'] == page:
                    with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
                        return HttpResponse(f.read())
            # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
            # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
            # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
            return HttpResponse(status=404)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'app_store/product/{data["html"]}.html', encoding="utf-8") as f: # Определяем название файла для открытия
                    return HttpResponse(f.read())


def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)

# --------------------------------------------------


def cart_view_json(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result =  add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = remove_from_cart(id_product, username) # TODO Вызвать ответственную за это действие функцию remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})