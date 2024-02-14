from flask import Blueprint, current_app, render_template, request

bp = Blueprint('builder', __name__, url_prefix='/builder')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    fields = current_app.get_structure_generator().get_fields()

    front_fields = __generate_front_fields(fields)

    print(front_fields)

    if request.method == 'POST':
        print("AAAA")
        print(request.get_json())

    return render_template("builder/create.html", front_fields=front_fields)


def __generate_front_fields(fields: dict) -> dict:
    front_fields = {}

    for field in fields:

        if fields[field]["show"]:
            show_group = "Прочее"
            if "show_group" in fields[field]:
                show_group = fields[field]["show_group"]

            if show_group not in front_fields:
                front_fields[show_group] = {}

            front_fields[show_group][fields[field]["name"]] = {"field": field, "type": fields[field]["type"]}

    return front_fields
