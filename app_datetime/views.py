from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def datetime_view(request):
    if request.method == "GET":
        data = datetime.now()  # TODO Написать, что будет возвращаться из данного представления
        return HttpResponse(data)  # TODO Вернуть объект HttpResponse с необходимыми данными


def dynamic_datetime_view(request):
    if request.method == "GET":
        data = """
        <script>
            function updateTime() {
                fetch("/datetime/")
                    .then(response => response.text()) // Получаем HTML с сервера
                    .then(html => {
                        let parser = new DOMParser();
                        let doc = parser.parseFromString(html, "text/html");
                        let time = doc.body.innerText; // Извлекаем текст (дату и время)
                        document.getElementById("time").innerText = time;
                    })
                    .catch(error => console.error("Ошибка загрузки:", error));
            }
    
            setInterval(updateTime, 1000); // Обновление каждую секунду
            window.onload = updateTime; // Загружаем первое значение при открытии страницы
        </script>
        <body>
            <h1>Текущее время:</h1>
            <p id="time">Загрузка...</p>
        </body>
        
        """
        return HttpResponse(data)
