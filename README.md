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
5. You may need to install pyreadline3 by running `pip install pyreadline3`

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
#### Toolbar
##### Tool Bar includes: Add Class, Add Relationship, Lists, New, Save, Load, Export HTML, Quit
Add Class
    Opens a new class modal
Add Relationship
    Opens a new relationship modal
Lists
    View all classes and relationships
New
    Create a new project file with a <filename.json> provided
Load
    Load the file at the <filename.json> given
Save
    Save the file with the given name
Export HTML
    Type desired file name and click export 
Quit
    Quits the program. Prompts 'Are you sure?'

#### Navigating a class
How to add a class:
    Click the text box to type and click the Add Class button to add your new named
    Click the 'x' to exit creating a class

Editing a class:
    Click the edit button on the top-left of the class details box
    Edit the any name by clicking on the name itself while in edit mode
    Click the corresponding button to:
        Add a field
        Add a method
    Add a parameter
        *After a class is added the corresponding button to add a parameter is visible
    Close a class by click the grey 'x'
    Delete fields and methods by clicking the corresponding red 'x'
    Delete a class by clicking the red 'x' on the class list (view by clicking Lists)

Adding a relationship:
    Use the drop down menus to select the type, source class and destination class
    Remove with red 'x' button

Editing a relationship:
    While view the Lists, edit the relationship type with the drop down
    Edit by clicking on edit button to add fields and methods


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
- Chain of command 
    - Example: Change method, calls a different version of itself in different classes
- Builder
    - SVG exporter 

## Using BS-uml program
- Type the `help` commmand to see a list of possible commands and their use
