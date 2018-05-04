# Notebooks and Rmd for strawberry analysis and visualisation

## Reading and extract data from MTG

MTG_protocol.ipynb

### TODO
- Problem :
    * OK: New common index ok for octoploid,
    * OK : Unable to read the MTG: Nils_2.mtg (test...)

- TODO:
    * Add properties : Computation of some new properties (eg leaflet_area), leaf area or keep manually
    so it necessary to incorporate it into MTG.


## Extract sequence at different scales from MTG

Sequence_Analysis.ipynb or
Sequence Analysis Marc.ipynb, but i prefer because integrate last minor modification

add new variable like petiol lenght, leaf area ect...

## Compute mean individual and plot

Rscripts
Z:\G1\Fraise\Marc-Labadie\R\R-users\FraFlo\Script\Architecture analysis

* 2017_04_27_selection of the most central individual.R, this selection was perform on the extraction of sequence according module non overlapping.
	- [Hint: Selection of the most central individual no generalize i don't know if this funtion is extendible]

* Architecture sequence analysis-scriptpropre.R. This script allows to represent the number of flower, leaves,ect by order and realize linear regression in order to identify from which order we obtain a stationarity of the number of flowers, leave ect.
	- [Hint: Error, Figure representing linear model with confident interval script need to clear the script and review some function]

* [Global Hint: It needed to review all script width new properties (colname) to extract and represented data.
	- Perhaps realized two script one to calculation of most central individual we return only one dataset with individuals (plante.select.csv) in order to incorporate all csv for visualisation.
	-  For the second script, Analysis modify and simplify representation fonction incorporate a new version and functions (function plotmean by order)
	and intergrate new future analysis such as function plotmean by node and new variables (leaf area), return plot according to variables]

## Visualisation 2D, 3D for each genotypes, ...

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

Visualisation.ipynb

