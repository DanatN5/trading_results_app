## Установка и запуск:
### Клонировать репозиторий
``` 
git clone git@github.com:DanatN5/trading_results_app.git
```
### Перейти в репозиторий проекта
````
cd trading_results_app
````

### Сконфигурируйте файл .env с со следущими переменными:
`````
REDIS_HOST
REDIS_PORT

POSTGRES_DB
POSTGRES_HOST 
POSTGRES_PORT 
POSTGRES_USER 
POSTGRES_PASSWORD 
DATABASE_URL


`````
##  Для работы необходим пактный менеджер uv:
curl -LsSf https://astral.sh/uv/install.sh | sh

## Запуск через Docker
`````
make up
`````
## Запуск на localhost
### Установка зависимостей

`````
make install
`````
### Cоздание таблиц в базе данных
`````
make migrate
`````

### Запуск приложения
````````
make runserver
````````