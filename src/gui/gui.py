from flask import Flask, request, Response, render_template, jsonify

from umlcontroller import UmlController
from view import View
import os

class UmlFlaskApp(Flask):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller:UmlController = None
        self.view:View = None
    
    def set_controller(self, controller:UmlController):
        self.controller = controller
        self.view = controller.view


# app = Flask(__name__)
app = UmlFlaskApp(__name__)

@app.route("/")
def index():
    return render_template("flask.html")

@app.route("/run",methods=["POST"])
def run():
    """"""
    # g.get("controller").run()
    app.controller.run()
    return Response(status=200)

@app.route("/quit", methods=["POST"])
def quit():
    app.controller.running = False
    app.view.set_command("quit")

    return Response(status=200)

@app.route("/command", methods=["POST"])
def command():
    # g.get("controller").view.set_command("class add Car")
    app.view.set_command("class add Car")
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
    return jsonify(app.controller.model.classes)

@app.route("/classdetails")
def classdetails():
    class_name = request.args.get('name')
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
    data = {'html': render_template("/_umlclass.html", dto = dto)}
    return jsonify(data)

@app.post("/renameField")
def rename_field():
    data = request.get_json()
    class_name = data.get('classname')
    oldname = data.get('oldname')
    newname = data.get('newname')

    app.controller.execute_command(["class", class_name])
    app.controller.execute_command(["field", "rename", oldname, newname])

    return Response(status=200)




@app.post("/setActiveClass")
def set_active_class():
    try:
        data = request.get_json()
        app.view.set_command(f"class {data.get('classname')}")
        while app.view.get_renderable() is None:
            True
        renderable = app.view.get_renderable()
        data = {
            'html': renderable.render(),
            'data': renderable.umlclass
        }
        app.view.render(None)
        return jsonify(data), 200
    except Exception as e:
        print("Failed: route setActiveClass")
        print(e)

@app.get("/loadfile")
def loadFile():
    """"""
    file = request.args.get("filename")
    app.controller.load_project(file)
    return Response(status=200)