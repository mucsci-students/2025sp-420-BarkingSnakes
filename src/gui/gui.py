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
    class_info = app.controller.model.classes
    details = class_info.get(class_name, {"fields": [], "methods": []})
    return jsonify(details)

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

@app.post("/saveproject")
def save():
    """"""
    file = request.args.get("filename")
    app.controller.save_project(file)
    return Response(status=200)
    
