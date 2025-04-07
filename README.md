# BS-uml
## 2025sp-420-BarkingSnakes 
## Contributors
- Evan Magill
- John Hershey
- Kyle Kalbach
- Steven Barnes
- Juliana Vinluan
- Spencer Hoover

## Windows Installation Instructions
1. Install python3 a version >= 3.9 if not present https://www.python.org/downloads/windows/
2. Install a python virtual environment with `python -m venv venv`
3. Activate the virtual environment with `.\venv\scripts\activate`
4. Install required packages with `pip install -r requirements.txt`

## Linux Installation Instructions
1. Install python3 a version >= 3.9 if not present https://docs.python.org/3/using/unix.html
2. Install pip use `apt install python3-pip`
3. Install a python virtual environment use `python3 -m venv venv`
4. To Activate the virtual environment use `source venv/bin/activate`
5. Install required packages using `pip install -r requirements.txt`
6. To deactivate virtual environment type `deactivate`

## Running the program
- Windows: `python src\uml.py`
      or to start in CLI: `python src\uml.py --cli`
- Linux: `python3 src/uml.py`
      or to start in CLI: `python3 src/uml.py --cli`
### CLI Mode:
In the command-line interface, type the help command to see a list of possible commands and their usage.

### GUI Mode (Flask):
Interact with the web-based interface after it opens in your browser or by navigating to the URL provided when the Flask server starts. Use the toolbar, menus, and on-screen instructions to manage your class diagrams.

## GUI Instructions
When running BS-uml in GUI mode, the following applies:

Launching the GUI:
The program starts a Flask server, which hosts the GUI on a local web address (default: http://127.0.0.1:5000). Check your terminal for the exact URL once the server is running.

### Using the Web Interface:
#### Main Page:
The browser window will display the main interface where you can create and edit class diagrams.
#### Toolbar & Menus:
Use on-screen buttons and menu options to add new classes, define fields/methods, and establish relationships like inheritance or composition.
#### Saving & Loading Diagrams:
The interface includes options for saving your current diagram or loading a previously saved diagram.

### How-to GUI
#### NOTICE: To be able to save project, must click 'new' button to start
Upper Tool Bar includes: new, save, load, quit
New
    Create a new project file with a <filename.json> provided 
Load
    Load the file at the <filename.json> given
Save
    Save the file with the given name
Quit
    Quits the program. Prompts 'Are you sure?'

#### Navigation
Side pop buttons:
ClassList
    View current classes, or add more
RelationList
    View all relationships in the current project.
Within ClassList:
To enter the details of that class, click on the class name and you can view: fields, methods and parameters. 

Adding, renaming, and deleting - classes, fields, methods, and parameters:
      add
            click on appropriately labeled button
      rename
            Click on the field, method, or parameter 'name' to reveal a textbox where you can rename it
      delete
            Click on the red x box on the right of the field, method, or parameter you want to delete

Within RelationList:
Shows list of existing relationships by displaying type, source class, and target class.
      add
            Choose type from drop down and classes from drop downs
      edit
            Use appropriate drop downs to edit existing relationships
      remove
            Click red x box on the right of the relationship to remove
            

## Running tests
- Use for specific test 
   Windows: `pytest tests\<test_testname>` 
   Linux: `pytest tests/<test_testname>`
- Use to run all tests `pytest`
- Current available test names  
  `test_attributeObj.py`  
  `test_classObj.py`  
  `test_save_load.py`  
  `test_user_input.py`  
  `test_relation.py`
  `test_fieldObj.py`
- To check code coverage and print to terminal
   Windows: `pytest --cov --cov-report term`
   Linux: `pytest --cov --cov-report term`

## Design Patterns 
- Command
    - Used to represent the actions the user wants to take can be found in controller_commands.py
- Memento
    - Used to implemented Undo and Redo can be found in umlmodel.py
- Observer
    - Used for communication between the controller and the view can be found in umlcontroller_observer.py and umlview_observer.py
- Decorator
    - Used to add functionality in different places can be found in umlmodel.py

## Using BS-uml program
- Type the `help` commmand to see a list of possible commands and their use
