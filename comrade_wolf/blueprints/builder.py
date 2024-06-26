from flask import Blueprint, render_template, request, current_app

from query_builder.utils.data_types import WhereFields, AllFields
from query_builder.utils.exceptions import QueryBuilderException

bp = Blueprint('builder', __name__, url_prefix='/builder')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    select_fields: AllFields = current_app.get_structure_generator().get_fields()
    where_fields = current_app.get_structure_generator().get_where()

    front_fields = __generate_front_fields(select_fields, where_fields)

    print(front_fields)

    if request.method == 'POST':
        print(request.get_json())
        q: str
        try:
            q: str = current_app.build_query(request.get_json())
        except QueryBuilderException as e:
            q = str(e)
            q += "\nОбратитесь к администратору"
        except Exception as e:
            print(e)
            q = "\nПроизошла неизвестная ошибка. Обратитесь к администратору"
        # print(q)
        return q

    return render_template("builder/create.html", front_fields=front_fields)


def __generate_front_fields(select_fields: AllFields, where_fields: WhereFields) -> dict:
    front_fields = {}

    for field in select_fields:

        if select_fields[field]["show"]:
            show_group = "Прочее"
            if "show_group" in select_fields[field]:
                show_group = select_fields[field]["show_group"]

            if show_group not in front_fields:
                front_fields[show_group] = {}

            front_fields[show_group][select_fields.get_frontend_name(field)] \
                = {
                    "field": field,
                    "type": select_fields.get_backend_field_type(field),
                    "front_field_type":  select_fields[field]["front_field_type"],
                   }

    print(where_fields)

    for field in where_fields:
        show_group = where_fields.get_show_group(field)
        front_name = where_fields.get_frontend_name(field)

        if show_group not in front_fields:
            front_fields[show_group] = {}

        front_fields[show_group][front_name] = {"field": field, "type": "where", }

    return front_fields
