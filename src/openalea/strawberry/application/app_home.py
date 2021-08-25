import ipyvuetify as v
from ipywidgets import HTML

container_main = v.Card(elevation="0", children=[
    HTML(""" 
<style>.someclass { color : blue ; }</style>
<html>
<body>
<img style="width:150px;" src="https://raw.githubusercontent.com/openalea/strawberry/master/doc/source/_static/openalea_logo.png">
<img align="right" style="width:100px;" src="https://raw.githubusercontent.com/openalea/strawberry/master/doc/source/_static/logo_strawberry.png">

<h1 style='margin-bottom: 1em; word-break: normal; text-align: center; font-size: 48px'>
Strawberry interactive application
</h1>

<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
The complete documentation of the package can be found on readthedoc as well as
tutorials <a href="https://strawberry.readthedocs.io/en/latest/">here.</a>
</p>

<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
Welcome to the Strawberry interactive application. 
This application is a display of the function proposed in the OpenAlea Strawberry python package.
The source code can be found on Github <a href="https://github.com/openalea/strawberry">here.</a>
</p>

</body>
</html>
""")
               ])
container_main