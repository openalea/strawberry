
# Rapport Formation Entrée des données friendlyfruit par Karine et Marie Noelle

## Lancer condaPromt

1. Dans conda choisir le répetoire d'installation pour cela:cd path

path= chemin d'accès example c:\users\mlabadie\Documents\GitHub\strawberry

2. Activé l'environnement conda (strawberry/ openalea)
taper: conda activate strawberry

3. Taper: python setup.py install

4. Taper jupyter notebook pour afficher le programme (sur internet)
cliquer sur example puis Formation puis Demo strawberry

5. Pour lancer les ligne de commande appuyer sur MAJ + entrée
 

## Mardi 20 juin 2018

​​* **Erreurs Majeurs  empêchant de charger le MTG**
​​	-Ligne 815-816-817: mauvaise position du F et/ou il doit manquer un +A
	-Ligne 1073-1074-1075: saut de deux lignes + début de l'axe/coeur en 3ième colonne
	-Ligne 3659-3660-3661: saut de deux lignes + début de l'axe/coeur en 3ième colonne
​​
​* **Erreurs Mineurs qui n’empêche pas le programme de charger le jeux de donner, que je faire identifier par le programme et corriger manuellement.** 

​​*Attention: les erreurs mineur peuvent influencer la visualisation et l'extraction des données donc une mauvaise analyse*

	-Lignes 198, 203, 210, 220-223, 235, 392,675, 682, 687, 964, 1766, 2361, 2509, 2726, 2744: erreur de signe dans la majorité des cas il faut remplacer le "/" par "<"
	-Ligne 3342, un axe ne peux se terminer par un F, il faut obligatoirement qu'il se termine par un bt, ht ou HT. 

## Mercredi 21 juin 2018

Chargement du friendlyfruit.mtg dans Openalea. 

* **Erreur identifié par le programme**

"ERROR ^<F(_line=4178)
ERROR ^/F(_line=4585)
ERROR ^/F(_line=4591)
replace all the date format by -
Args  CUT of vertex  186 of type  INFLOLG is not of type  <type 'float'>
Args  A of vertex  512 of type  Plant_ID is not of type  <type 'int'>
Args  E of vertex  509 of type  Plant_ID is not of type  <type 'int'>
Args  4177) of vertex  4116 of type  _line is not of type  <type 'int'>
Args  4584) of vertex  4523 of type  _line is not of type  <type 'int'>
Args  4590) of vertex  4527 of type  _line is not of type  <type 'int'>
ERROR: Missing component for vertex 24
ERROR: Missing component for vertex 337
ERROR: Missing component for vertex 617
ERROR: Missing component for vertex 618
ERROR: Missing component for vertex 1402
ERROR: Missing component for vertex 1403
ERROR: Missing component for vertex 1430
ERROR: Missing component for vertex 1431
ERROR: Missing component for vertex 1437
ERROR: Missing component for vertex 1438
ERROR: Missing component for vertex 2080
ERROR: Missing component for vertex 2081
ERROR: Missing component for vertex 2082
ERROR: Missing component for vertex 2640
ERROR: Missing component for vertex 2641
ERROR: Missing component for vertex 2643
ERROR: Missing component for vertex 2644
ERROR: Missing component for vertex 4497
ERROR: Missing component for vertex 4498_"


**Remarque**:
============= 
* les erreurs identifié par "ERROR ^<F(_line=4178)_ sont des erreurs très importante qui sont principalement du a une erreur dans l'encodage du MTG (erreur de colonne ou de edge_type "/" ou "<"). Il est donc necessaire de reprendre le fichier manuellement à la ligne indiqué et bien évidement de la corriger. 

* erreur de type Args signifie que la propriété est mal placé
Ce type d'erreur renvoi la propriété ainsi que le vertex auquel se situe l'erreur

	Par exemple: Args  CUT of vertex  186 of type  INFLOLG is not of type  <type 'float'>
	signifie que dans la colonne INFLOLG il y a un CUT au vertex 186 alors que la propriétés INFLOLG doit être necessairement une variable REAL comme déclaré dans le fichier d'entête du mtg. 

	**Note:**
	=========
	Pour ce type d'erreur vous pouvez dans une autre cellule taper goct[vertex] c.a.d goct[186] est regarder la description au niveau
	_line_ qui vous donnera le numéros de la ligne correspondante dans votre fichier

* les erreurs de type ERROR: Missing component for vertex 4498, indique qu'il manque un composant donc soit il n'arrive pas à le lire soit il manque quelque chose 

### TODO:

**Demande de la part d'Invenio (Karine Guy)**
=============================================
Actuellement afin d'avoir la structure du plant parfois il est necessaire d'ajouter une feuille (feuille n'est plus présente du à la sénésence). Cependant ils souhaiteraient calculer la surface foliaire qui correspond au feuille réellement présent. 

	=>	S= 1.89*nb_leaves

C'est pourquoi tous comme la propriété visible/non visible, il serait important de mettre une propriété qui permettrai d'identifier les feuilles réelement présente.

	=> senecent_leaf = g.property(Absent) if Abscent==T and label==F 



