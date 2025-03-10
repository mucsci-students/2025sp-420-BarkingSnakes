import functools
from flask import Flask, request, Response, render_template, jsonify

from umlcontroller import UmlController
from views.umlview_gui import UmlGuiView
from umlrelationship import RelationshipType
import errors
import sys


class UmlFlaskApp(Flask):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller: UmlController = None
        self.view: UmlGuiView = None

    def set_controller(self, controller: UmlController):
        self.controller = controller
        self.view = controller.view

    def set_view(self, view: UmlGuiView):
        self.view = view


# app = Flask(__name__)
app = UmlFlaskApp(__name__)


def handle_umlexception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.UMLException as uml_e:
            app.view.handle_umlexception(uml_e)
            return app.view.response

    return wrapper


@app.route("/")
def index():
    return render_template("flask.html")


@app.post("/quit")
@handle_umlexception
def quit():
    app.view.set_command("quit")
    # sys.exit(0)
    # app.controller.execute_command(["quit"])
    return Response(status=200)


@app.get("/classlist")
def class_list():
    # app.view.set_command("class list")
    # while app.view.get_renderable() is None:
    #     True
    # renderable = app.view.get_renderable()
    # data = {
    #     'html': renderable.render(),
    #     'data': renderable.classes
    # }
    # app.view.render(None)
    # return jsonify(data), 200

    # return jsonify(app.controller.model.classes)
    try:
        classes = [k for k in app.controller.model.classes.keys()]
        # project_dto = app.view.get_umlproject()
        # classes = [c.name for c in project_dto.classes]
        data = {"html": render_template("/_umlclasslist.html", classes=classes)}

        return jsonify(data)
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response


@app.route("/classdetails")
def classdetails():
    try:
        class_name = request.args.get("name")
        if class_name and app.controller.view.active_class != class_name:
            app.controller.execute_command(["class", class_name])
        elif not class_name and app.controller.view.active_class:
            class_name = app.controller.view.active_class
        # class_info = app.controller.model.classes
        model = app.controller.model
        umlclass = model.get_umlclass(class_name)
        # details = class_info.get(class_name, {"fields": [], "methods": []})
        dto = app.controller._get_class_data_object(umlclass)
        # dto = {
        #     'name':_dto.name,
        #     'fields': [f.name for f in _dto.fields],
        #     'methods':[{'name':m.name, 'params':[p.name for p in m.params]} for m in _dto.methods]
        # }
        data = {"html": render_template("/_umlclass.html", dto=dto)}
        return jsonify(data)
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response


@app.post("/addClass")
@handle_umlexception
def add_umlclass():
    data = request.get_json()
    classname = data.get("classname")
    if classname:
        app.controller.execute_command(["class", "add", classname])
        return Response(status=202)
    return Response(status=406)


@app.post("/deleteclass")
@handle_umlexception
def delete_umlclass():
    data = request.get_json()
    classname = data.get("classname")
    override = data.get("override") or False
    app.controller.execute_command(["class", classname])
    app.controller.execute_command(["delete", str(override)])
    return Response(status=202)


@app.post("/renameClass")
def rename_umlclass():
    try:
        data = request.get_json()
        oldname = data.get("oldname")
        newname = data.get("newname")
        app.controller.execute_command(["rename", newname])
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response


@app.post("/addField")
@handle_umlexception
def add_field():
    data = request.get_json()
    fieldname = data.get("fieldname")
    classname = data.get("classname")
    if fieldname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["field", "add", fieldname])
        return jsonify({"message": "Field added successfully"}), 202
    return jsonify({"error": "Missing field"}), 406

@app.post("/deleteField")
@handle_umlexception
def delete_field():
    data = request.get_json()
    fieldname = data.get("fieldname")
    classname = data.get("classname")
    if fieldname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["field", "delete", fieldname])
        return jsonify({"message": "Field deleted successfully"}), 200
    return jsonify({"error": "Missing field or class name"}), 406

@app.post("/renameField")
@handle_umlexception
def rename_field():
    data = request.get_json()
    class_name = data.get("classname")
    oldname = data.get("oldname")
    newname = data.get("newname")
    if class_name and oldname and newname:
        app.controller.execute_command(["class", class_name])
        app.controller.execute_command(["field", "rename", oldname, newname])
        return jsonify({"message": "Field renamed successfully"}), 200
    return jsonify({"error": "Field rename failed"}), 406


@app.post("/addMethod")
@handle_umlexception
def add_method():
    data = request.get_json()
    methodname = data.get("methodname")
    if methodname:
        app.controller.execute_command(["method", "add", methodname])
        return Response(status=202)
    return Response(status=406)


@app.post("/renameMethod")
@handle_umlexception
def rename_method():
    data = request.get_json()
    class_name = data.get("classname")
    oldname = data.get("oldname")
    newname = data.get("newname")
    if class_name and oldname and newname:
        app.controller.execute_command(["class", class_name])
        app.controller.execute_command(
            ["method", "rename", oldname, newname, "arity", "0"]
        )
        return Response(status=202)
    return Response(status=406)


@app.post("/setActiveClass")
def set_active_class():
    try:
        data = request.get_json()
        app.view.set_command(f"class {data.get('classname')}")
        while app.view.get_renderable() is None:
            True
        renderable = app.view.get_renderable()
        data = {"html": renderable.render(), "data": renderable.umlclass}
        app.view.render(None)
        return jsonify(data), 200
    except Exception as e:
        print("Failed: route setActiveClass")
        print(e)


@app.get("/loadfile")
@handle_umlexception
def loadFile():
    """"""
    file = request.args.get("filename")
    override = request.args.get("override").capitalize() or False
    print("[gui::loadFile]", file, override)
    # app.controller.load_project(file, override == "True")
    app.controller.execute_command(["load", file, str(override)])
    return Response(status=200)


@app.post("/saveproject")
@handle_umlexception
def save():
    """"""
    data = request.get_json()
    print(data)
    file = data.get("filename")
    override = data.get("override") or False
    # app.controller.save_project(file)
    command = ["save", file, str(override)]
    app.controller.execute_command(command)
    return Response(status=200)


@app.post("/newproject")
@handle_umlexception
def newproject():
    """"""
    data = request.get_json()
    file = data.get("filename")
    override = data.get("override_file") or False
    command = ["new", file, str(override)]
    print(command)
    app.controller.execute_command(command)
    return Response(status=202)
    
@app.post("/addMethodParam")
@handle_umlexception
def add_method_param():
    data = request.get_json()
    methodname = data.get('methodname')
    paramname = data.get('paramname')
    arity = data.get('arity')
    
    app.controller.execute_command(["method", methodname, "arity", str(arity)])
    app.controller.execute_command(["parameter", "add", paramname])
    return Response(status=200)

@app.route("/relationList")
@handle_umlexception
def relation_list():
    project_dto = app.controller._get_model_as_data_object()
    relation_types = list(filter(lambda n: n != "DEFAULT", RelationshipType._member_names_))

    data = {'html': render_template("_umlrelationshiplist.html", model = project_dto, relation_types = relation_types)}

    return jsonify(data)

@app.post("/addRelation")
@handle_umlexception
def add_relation():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    relation_type = data.get('type')
    if source and destination and relation_type:
        app.controller.execute_command(["relation", "add", source, destination, relation_type])
        return Response(status=202)
    return Response(status=406)

@app.post("/deleteRelation")
@handle_umlexception
def delete_relation():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    if source and destination:
        app.controller.execute_command(["relation", "delete", source, destination])
        return Response(status=202)
    return Response(status=406)