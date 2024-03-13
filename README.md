# Query Builder

## Построитель запросов
MVP приложения для аналитиков, которые не умеют писать SQL-запросы 
![Comrade-wolf](assets/preview.gif?raw=true "Comrade-wolf")

Общение пользователя с бэкендом происходит через Flask
Пользователь может сам выбрать поля, которые должны сформировать запрос. 

Настройка таблиц, полей и соединений происходит через toml-файлы

### Типы полей
1. ![Нечисловые поля](assets/non_numerical_field.png?raw=true "Нечисловые поля") <br/>Обычное поле. Можно использовать в select без вычислений и в where. Доступны калькуляции count, count distinct
2. ![Числовые поля](assets/numerical_field.png?raw=true "Числовые поля") <br/>Числовое поле. Можно использовать в select без вычислений и в where. Доступны калькуляции count, count distinct, sum, avg
3. ![Преднастроенный фильтр](assets/predefined_filter.png?raw=true "Преднастроенный фильтр") <br/>Сложный фильтр. Можно использовать в where. Разработчик настраивает любые фильтры в toml-файле в sql-формате
4. ![Преднастроенное вычисление](assets/predefined_calculation.png?raw=true "Преднастроенное вычисление") <br/>Сложное вычисление с возможностью добавления фильтра. Разработчик настраивает любые фильтры в toml-файле в sql-формате. Например, сумма запасов на начало каждого месяца

### С какой структурой БД лучше всего работает
Лучше всего применима для реляционных моделей, снежинка, звездочка

### Джойны между фактовыми таблицами
Джойны между фактовыми таблицами реализованы через CTE следующей структуры:
```
with
 cte_0 as (
             all fields for fact_table[0]
            ,all dimension table fields
         )
,cte_1 as (
             all fields for fact_table[1]
            ,all dimension table fields
          )
,cte_i as (
             all fields for fact_table[i]
            ,all dimension table fields
          )
cte_main as (UNION of all non calculation fields)

select
    ..,fields
from cte_main
    left join cte_0
    left join cte_1
    left join cte_i
where if needed
group by if needed
```

