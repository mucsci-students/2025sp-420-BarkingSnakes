
BS-uml> new diagram
Failed: file should be a .json extension.
BS-uml> new <diagram>
Failed: file should be a .json extension.
BS-uml> load
BS-uml> Enter project file name j
Invalid file: Use command: new <filename.json> to make a new file,                     
 or command: load <filename.json> to load a file that exists                     
 in current folder, or specify subfolder with <filepath/filename.json>
BS-uml> new <diagram1.json>                           
BS-uml> edit
Invalid command: edit.  Use command 'help' for a list of valid commands.
BS-uml> list
No classes to display.
BS-uml> add myclass
No active class selection. Use command: class <class name> to select a class.
BS-uml> list
No classes to display.
BS-uml> add
No active class selection. Use command: class <class name> to select a class.
BS-uml> class
BS-uml> Enter class name class1
BS-uml[class1]> add
BS-uml[class1]> 2
Invalid command: 2.  Use command 'help' for a list of valid commands.
BS-uml[class1]> attribute add
Invalid command: attribute add.  Use command 'help' for a list of valid commands.
BS-uml[class1]> attribute add att1
BS-uml[class1]> list
+--------+
|class1 |
+--------+
|-att1  |
+--------+
BS-uml[class1]> atribute add att2
Invalid command: atribute add att2.  Use command 'help' for a list of valid commands.
BS-uml[class1]> attribute add att2
BS-uml[class1]> list
+--------+
|class1 |
+--------+
|-att1  |
|-att2  |
+--------+
BS-uml[class1]> back
BS-uml> list
Displaying 1 classes.
+--------+
|class1 |
+--------+
|-att1  |
|-att2  |
+--------+
BS-uml> class
BS-uml> Enter class name class2
BS-uml[class2]> attribute add att3
BS-uml[class2]> attribue add att4
Invalid command: attribue add att4.  Use command 'help' for a list of valid commands.
BS-uml[class2]> attribute add att4
BS-uml[class2]> list
+--------+
|class2 |
+--------+
|-att3  |
|-att4  |
+--------+
BS-uml[class2]> back
BS-uml> list
Displaying 1 classes.
+--------+
|class1 |
+--------+
|-att1  |
|-att2  |
+--------+
BS-uml> class
BS-uml> Enter class name class2
BS-uml[class2]> list
+--------+
|class2 |
+--------+
+--------+
BS-uml[class2]> attribute add att5
BS-uml[class2]> list
+--------+
|class2 |
+--------+
|-att5  |
+--------+
BS-uml[class2]> back
BS-uml> list
Displaying 1 classes.
+--------+
|class1 |
+--------+
|-att1  |
|-att2  |
+--------+
BS-uml> relation add class1 class2
Operation failed:UML Error:NoSuchObjectError
BS-uml> class
BS-uml> Enter class name class2
BS-uml[class2]> list
+--------+
|class2 |
+--------+
+--------+
BS-uml[class2]> attribute add att6
BS-uml[class2]> save
BS-uml[class2]> list
+--------+
|class2 |
+--------+
|-att6  |
+--------+
BS-uml[class2]> back
BS-uml> list
Displaying 1 classes.
+--------+
|class1 |
+--------+
|-att1  |
|-att2  |
+--------+
BS-uml> class
BS-uml> Enter class name class1
BS-uml[class1]> attribute add thisisanattribute
BS-uml[class1]> list
+-------------------+
|class1            |
+-------------------+
|-att1              |
|-att2              |
|-thisisanattribute |
+-------------------+
BS-uml[class1]> back
BS-uml> list
Displaying 1 classes.
+-------------------+
|class1            |
+-------------------+
|-att1              |
|-att2              |
|-thisisanattribute |
+-------------------+
BS-uml> class
BS-uml> Enter class name class2
BS-uml[class2]> attribute add attribute-here
BS-uml[class2]> list
+----------------+
|class2        |
+----------------+
|-attribute-here |
+----------------+
BS-uml[class2]> attribute add attri7
BS-uml[class2]> list
+----------------+
|class2        |
+----------------+
|-attribute-here |
|-attri7        |
+----------------+
BS-uml[class2]> save
BS-uml[class2]> back
BS-uml> list
Displaying 1 classes.
+-------------------+
|class1            |
+-------------------+
|-att1              |
|-att2              |
|-thisisanattribute |
+-------------------+
BS-uml> quit
BS-uml> load
BS-uml> Enter project file name <diagram1.json>
BS-uml> list
Displaying 1 classes.
+-------------------+
|class1            |
+-------------------+
|-att1              |
|-att2              |
|-thisisanattribute |
+-------------------+
BS-uml> quit


BS-uml> load
BS-uml> Enter project file name <diagram1.json>
BS-uml> list
Displaying 1 classes.
+-------------------+
|class1            |
+-------------------+
|-att1              |
|-att2              |
|-thisisanattribute |
+-------------------+
BS-uml> quit


