# BS-uml
## 2025sp-420-BarkingSnakes 
## Contributors
- Evan Magill
- John Hershey
- Kyle Kalbach
- Steven Barnes

## Windows Installation Instructions
1. Install python3 a version >= 3.9 if not present https://www.geeksforgeeks.org/how-to-install-python-on-windows/
2. Install a python virtual environment with `python -m venv venv`
3. Activate the virtual environment with `.\venv\scripts\activate`
4. Install required packages with `pip install -r requirements.txt`

## Linux Installation Instructions
1. Install python3 a version >= 3.9 if not present https://www.geeksforgeeks.org/how-to-install-python-on-linux/
2. Install pip use `apt install python3-pip`
3. Install a python virtual environment use `virtualenv venv venv`
4. To Activate the virtual environment use `./venv/bin/activate`
5. Install required packages using `pip install -r requirements.txt`
6. To deactivate virtual environment type `deactivate`
7. To run the uml program ``

## Running the program
   Windows:`python3 src\uml.py`
   Linux:`python3 src/uml.py`

## Running tests
- Use for specific test 
   Windows: `pytest <tests\test_testname>` 
   Linux: `pytest <tests/test_testname>`
- Use to run all tests `pytest`
- Current available test names 
  test_attributeObj.py
  test_classObj.py
  test_save_load.py
  test_user_input.py

## Using BS-uml program
- Type the `help` commmand to see a list of possible commands and their use