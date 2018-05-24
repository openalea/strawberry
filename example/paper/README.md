# Notebooks and Rmd for strawberry analysis and visualisation

## Reading and extract data from MTG
- New information: In order to import and read MTG, I (Marc) Create a new ipynb name: 0-MTG Reader.ipynb 
This script features importing MTG diploid data and octoploids made the last time in XXX.
to which I added a function to realize a big_mtg (union of all the mtg octoploids) to allow a meta-analysis.

[Hint: So I think we will be able after verification clear the notebook XXX]

1_MTG_protocol.ipynb

### TODO
- Problem :
    * OK: New common index ok for octoploid,
    * OK : Unable to read the MTG: Nils_2.mtg (test...)

- TODO:
    * Add properties : Computation of some new properties (eg leaflet_area), leaf area or keep manually
    so it necessary to incorporate it into MTG.


## Extract sequence at different scales from MTG

2_Sequence_Analysis.ipynb 

add new variable like petiol lenght, leaf area ect...

## Compute mean individual and plot

Rscripts
Z:\G1\Fraise\Marc-Labadie\R\R-users\FraFlo\Script\Architecture analysis

*mean_plant_selection_170427.R, this selection was perform on the extraction of sequence according module non overlapping.
	- [Hint: Selection of the most central individual no generalize i don't know if this funtion is extendible]

* Architecture sequence analysis-scriptpropre.R. This script allows to represent the number of flower, leaves,ect by order and realize linear regression in order to identify from which order we obtain a stationarity of the number of flowers, leave ect.
	- [Hint: Error, Figure representing linear model with confident interval script need to clear the script and review some function]

* [Global Hint: It needed to review all script width new properties (colname) to extract and represented data.
	- Perhaps realized two script one to calculation of most central individual we return only one dataset with individuals (plante.select.csv) in order to incorporate all csv for visualisation.
	-  For the second script, Analysis modify and simplify representation fonction incorporate a new version and functions (function plotmean by order)
	and intergrate new future analysis such as function plotmean by node and new variables (leaf area), return plot according to variables]

## Visualisation 2D, 3D for each genotypes, ...

3_Visualisation.ipynb

* 2D: create a module
	- incorporate cotyledons, unifoliate and trifoliate leaves.
	- Two types of visualization short vizualisation (show only visible organs) and deploy vizualisation (shows all organ, even the organs contained in the buds (organ primordium))
	- Include in the vizualisation text function to plot Number of flower or opened flower in inflorescence.
        Which property?
	- To discuss if we integrate petiol lenght (PETLG) and leaf area properties and eventually internod lenght property

* 3D : test on previous and new MTGs

	- include new properties
		- for generalization diploid and octoploid incorporation of cotyledon and unifoliate rules
		- if possible incorporation of properties in the visualisation petiol lenght, area, ect


