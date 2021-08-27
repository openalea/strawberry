from ipywidgets import HTML


p1_doc = HTML("""   
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                The MTG import tab allows you to import MTG files (tab IMPORT FILES) and to obtain a description of the files (Tab Description files).
                <ul style='text-align: justify; font-size: 16px; color: black;'>
                <li>In IMPORT FILES windows:</li>
                    <ul>
                    <li> you can import one or several mtg files from your computer using import file button. </li>
                    <li> Une fois les fichiers charger, you can select one or some files upload. You could see so a view of your MTG in dataframe </li>
                    <li> Selecting a genotype, a MTG representation of one plant appears. You can so visualize MTG graph for each plant, selecting the plant thanks a slider.</li>
                    </ul>
                <li> In describe files windows, you can find a description of selected files with some informations. </li>
                    <ul>
                    <li> In the first paragraph number of files selected, a names of experiementation, the names of the deferent genotype, the number of plant and the list of properties in the MTG</li>
                    <li> In the second paragraph you found summary of each properties, when the properties is numeric the variable will be describe by the min, max , mean and quartile values either the a list unique values you will be given </li>
                    </ul>
                </ul>
                </p>
                </body>
                </html>
                """)

p2_doc_visu2d = HTML("""   
                <html>

                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                The Visualisation tab provides a 2D (2D visualization windows) and 3D visualisation of the plants (3D visualization windows)<br>
                <br>
                The 2D visualization is a schematic representation of strawberry plant architecture The 2D schematic visualization  of the plant architecture highlights the sympodial branching as well as the different structures of the plant. This representation makes it possible to highlight apparent axes, distinguishing the main axis (succession of extension crowns deriving from the primary crown) from the branches (succession of extension crowns deriving from a branch crown).
                We proposed you two type of 2D visualizations (if several genotype are present in MTG files, you can select the genotype using genotype button):
                <ul style='text-align: justify; font-size: 18px; color: black;'>
                <li> First visualization (left), allows to visualize one plant, you can select the plant visualized using plant id button. </li>
                <li> A second visualization (right), show the most central individual according to date. The most central plant is calculate using robust standardized distance  based on few global variables (number of flowers, number of leaves, number of stolons, maximum module order and number of branch and extension crowns)
                
                <math>
                d<sub>i</sub> = (&sum;<sub>j</sub>&nbsp;
                |X<sub>i,j</sub>-<u style='text-decoration: overline;'>X</u><sub>j</sub>|)&nbsp/&nbsp(mad<sub>j</sub>) 
                where mad<sub>j</sub>= &sum;<sub>j</sub>&nbsp;
                |X<sub>i,j</sub>-<u style='text-decoration: overline;'>X</u><sub>j</sub>| is the mean absolute deviation from the median <u style='text-decoration: overline;'>X</u><sub>j</sub> for the variable j 
                </math>
                
                </li> 
                </ul>
                </p>
                </body>
                </html>
                """)

p2_doc_visu3d = HTML("""   
                <html>

                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                
                3D visualization is a realistic representation of the canopy.<br> 
                It highlights the 3D spatial organisation of the plant, including phyllotaxy.It represents the set of plants architected (y-axis) for succesive dates of observation (x-axis).<br>
                In this windows, two 3D visualization are proposed.  
                <ul style='text-align: justify; font-size: 18px; color: black;'>
                <li> First visualization  (left) shows vegetative development represented using occurence of module order throught a colour scale based on module order.</li> 
                <li> Second visualization (rigth) shows the timing and intensity of flowering indicated by modulating the size and shape of the light blue boxes representing 
                the inflorescences. </li>
                In both representation, axillary buds were represented by coloured spheres or cubes according to their axillary meristem stage
                </p>
                </body>
                </html>
                """)

p3_doc_extraction = HTML("""   
                <html>

                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                In plant scale tab you found all informations proposed on whole plant. This tab contains two windows (Export and Analyses)<br> 
                
                Export windows allows to extract both MTG properties at plant scale in dataframe such as 
                (Genotype, date,modality of experiment, plant, nb_total_leaves, nb_total_flowers, nb_stolons, nb_visible_leaves, nb_vegetative_bud, nb_initiated_bud, 
                nb_floral_bud, nb_inflorescence, leaf_area, order_max, nb_ramifications).<br>
                For this, you can select one or several genotype thanks genotypes button. This dataframe can by exported in .csv using export table button
                </p>
                </body>
                </html>
                """)

p3_doc_analyses = HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                 Analyses windows offers you different graphicales representation of data for one genotype, a line plot and a pie chartdatetime A combination of a date and a time.<br>
                 For one genotype (select using button genotype).
                 <ul style='text-align: justify; font-size: 16px; color: black;'>
                 <li> The line plot: for each variable selected (using select variable button) and one date. A line plot show the evolution of this variable along times.</li>
                 <li> A pie chart represent only the stage proportion (%) of terminal bud/Inflorescence at given date (selected using date select) by genotype.</li>
                 </ul>
                </p>
                </body>
                </html>
                 """)

p4_doc_extraction = HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                In module scale tab you found all informations by module order (rank of axis). This tab contains four windows (Export data and Analyses by genotype, analyses on several genotype and waffle representation)<br> 
                <br> 
                Export windows allows to extract both MTG properties at module scale in dataframe (data group by Genotype, date, modality,order) such as 
                (Genotype, date, modality, plant,order,nb_visible_leaves,nb_foliar_primordia,nb_total_leaves, nb_open_flowers, nb_aborted_flowers, nb_vegetative_bud, nb_initiated_bud, nb_floral_bud, nb_stolons, type_of_crown, crown_status, complete_module, stage).<br>
                <br>
                For this, you can select one or several genotype thanks genotypes button. <br>
                This dataframe can by exported in .csv using export table button

                </p>
                </body>
                </html>
                 """)

p4_doc_single =  HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                
                Single Genoype  group analysis perfomed genotype by genotype. In this windows you found 3 analysis<br>
                the occurence of successive module order,<br>
                the relative frequency of incomplete vs complete module by order and<br>
                the relative frequency of incomplete vs complete module by date
                <ul style='text-align: justify; font-size: 16px; color: black;'>
                <li> The occurence of successive module order shows the cumulative frequence distribution 
                of the highest module order for the successive date of observation. 
                This graph can be read in this way, a module order can be considered really appeared on the population 
                when the lineplot cross for the first time the a probability of 0.9</li>
                <li> The relative frequency of complete and incomplete module by module order shows 
                the proportion of incomplet module (module not terminated by an inflorescence) and complete module (module termiated by inflorescence) for each module. </li>
                They exprime so by module order the proportion of module that was not complete developped or continue their growth </li>
                <li> The relative frequency of complete and incomplete module by date shows the proportion along time of the development module of the genotype. </li>
                They allows to knows if the plant are completely developped or not</li><br>

                Note: that for each figure is possible to extrat dataframe in csv which are permit to realized the plot using export table 

                </p>
                </body>
                </html>
                 """)

p4_doc_multiple = HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                
                Multiple Genoype  grouped analysis perfomed on one or several genotype. In this windows you found 2 types of analyses on 5 plots.<br> 
                Pointwise mean and their standard deviation of number of leave, flowers and stolon by genotype according to module order (plot 1 to 3) and the relative frequency of the branch crown and extenstion crown.
                
                <ul style='text-align: justify; font-size: 16px; color: black;'>
                <li> Pointwise mean plot allows to show the mean number leaves, flowers and stolon along the orders 
                when the lineplot cross for the first time the a probability of 0.9</li>
                <li> relative frequency allows to shows the repartition of branch crown and extension crown for each module orders</li>

                Note: that for each figure is possible to extrat dataframe in csv which are permit to relize the plot using export table 
                </p>
                </body>
                </html>
                 """)

p4_doc_waffle = "Awsome description o"

p5_doc_waffle = "Awsome description o"

