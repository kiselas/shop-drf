## Инструкция по установке
```
Создать .env file

POSTGRES_USER={}
POSTGRTES_PASSWORD={}
POSTGRES_DATABASE={}
SECRET_KEY={}
```
```
sudo docker-compose up -d --build
```

## Создание суперюзера
```
docker exec -it {container_id} python manage.py createsuperuser
```

## Основные методы

### GET city/
Получение списка городов


### GET city/{city_id}/street/
Получение списка улиц относящихся к указанному городу


### POST shop/
    {
        "name": "Ашан",
        "city": "1",
        "street": "1",
        "address_number": "16",
        "open_time": "8:00",
        "closing_time": "23:00"
    }
Создание нового магазина


### GET /shop/?street={street_id}&city={city_id}&open=0/1
Получение списка магазинов. Фильтры необязательны