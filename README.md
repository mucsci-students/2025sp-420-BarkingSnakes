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
Interact with the web-based interface by navigating to the URL provided when the Flask server starts. Use the toolbar, menus, and on-screen instructions to manage your class diagrams.

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

## Using BS-uml program
- Type the `help` commmand to see a list of possible commands and their use
