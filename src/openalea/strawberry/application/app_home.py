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
tutorials <a href="https://strawberry.readthedocs.io/en/latest/" onclick="window.open(this.href); return false;">here.</a>
</p>

<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
Welcome to the Strawberry interactive application. 
This application is a display of the function proposed in the OpenAlea Strawberry python package.
The source code can be found on Github <a href="https://github.com/openalea/strawberry" onclick="window.open(this.href); return false;">here.</a>
</p>
<style>
    table, th, td {
        border:1px solid black;
        border-collapse: collapse;
        text-align: center;
        vertical-align: middle}
</style>
<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
Currently the application use mtg data format (.mtg). Characteristic of MTG format and minimal properties require was details above
</p>
<h2> Data Format mtg file</h2>
<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
You can find an example of an mtg file <a href="https://raw.githubusercontent.com/openalea/strawberry/master/share/data/Gariguette.mtg" onclick="window.open(this.href); return false;">here.</a>
</p>
<br>
<h3> Specificity of Multiscale Tree Graph</h2>
<br>

<table style="width:100%">
<tr>
    <th>Symbol </th>
    <th>Botanical entity </th>
    <th>Scale (scale level)</th>
    <th>associated propeties</th>
</tr>
<tr>
    <td>P</td>
    <td>Plant</td>
    <td>Plant scale (1)</td>
    <td>Experimental name, Genotype, Plant id, Sample date, Architectural date, Modality </td>
</tr>
<tr>
    <td>T</td>
    <td>Main crown (stem)</td>
    <td>Axis scale (2)</td>
    <td>Diameter (DBI)</td>
</tr>
<tr>
    <td>A</td>
    <td>Lateral crown (lateral stem: Branch or extension crowns)</td>
    <td>Axis scale (2)</td>
    <td></td>
</tr>
<tr>
    <td>F</td>
    <td>Leaf</td>
    <td>Organ (3)</td>
    <td>Petiol lenght (PETLG), Right leaflet lenght (LFTLG_RIGHT), Central leaflet lenght (LFTLG_CENTRAL), Left leaflet lenght (LFTLG_LEFT), Right leaflet width (LFTWD_RIGHT), Central leaflet width (LFTWD_CENTRAL), left leaflet width (LFTWD_LEFT), Right leaflet area (LFTAR_RIGHT),Central leaflet area (LFTAR_CENTRAL),Right leaflet area (LFTAR_LEFT), total leaf area (LFAR)</td>
</tr>
<tr>
    <td>f</td>
    <td>Leaf primordium (in the bud)</td>
    <td>Organ (3)</td>
    <td></td>
</tr>
<tr>
    <td>bt</td>
    <td>Bud</td>
    <td>Organ (3)</td>
    <td> meristem stage from 17 (vegetative) to A (initiated)</td>
</tr> 
<tr>
    <td>s</td>
    <td>Stolon</td>
    <td>Organ (3)</td>
    <td></td>
</tr>  
<tr>
    <td>HT</td>
    <td>Inflorescence</td>
    <td>Organ (3)</td>
    <td>stage from I to 89 (BBCH scale), no. total flowers (FLWRNUMBER), no. open flowers (FLWRNUMBER_OPEN),<br> no. closed flowers (FLWRNUMBER_CLOSED), no. aborted flowers (FLWRNUMBER_ABORTED), no. fruits</td>
</tr>
    <td>ht</td>
    <td>inflorescence priomdium</td>
    <td>Organ (3)</td>
    <td>stage from B to H</td>
</tr>
</table>
<br>
<h3> Description of features/properties</h3>
<table style="width:100%">
<tr>
    <th>Features name</th>
    <th>type</th>
    <th>description</th>
</tr>
<tr>
    <td>Experiment_name</td>
    <td>STRING</td>
    <td>Experimental name</td>
</tr>
<tr>
    <td>Sample_date</td>
    <td>Date (DD/MM/YYYY)</td>
    <td>Date of sampling</td>
</tr>
<tr>
    <td>Architecture_date</td>
    <td>Date (DD/MM/YYYY)</td>
    <td>Architectural date</td>
</tr>
<tr>
    <td>Genotype</td>
    <td>STRING</td>
    <td>Genotype name</td>
</tr>
<tr>
    <td>Modality</td>
    <td>STRING</td>
    <td>modality of treatement</td>
</tr>
<tr>
    <td>Plant_ID</td>
    <td>INT</td>
    <td>id of the plant</td>
</tr>
<tr>
    <td>Stade</td>
    <td>STRING</td>
    <td>Stade of development</td>
</tr>
<tr>
    <td>DBI (optional)</td>
    <td>REAL</td>
    <td>Collar diameter</td>
</tr>
<tr>
    <td>INFLOLG (optional)</td>
    <td>REAL</td>
    <td>inflorescence length</td>
</tr>
<tr>
    <td>PETLG (optional)</td>
    <td>REAL</td>
    <td>petiole lenght (mm)</td>
</tr>
<tr>
    <td>LFTLG_RIGHT (optional)</td>
    <td>REAL</td>
    <td>Right leaflet length (mm)</td>
</tr>
<tr>
    <td>LFTLG_CENTRAL (optional)</td>
    <td>REAL</td>
    <td>Central leaflet length (mm)</td>
</tr>
<tr>
    <td>LFTLG_LEFT (optional)</td>
    <td>REAL</td>
    <td>left leaflet length (mm)</td>
</tr>
<tr>
    <td>LFTWD_RIGHT (optional)</td>
    <td>REAL</td>
    <td>right leaflet width (mm)</td>
</tr>
<tr>
    <td>LFTWD_CENTRAL (optional)</td>
    <td>REAL</td>
    <td>Central leaflet width (mm)</td>
</tr>
<tr>
    <td>LFTWD_LEFT (optional)</td>
    <td>REAL</td>
    <td>Left leaflet width (mm)</td>
</tr>
<tr>
    <td>LFTAR_RIGHT (optional)</td>
    <td>REAL</td>
    <td>Right leaflet area (mm²)</td>
</tr>  
<tr>
    <td>LFTAR_CENTRAL (optional)</td>
    <td>REAL</td>
    <td>Central leaflet area (mm²)</td>
</tr>
<tr>
    <td>LFTAR_LEFT (optional)</td>
    <td>REAL</td>
    <td>Left leaflet area (mm²)</td>
</tr>
<tr>
    <td>LFAR (optional)</td>
    <td>REAL</td>
    <td>Total leaf area (mm²)</td>
</tr>
<tr>
    <td>FLWRNUMBER</td>
    <td>INT</td>
    <td>Total no. flowers</td>
</tr>
    <tr>
    <td>FLWRNUMBER_OPEN</td>
    <td>INT</td>
    <td>no. opened flowers</td>
</tr>
<tr>
    <td>FLWRNUMBER_ABORTED (optional)</td>
    <td>INT</td>
    <td>no. aborted flowers</td>
</tr>
<tr>
    <td>FLWRNUMBER_CLOSED (optional)</td>
    <td>INT</td>
    <td>no. closed flowers</td>
</tr>
<tr>
    <td>no_fruits (optional)</td>
    <td>INT</td>
    <td>no. fruits</td>
</tr>
</table>
<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
NB:STRING: character type, Date: date type, INT: integer number, REAL: real number
</p>
 
<p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: #FFA500;'>
<b>Warning:</b> If the names of the optional variables are filled in, they will automatically be filled in with zero when the data is extracted.
</p>

</body>
</html>
""")
               ])
container_main