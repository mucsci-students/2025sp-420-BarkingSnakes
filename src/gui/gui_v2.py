from flask import Flask, request, Response, render_template, jsonify

from umlrelationship import RelationshipType
from views.umlview_gui_observer import UmlViewGuiObserver
import umlcommands.controller_commands as c_cmd
from utilities.model_utils import UmlClassNamedTupledEncoder
import errors

app = UmlViewGuiObserver(__name__)

@app.route("/")
def index():
    return render_template("flask.html")

@app.get("/classlist")
def class_list():
    """"""
    cmd_string = "class list"
    cmd:c_cmd.ListClassesCommand = app.parse_command(cmd_string)
    app.handle_command(cmd)
    result = cmd.get_result()
    if result.outcome == c_cmd.CommandOutcome.SUCCESS:
        classes = [c.class_name for c in cmd.umlclasses]
        data = {"html": render_template("/_umlclasslist.html", classes=classes)}
        return jsonify(data)
    return 400

@app.route("/classdetails")
def classdetails():
    try:
        class_name = request.args.get("name")
        cmd_string = "class " + class_name
        cmd:c_cmd.GetUmlClassCommand = app.parse_command(cmd_string)
        app.handle_command(cmd)
        result = cmd.get_result()
        if result.exception:
            raise result.exception

        if result.outcome == c_cmd.CommandOutcome.SUCCESS:
            """"""
            encoder = UmlClassNamedTupledEncoder()
            dto  = encoder.encode(cmd.umlclass)
            data = {"html": render_template("/_umlclass.html", dto=dto)}

            cmd:c_cmd.GetUmlClassCommand = app.parse_command("controller back")
            app.handle_command(cmd)

            return jsonify(data)
        return 400
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/addClass")
def add_umlclass():
    data = request.get_json()
    classname = data.get("classname")
    if classname:
        # app.controller.execute_command(["class", "add", classname])
        cmd_string = "class add " + classname
        cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
        app.handle_command(cmd)
        result = cmd.get_result()
        if result.exception:
            raise result.exception

        if result.outcome == c_cmd.CommandOutcome.SUCCESS:
            """"""
            return Response(status=202)
        
    return Response(status=406)

@app.post("/deleteclass")
def delete_umlclass():
    data = request.get_json()
    classname = data.get("classname")
    # override = data.get("override") or False
    # app.controller.execute_command(["class", classname])
    # app.controller.execute_command(["delete", str(override)])

    if classname:
        commands = ["class " + classname, "delete", "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
                
        return jsonify({"message": "Class deleted successfully"}), 200
    
    return 400

@app.post("/renameClass")
def rename_umlclass():
    try:
        data = request.get_json()
        oldname = data.get("oldname")
        newname = data.get("newname")
        commands = ["class " + oldname, "rename " + newname, "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
            
        return jsonify({"message": "Class renamed successfully"}), 200
    except errors.UMLException as uml_e:
        app.view.handle_umlexception(uml_e)
        return app.view.response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/addField")
def add_field():
    data = request.get_json()
    fieldname = data.get("fieldname")
    classname = data.get("classname")
    ftype = data.get("type")
    if fieldname:
        commands = ["class " + classname, f"field add {fieldname} {ftype}", "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
        return jsonify({"message": "Field added successfully"}), 202
    return jsonify({"error": "Missing field name, class name, or field type"}), 406

@app.post("/deleteField")
def delete_field():
    data = request.get_json()
    fieldname = data.get("fieldname")
    classname = data.get("classname")
    if fieldname:
        commands = ["class " + classname, f"field delete {fieldname}", "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
        return jsonify({"message": "Field deleted successfully"}), 200
    return jsonify({"error": "Missing field or class name"}), 406

@app.post("/renameField")
def rename_field():
    data = request.get_json()
    classname = data.get("classname")
    oldname = data.get("oldname")
    newname = data.get("newname")
    if classname and oldname and newname:
        commands = ["class " + classname, f"field rename {oldname} {newname}", "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
        return jsonify({"message": "Field renamed successfully"}), 200
    return jsonify({"error": "Field rename failed"}), 406

@app.post("/addMethod")
def add_method():
    data = request.get_json()
    methodname = data.get("methodname")
    returntype = data.get("returntype")
    classname = data.get("classname")
    if methodname and classname and returntype:
        commands = ["class " + classname, f"method add {methodname} {returntype}", "controller back"]
        for cmd_string in commands:
            cmd:c_cmd.AddClassCommand = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception
        return jsonify({"message": "Method added successfully"}), 202
    return jsonify({"error": "Missing method name, return type, or class name"}), 406

@app.put("/renameMethod")
def rename_method():
    data = request.get_json()
    class_name = data.get("classname")
    oldname = data.get("oldname")
    newname = data.get("newname")
    arity = data.get("arity")
    if class_name and oldname and newname:
        # app.controller.execute_command(["class", class_name])
        # app.controller.execute_command(["method", "rename", oldname, newname, "arity", arity])
        return Response(status=202)
    return Response(status=406)

@app.get("/loadfile")
def loadFile():
    """"""
    file = request.args.get("filename")
    # override = request.args.get("override").capitalize() or False
    # print("[gui::loadFile]", file, override)
    # app.controller.load_project(file, override == "True")
    # app.controller.execute_command(["load", file, str(override)])
    return Response(status=200)

@app.route("/relationList")
def relation_list():
    # project_dto = app.controller._get_model_as_data_object()
    relation_types = list(filter(lambda n: n != "DEFAULT", RelationshipType._member_names_))

    cmd:c_cmd.ListRelationCommand = app.parse_command("relation list")
    app.handle_command(cmd)
    result = cmd.get_result()
    if result.exception:
        raise result.exception

    relationships = [
        {
            'source': r.source_class.class_name,
            'destination': r.destination_class.class_name,
            'relation_type': r.relationship_type.name
        } for r in cmd.relationships
    ]

    cmd:c_cmd.ListClassesCommand = app.parse_command("class list")
    app.handle_command(cmd)
    result = cmd.get_result()
    if result.exception:
        raise result.exception
    
    classes = cmd.umlclasses

    class Model:
        def __init__(self, classes, relationships):
            self.classes = classes
            self.relationships = relationships

    model = Model(classes, relationships)

    data = {
        'html': render_template("_umlrelationshiplist.html", model=model, relation_types=relation_types),
        'model': {
            'relationships': relationships
        }
    }

    return jsonify(data)

@app.post("/updateClassPosition")
def update_umlclass_position():
    """updates the position in the model of the class the user just stopped dragging"""
    data = request.get_json()
    classname = data.get("classname")
    x_pos = float(data.get("x_pos"))
    y_pos = float(data.get("y_pos"))
    
    # tell controller to tell model to update position
    if classname and x_pos and y_pos:
        commands = ["class " + classname, f"class position set {x_pos} {y_pos}", "controller back"]
        for cmd_string in commands:
            cmd = app.parse_command(cmd_string)
            app.handle_command(cmd)
            result = cmd.get_result()
            if result.exception:
                raise result.exception

    return jsonify({"message": "Class position updated successfully"}), 200

@app.post("/addRelation")
def add_relation():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    relation_type = data.get('type')
    if source and destination and relation_type:
        cmd:c_cmd.RelationAddCommand = app.parse_command(f"relation add {source} {destination} {relation_type}")
        app.handle_command(cmd)
        result = cmd.get_result()
        if result.exception:
            raise result.exception
        return Response(status=202)
    return Response(status=406)

@app.post("/deleteRelation")
def delete_relation():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    if source and destination:
        cmd_string = f"relation delete {source} {destination}"
        cmd = app.parse_command(cmd_string)
        app.handle_command(cmd)
        result = cmd.get_result()
        if result.exception:
            raise result.exception
        return Response(status=202)
    return Response(status=406)