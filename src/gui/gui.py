import functools
from flask import Flask, request, Response, render_template, jsonify

from umlcontroller import UmlController
from views.umlview_gui import UmlGuiView
from umlrelationship import RelationshipType
from utilities.uml_svg_builder import UmlDiagramSvgBuilder
from utilities.model_utils import UmlModelNamedTupleEncoder
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
    # if there was a "true" override, don't show the modal again
    override = request.args.get("override") == "true"
    if app.controller.model.has_unsaved_changes and not override:
        return jsonify({
            "action": "showModal",
            "tagId": "yesNoModal",
            "error": "You have unsaved changes. Are you sure you want to quit?"
        }), 400
    app.view.set_command("quit")
    return Response(status=200)


@app.get("/classlist")
def class_list():
    try:
        #this is probably not MVC
        classes = [k for k in app.controller.model.classes.keys()]
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
        model = app.controller.model
        umlclass = model.get_umlclass(class_name)
        if not umlclass:
            raise errors.NoSuchObjectException(f"Class '{class_name}' does not exist.")
        dto = app.controller._get_class_data_object(umlclass)
        position = umlclass.get_umlclass_position()
        # passes the position separate from the html, this may need changed
        data = {"html": render_template("/_umlclass.html", dto=dto), "x_pos": position[0], "y_pos": position[1]}
        return jsonify(data)
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    return jsonify({"message": "Class deleted successfully"}), 200


@app.post("/renameClass")
def rename_umlclass():
    try:
        data = request.get_json()
        oldname = data.get("oldname")
        newname = data.get("newname")
        app.controller.execute_command(["class", oldname])
        app.controller.execute_command(["rename", newname])
        app.controller.view.set_active_class(newname)
        return jsonify({"message": "Class renamed successfully"}), 200
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.post("/updateClassPosition")
@handle_umlexception
def update_umlclass_position():
    """updates the position in the model of the class the user just stopped dragging"""
    data = request.get_json()
    classname = data.get("classname")
    
    # enter class context
    app.controller.execute_command(["class", classname])
    x_pos = float(data.get("x_pos"))
    y_pos = float(data.get("y_pos"))
    
    # tell controller to tell model to update position
    app.controller.command_update_umlclass_position(x_pos, y_pos)
    return jsonify({"message": "Class position updated successfully"}), 200

@app.post("/addField")
@handle_umlexception
def add_field():
    data = request.get_json()
    fieldname = data.get("fieldname")
    classname = data.get("classname")
    type = data.get("type")
    if fieldname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["field", "add", fieldname, type])
        return jsonify({"message": "Field added successfully"}), 202
    return jsonify({"error": "Missing field name, class name, or field type"}), 406

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
    methodtype = data.get("returntype")
    paramlist = data.get("paramlist").split()
    classname = data.get("classname")
    
    if methodname and classname:
        app.controller.execute_command(["class", classname])
        thecmd = ["method", "add", methodname, "returns" ,methodtype]
        thecmd.extend(paramlist)
        app.controller.execute_command(thecmd)
        return jsonify({"message": "Method added successfully"}), 202
    return jsonify({"error": "Missing method name or class name"}), 406


@app.put("/renameMethod")
@handle_umlexception
def rename_method():
    data = request.get_json()
    class_name = data.get("classname")
    oldname = data.get("oldname")
    newname = data.get("newname")
    arity = data.get("arity")
    if class_name and oldname and newname:
        app.controller.execute_command(["class", class_name])
        app.controller.execute_command(["method", "rename", oldname, newname, "arity", arity])
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
    return jsonify({"message": "Project saved Successfully"}), 200


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
    classname = data.get('classname')

    if paramname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["method", methodname, "arity", str(arity)])
        app.controller.execute_command(["parameter", "add", paramname])
        return jsonify({"message": "Parameter added successfully"}), 200
    return jsonify({"error": "Missing method name or arity or parameter name"}), 406

@app.delete("/deleteMethodParam")
@handle_umlexception
def delete_param():
    data = request.get_json()
    methodname = data.get("methodname")
    arity = data.get("arity")
    parametername = data.get("parametername")
    classname = data.get("classname")
    if methodname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["method", methodname , "arity" ,arity])
        app.controller.execute_command(["parameter","delete",parametername])
        return jsonify({"message": "Parameter deleted successfully"}), 200
    return jsonify({"error": "Missing parameter name"}), 406

@app.put("/renameMethodParam")
@handle_umlexception
def rename_method_param():
    data = request.get_json()
    oldname = data.get("oldname")
    newname = data.get("newname")
    methodname = data.get("methodname")
    arity = data.get("arity")
    classname = data.get("classname")
    if classname and oldname and newname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["method", methodname , "arity" ,arity])
        app.controller.execute_command(["parameter", "rename" , oldname,newname])
        return Response(status=202)
    return jsonify({"error": "Invalid rename"}), 406

@app.delete("/deleteMethod")
@handle_umlexception
def delete_method():
    data = request.get_json()
    methodname = data.get("methodname")
    arity = data.get("arity")
    classname = data.get("classname")
    if methodname:
        app.controller.execute_command(["class", classname])
        app.controller.execute_command(["method", "delete", methodname, "arity" ,arity])
        return jsonify({"message": "Method deleted successfully"}), 200
    return jsonify({"error": "Missing method name or arity"}), 406

@app.route("/relationList")
@handle_umlexception
def relation_list():
    project_dto = app.controller._get_model_as_data_object()
    relation_types = list(filter(lambda n: n != "DEFAULT", RelationshipType._member_names_))

    class_names = [c.name for c in project_dto.classes]

    print("Classes in project:", class_names)
    print("Relationships in project:", [
        {
            'source': r.source,
            'destination': r.destination,
            'relation_type': r.relation_type
        } for r in project_dto.relationships
    ])

    data = {
        'html': render_template(
            "_umlrelationshiplist.html",
            model=project_dto,
            relation_types=relation_types,
            class_names=class_names
        ),
        'model': {
            'relationships': [
                {
                    'source': r.source,
                    'destination': r.destination,
                    'relation_type': r.relation_type
                } for r in project_dto.relationships
            ],
            'classes': class_names
        }
    }

    return jsonify(data)

@app.post("/addRelation")
@handle_umlexception
def add_relation():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    relation_type = data.get('type').upper()
    if source and destination and relation_type:
        app.controller.execute_command(["relation", "add", source, destination, relation_type])
        return jsonify({"message": "Relation added successfully"}), 202
    return jsonify({"error": "Invalid input"}), 406

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

@app.post("/updateRelationType")
@handle_umlexception
def update_relation_type():
    data = request.get_json()
    source = data.get("source")
    destination = data.get("destination")
    new_type = data.get("type").upper()

    if source and destination and new_type:
        app.controller.execute_command(["relation", "set", source, destination, new_type])
        return jsonify({"message": "Relationship type updated successfully"}), 200
    return jsonify({"error": "Invalid input"}), 406

@app.get("/getClassData")
def get_class_data():
    class_name = request.args.get("name")
    umlclass = app.controller.model.get_umlclass(class_name)
    if umlclass is None:
        return jsonify({"error": "Class not found"}), 404

    dto = app.controller._get_class_data_object(umlclass)
    relationships = [
        {
            "source": r.source_class.class_name,
            "destination": r.destination_class.class_name,
            "relation_type": r.relationship_type.name
        }
        for r in app.controller.model.relationships
        if r.source_class.class_name == class_name or r.destination_class.class_name == class_name
    ]

    return jsonify({
        "fields": [{"name": f.name, "type": f.type} for f in dto.fields],
        "methods": [ {
            "name": m.name,
            "return_type": m.return_type,
            "params": [{"name": p.name, "type": p.type} for p in m.params]
        } for m in dto.methods],
        "relationships": relationships
    })


@app.post("/export")
def export():
    data = request.get_json()
    fname = data.get("filename")
    app.controller.execute_command(["export", fname])
    return Response(status=200)