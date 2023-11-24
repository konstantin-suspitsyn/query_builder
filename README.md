# Query Builder

## Как начать работать
### Установка БД
1. Установить Docker
2. Открыть терминал
3. Перейти в папку ```docker_postgres_test_env```
4. Запустить команду в терминале```docker compose up```
5. По очереди запустить sql запросы
6. Если в DBeaver ты не видишь БД, то зайти в настройки соединения ```F4 → Connection Settings → PostgreSQL → Show all databases```

## Документация 
### Tables.toml
```
# Все, что касается таблицы
table = "название таблицы"
schema = "схема"
database = "база данных"

# Поля
[fields]
#
# type — тип поля. Может быть select (нельзя складывать, считать среднее и т. п.). math — можно делать вычисления, groupping — поле для груупировки данных, вычисления делать нельзя 
# show — true, если выводим на frontend (по умолчанию). false — если не выводим
# name — название, если выводим на frontend
# exclude_from_group содержит список полей, кторые должны быть исключены из select, если type = groupping и входит в join
#
sk_item_id = {type = "select", show = "false"}
bk_item_id = {type = "select",show = "false"}
bk_item_name = {type = "select",show = "true", name="Название товара"}
bk_combined_map = {type = "groupping", name="Жанр", show="true", exclude_from_group = ["sk_account_id", "bk_account_id", "bk_account_name"], same_field="query_builder.public.dim_item.dim_account"}

```