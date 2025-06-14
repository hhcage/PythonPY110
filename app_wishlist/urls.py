from django.urls import path
from .views import wishlist_view, wishlist_view_json, wishlist_add_view_json, wishlist_del_view_json, wishlist_remove_view

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist_view'),  # TODO Зарегистрируйте обработчик
    path('api/', wishlist_view_json),
    path('api/add/<id_product>', wishlist_add_view_json),
    path('api/del/<id_product>', wishlist_del_view_json),
    path('remove/<id_product>', wishlist_remove_view, name="remove_now"),
]