
# Rapport Formation Entrée des données friendlyfruit par Karine et Marie Noelle

## Objectifs

1. Former Marie Noelle et Karine à L'utilisation du MTG (module strawberry) à Marie Noelle et Karine Guy
2. Continuer à développer le module MTG (Strawberry) 
3. Permettre à INVENIO d'analyser les donner d'architecture sur des donnée en routine

Ce documents est un compte rendu des différents problème rencontrer par Karine lors de la formation sur les données Firendly fruit. 
Il permet également à INVENIO d'avoir un appercu de l'utilisation et du potentielle d'utilisation du MTG
Il permet à Marc d'avoir une idée plus précise des attentes d'INVENIO pour l'élaboration des différents script Python et R. 
==> réaliser et adapter les scripts en fonction des attentes d'INVENIO

Cette formation permettra ainsi d'établir un cahier des charges plus précis entre INVENIO, CIRAD & INRA

## Lancer condaPromt

1. Dans conda choisir le répetoire d'installation pour cela:
cd path

path= chemin d'accès example  c:\users\mlabadie\Documents\GitHub\strawberry

2. Activé l'environnement conda (strawberry/ openalea)
taper: conda activate strawberry

3. Taper: python setup.py install

4. Taper jupyter notebook pour afficher le programme (sur internet)
cliquer sur example puis Formation puis Demo strawberry

5. Pour lancer les ligne de commande appuyer sur MAJ + entrée
 

## Mardi 20 juin 2018

* **Erreurs Majeurs  empêchant de charger le MTG**
	-Ligne 815-816-817: mauvaise position du F et/ou il doit manquer un +A
	-Ligne 1073-1074-1075: saut de deux lignes + début de l'axe/coeur en 3ième colonne
	-Ligne 3659-3660-3661: saut de deux lignes + début de l'axe/coeur en 3ième colonne

* **Erreurs Mineurs qui n’empêche pas le programme de charger le jeux de donner, que je faire identifier par le programme et corriger manuellement.** 

*Attention: les erreurs mineur peuvent influencer la visualisation et l'extraction des données donc une mauvaise analyse*

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

1. Actuellement afin d'avoir la structure du plant parfois il est necessaire d'ajouter une feuille (feuille n'est plus présente du à la sénésence). Cependant ils souhaiteraient calculer la surface foliaire qui correspond au feuille réellement présent. 

	=>	S= 1.89*nb_leaves

**C'est pourquoi tous comme la propriété visible/non visible, il serait important de mettre une propriété qui permettrai d'identifier les feuilles réelement présente.**

	=> senecent_leaf = g.property(Absent) if Abscent==T and label==F 

2. Visualisation 3D. 

Mettre en place des argument qui me permette de definir la grille (un argument nombre de modalite et un autre nombre de plant par modalité).

**Objectif est de pouvoir visualiser les plants sur une grille avec une colonne = une modalité et une ligne par plante** 


3. Visualisation 2D

Problème de visualisation je n'arrive pas à visualiser l'ensemble des plantes. 

4. Extraction sous forme de dataframe

    4.1 A l'échelle du plant
    
    Actuellement le dataframe extrait permet de visualiser et calculer l'individu central en fonction du génotype et de la date. 
    Invenio (Karine) aimerai également qu'il puisse tenir en compte d'une modalité par exemple dans le projet friendly fruit l'origine du plant. 
    
    * Prévoir dans le MTG, dans la sortie du dataframe une variable LA et LAI qui se calculerai seul en fonction des données rentrées
        - LA= 1.89+(2.145*Hauteur Lobe central* Hauteur Lobe Gauche)
        - LAI = LA* nombre de feuille Total
    
    * Dans le extraction des dataframe prévoire un argument qui permet de modalité =T ou F et extraire également la l'information modalité en plus de la variétés.
    * Afficher dans le dataframe l'ensemble des variables mesurer.
    * Prévoir également dans le calcul de l'individu centrale  la possibilité de choisir la modalité (par exemple modality =T or False ou modalite== "Origin"
    * Permettre aux utilisateurs de choisir les variables pour le calcule de l'individu centrale actuellement, l'individu centrale est calculer sur des variable de comptage. Cependant il est possible que Invenio souhaite calculer l'individu centrale sur d'autres variables tel que la surface foliaire (LA), ou la surface foliaire rapporter au sol (LAI). 
    
    
    4.2 A l'echelle du module
    
    Actuellement il n'y a pas d'extraction sous forme de dataframe à l'echelle du module. 
    Il serait important pour Invenio et Karine d'avoir ce type d'extraction. 
    
    **Objectif est de pouvoir voir une certain nombre de variable en fonction du rang du module est de pouvoir les annalyser par la suite**
   
## Mercredi 1 Aout 2018

**Marc:** J'ai fait des modifications afin de répondre à certaine attentes des centres experimentaux (INVENIO, CIREF), que je présentaterai à Karine lors de notre future journée de formation prévu le vendredi 3 Aouts. 

* Dataframe extraction on plant scale:
	- Extration du dataframe à l'échelle ainsi que le l'extation de l'individu centrale prends en compte la Modalité (pour le moment une seul modalité est possible).
	La fonction extraction à l'echelle du plant revoie desormais le genotype/variété, la date, la modalité, le numéros du plant ainsi que les variable de comptage: nombre de feuilles , fleurs et stolons totale, l'ordre maximum ainsi que le nombre de ramification total. Il donne egalement le Vid (Numéros d'indexation du plant convertie en MTG)

	- Idem pour le calcul de l'individu centrale, le calcul de l'individu central tiens desormais en compte le modalité. le calcule de l'individu central ce fait desormais en fonction de ces trois paramètre globaux (groupby en fonction de des paramètres globaux). Le calcul se fait cependant toujours sur le nombre de feuilles, fleurs, stolon, ordre maximum et nombre de ramification. 

[**HINT:** Puisque le calcul se fait également sur la modalité il est donc necessaire au MTG d'ajouter et surtout de remplir la colonne modality par une valeur, si pas de modalité mettre A dans la case correspondante ou une autre valeur qui est identique pour chaque plante sinon le calcul ne marchera pas, en tout cas pour le moment. 
Attention les modalités sont considérer comme des STRING (FACTEUR), donc ne pas mettre de variable quantitative]

## Jeudi 2 Aout 2018

Autres modification approter par marc

* Pour la visualisation 3D:
	- J'ai ajouté un paramêtre qui me permet de donner le nombre de plante par modalité. Ce paramêtre permet ainsi de visualiser sur la grille l'ensemble des plantes avec une colonne par modalité. Attention, c'est un peu du bricolage donc pour que cela marche il faut le même nombre de plante par modalité sinon il risque (c'est même sur) d'y avoir un décalage. **PENSER A REDEFINIR LA FONCTION POUR QUE LA GRILLE SE FASSE EN FONCTION DU NOMBRE DE PLANTE ET DU NOMBRE DE MODALITE** 


* Ceux qui reste à faire:
	- Visualisation 3D:
		- Mettre un argument pour permettre de basculer d'une visualisation avec feuille à une visualisation sans feuille (without_leaf= True or False)	
	
	- Extraction sous forme de dataframe à l'échelle du module. 
		Il souhaite dans le dataframe extraire toute les variables à l'echelle du module. 

* Sur le MTG:
	- Calculer la propriété Leaf Area et Leaf Area Index
 		- LA= 1.89+(2.145*Hauteur Lobe central* Hauteur Lobe Gauche)
        - LAI = LA* nombre de feuille Total

## Vendredi 3 Aout

Deroulement de la session: 
Nous avons vu avec Karine les nouvelle amélioration du script 
Nous avons revu comment entrer les données en mtg. avec le nouveau template et rentrée quelque données Projet FriendlyFruit_Variete

je vais voir comment entre les données plus facilement. 


[**Hint**: A voir si on le fait sur Python ou sur R]
Demande de Karine:
	- extraire un dataframe avec la moyenne et ecart type de du génotype et de la modalité de toute les propriétés. 

	-représentation de chaque stade par niveau (nombre de bourdeons pour chaque stade)
		- uniquement les les axes visible se terminant par un BT

## Vendredi 10 aout

Faire la fonction pour extraire les données en excel (les tableaux)
Visualisation 3D argument pour augmenter la distance entre les plants aussi bien en ligne que en colonne
Faire une representation du plant médian en 3D
Faire une visualisation des plant moyen à la place des plant moyens. 
