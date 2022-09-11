# Тестовое задание от ГК АРТЭС (сеть аптек Таблеточка)
#### Cервис, который сохраняет переданные ему наборы данных c аптеками, позволяет их просматривать, редактировать информацию отдельных аптек, а также производить выборку по городам, регионами или ближайших на основе заданных координат и радиусу.
#### Используемые инструменты:
- Python
- Django
- Django REST framework

### Эндпоинты API:
- drugstore/ - GET, POST - все аптеки, создание аптеки
- drugstore/<id> - PUT, DELETE - редактирование аптеки, удаление аптеки
- create_drugstores/ - POST - создание записей аптек из списка

### Приложения проекта:
- api - приложения для взаимодействия посредством API
- drugstores - описание моделей, админка
 

### <span style="color:red"> В связи с тем, что данный проект является тестовым заданием секретный ключ из settings.py не выносится в .env </span>

### Автор
Владимир Кириченко