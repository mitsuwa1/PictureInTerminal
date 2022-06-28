# PictureInTerminal
Python-module for displaying an image in terminal.

## Usage

Install required packages
```
pip install -r .\PictureInTerminal\requirments.txt
```

Import the module
```
from PictureInTerminal.main import Draw
```

Draw an image
```
Draw(path="example.png")
```

In some cases you'd better use a negative mode. <br>
It reverses light and dark colors.              <br>
For this you should call the Draw() function with "negative" argument passed.
```
Draw(path="example.png", netagive=True)
```
