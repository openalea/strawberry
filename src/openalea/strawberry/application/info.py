from ipywidgets import HTML


p1_doc = HTML("""   
                <html>
                <body>

                
                <p style='text-align: justify; font-size: 18px; color: black;'>
                The MTG import tab allows you to import MTG files (tab IMPORT FILES) and to obtain a description of the files (Tab Description files).
                <ul style='text-align: justify; font-size: 16px; color: black;'>
                
                <li> in IMPORT FILES windows:
                    <ul>
                    <li> you can import one or several mtg files from your computer using import file button. </li>
                    <li>Once the files are uploaded, you can select one or some files upload. You could see so a view of your MTG in dataframe </li>
                    <li> Selecting a genotype, a MTG representation of one plant appears. You can so visualize MTG graph for each plant, selecting the plant thanks a slider.</li>
                    </ul>
                <li> In describe files windows, you can find a description of selected files with some informations. </li>
                    <ul>
                    <li> In the first paragraph number of files selected, a names of experimentation, the names of the deferent genotype, the number of plant and the list of properties in the MTG</li>
                    <li> In the second paragraph you can see summary of each properties, when the properties is numeric the variable will be describe by the min, max , mean and quartile values either the a list unique values you will be given </li>
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
                The 2D visualization is a schematic representation of strawberry plant architecture <br>
                This visualization of the plant architecture highlights the sympodial branching as well as the different structures of the plant. This representation makes it possible to highlight apparent axes, distinguishing the main axis (succession of extension crowns deriving from the primary crown) from the branches (succession of extension crowns deriving from a branch crown).
                We proposed you two type of 2D visualizations (if several genotype are present in MTG files, you can select the genotype using genotype button):
                <ul style='text-align: justify; font-size: 18px; color: black;'>
                <li> First visualization (left), allows to visualize one plant, you can select the plant visualized using plant id button. </li>
                <li> A second visualization (right), show the most central individual according to date. The most central plant is calculate using robust standardized distance  based on few global variables (no_total_leaves, no_total_flowers, no_stolons, no_floral_bud, no_inflorescence, no_branch_crown, no_extension_crown, order_max')
                
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
                In plant scale tab you can see all informations proposed on whole plant. This tab contains two windows (Export and Analyses)<br> 
                
                Export windows allows to extract both MTG properties at plant scale in dataframe.
                <br>
                <b>Variables Descriptions:</b>
                <style>
                    table, th, td {
                        border:1px solid black;
                        border-collapse: collapse;
                        text-align: center;
                        vertical-align: middle}
                </style>
                <table style="width:100%">
                <tr>
                    <th>Variable names</th>
                    <th>type</th>
                    <th>description</th>
                </tr>
                <tr>
                    <td>Genotype</td>
                    <td>STRING</td>
                    <td>Genotype name</td>
                </tr>
                <tr>
                    <td>date</td>
                    <td>Date (DD/MM/YYYY)</td>
                    <td>Architectural date</td>
                </tr>
                <tr>
                    <td>modality</td>
                    <td>STRING)</td>
                    <td>Treatment modality (eg: stress /No stress</td>
                </tr>
                <tr>
                    <td>plant</td>
                    <td>INT</td>
                    <td>Plant Id</td>
                </tr>
                <tr>
                    <td>no_visible_leaves</td>
                    <td>INT</td>
                    <td>Number of visible leaves (out of bud) </td>
                </tr>
                <tr>
                    <td>no_foliar_primordia</td>
                    <td>INT</td>
                    <td>Number of leaves in the buds</td>
                </tr>
                <tr>
                    <td>no_total_leaves</td>
                    <td>INT</td>
                    <td>Number of total leaves (visible leaves + foliar primordia)</td>
                </tr>
                <tr>
                    <td>no_open_flowers</td>
                    <td>INT</td>
                    <td>Number of open flowers (flowers with visible petals)</td>
                </tr>
                <tr>
                    <td>no_aborted_flowers</td>
                    <td>INT</td>
                    <td>Number of aborted flowers</td>
                </tr>
                <tr>
                    <td>no_closed_flowers</td>
                    <td>INT</td>
                    <td>Number of closed flowers (flowers with no visible petals)</td>
                </tr>
                <tr>
                    <td>no_total_flowers</td>
                    <td>INT</td>
                    <td>Total number of flowers</td>
                </tr>
                <tr>
                    <td>no_fruits (optional)</td>
                    <td>INT</td>
                    <td>Total number of fruits</td>
                </tr>
                <tr>
                    <td>no_stolons</td>
                    <td>INT</td>
                    <td>Number of stolons</td>
                </tr>
                <tr>
                    <td>no_vegetative_bud</td>
                    <td>INT</td>
                    <td>Number of vegetative buds (Stage 17 to 19, label bt)</td>
                </tr>
                <tr>
                    <td>no_initiated_bud</td>
                    <td>INT</td>
                    <td>Number of initiated bud (Stage A, label bt)</td>
                </tr>
                <tr>
                    <td>no_floral_bud</td>
                    <td>INT</td>
                    <td>Number of floral buds (stage B to I, label ht)</td>
                </tr>
                <tr>
                    <td>no_inflorescences</td>
                    <td>INT</td>
                    <td>Number of inflorescence</td>
                </tr>  
                <tr>
                    <td>no_branch_crown</td>
                    <td>INT</td>
                    <td>number of lateral crown corresponding to branch crowns</td>
                </tr>
                <tr>
                    <td>no_extension_crown</td>
                    <td>INT</td>
                    <td>Number of lateral crowns corresponding to extension crowns</td>
                </tr>
                <tr>
                    <td>no_ramifications</td>
                    <td>INT</td>
                    <td>Total number of lateral crown (Branch + Extension Crowns)</td>
                </tr>
                <tr>
                    <td>order_max</td>
                    <td>INT</td>
                    <td>Maximal order</td>
                </tr>
                <tr>
                    <td>vid</td>
                    <td>INT</td>
                    <td>Vertex identifier in MTG</td>
                </table>
                
                <p style='margin-bottom: 1em; text-align: justify; font-size: 18px; color: black;'>
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
                In module scale tab you can see all informations by module order (rank of axis). This tab contains four windows (Export data and Analyses by genotype, analyses on several genotype and waffle representation)<br> 
                <br> 
                Export windows allows to extract both MTG properties at module scale in dataframe (data group by Genotype, date, modality,order) 
                <br>
                <b>Variables Descriptions:</b>
                <style>
                    table, th, td {
                        border:1px solid black;
                        border-collapse: collapse;
                        text-align: center;
                        vertical-align: middle}
                </style>
                
                <table style="width:100%">
                <tr>
                    <th>Variable names</th>
                    <th>type</th>
                    <th>description</th>
                </tr>
                <tr>
                    <td>Genotype</td>
                    <td>STRING</td>
                    <td>Genotype name</td>
                </tr>
                                <tr>
                    <td>date</td>
                    <td>Date (DD/MM/YYYY)</td>
                    <td>Architectural date</td>
                </tr>
                <tr>
                    <td>modality</td>
                    <td>STRING)</td>
                    <td>Treatment modality (eg: stress /No stress</td>
                </tr>
                <tr>
                    <td>plant</td>
                    <td>INT</td>
                    <td>Plant Id</td>
                </tr>
                <tr>
                    <td>order</td>
                    <td>INT</td>
                    <td>order level, order of the module/axis</td>
                </tr>
                <tr>
                    <td>no_visible_leaves</td>
                    <td>INT</td>
                    <td>Number of visible leaves (out of bud)</td>
                </tr>
                <tr>
                    <td>no_foliar_primordia</td>
                    <td>INT</td>
                    <td>Number of leaves in the buds</td>
                </tr>
                <tr>
                    <td>no_total_leaves</td>
                    <td>INT</td>
                    <td>Number of total leaves (visible leaves + foliar primordia)</td>
                </tr>
                <tr>
                    <td>no_open_flowers</td>
                    <td>INT</td>
                    <td>Number of open flowers (flowers with visible petals)</td>
                </tr>
                <tr>
                    <td>no_aborted_flowers</td>
                    <td>INT</td>
                    <td>Number of aborted flowers</td>
                </tr>
                <tr>
                    <td>no_closed_flowers</td>
                    <td>INT</td>
                    <td>Number of closed flowers (flowers with no visible petals)</td>
                </tr>
                <tr>
                    <td>no_total_flowers</td>
                    <td>INT</td>
                    <td>Total number of flowers</td>
                </tr>
                <tr>
                    <td>no_fruits (optional)</td>
                    <td>INT</td>
                    <td>Total number of fruits</td>
                </tr>
                <tr>
                    <td>no_stolons</td>
                    <td>INT</td>
                    <td>Number of stolons</td>
                </tr>
                    <td>no_vegetative_bud</td>
                    <td>INT</td>
                    <td>Number of vegetative buds (Stage 17 to 19, label bt)</td>
                </tr>
                <tr>
                    <td>no_initiated_bud</td>
                    <td>INT</td>
                    <td>Number of initiated bud (Stage A, label bt)</td>
                </tr>
                <tr>
                    <td>no_floral_bud</td>
                    <td>INT</td>
                    <td>Number of floral buds (stage B to I, label ht)</td>
                </tr>
                <tr>
                    <td>type_of_crown</td>
                    <td>STRING</td>
                    <td>Type of crown (Main crown (1), Extension Crown(2) or Branch Crown (3))</td>
                </tr>
                <tr>
                    <td>crown_status</td>
                    <td>STRING</td>
                    <td>State of crowns (Terminal bud stage vegetative  (1), Terminal bud stage Initiated (2), Terminal bud stage floral (3), Inflorescence (4), Stolon (5), dried/aborted/cutted (-1)</td>
                </tr>
                <tr>
                    <td>stage</td>
                    <td>STRING</td>
                    <td>stage of the terminal bud/Inflorescence(stage 17 to 19, for vegetative bud, stage A for initiated bud, stage B to H, for floral bud, stage I to 89 according to BBCH Scale) </td>
                </tr>
                <tr>
                    <td>complete_module</td>
                    <td>STRING</td>
                    <td>If the module/axis is complet (Terminated by inflorescence) or incomplet (growing) </td>
                </tr>
                </table>
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
                
                Single Genoype  group analysis perfomed genotype by genotype. In this windows you can see 3 analysis<br>
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
                
                Multiple Genoype  grouped analysis perfomed on one or several genotype. In this windows you can see 2 types of analyses on 5 plots.<br> 
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

p4_doc_waffle = HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                
                The waffle plots represents the states of selected variables depending on the module of the plant.
                Each plant is represented on the X axis.
                </p>
                </body>
                </html>
                 """)


p5_doc_extraction = HTML("""
                        <html>
                        <body>
                        <p style='text-align: justify; font-size: 18px; color: black;'>
                        In node scale tab you can see all informations by node rank (rank of phytomer). This tab contains three windows (Data extraction, single genotype analysis and waffle                             analysis. 
                        
                        In this windows data extraction you can see all informations/properties/variables extracted at this scale. Properties signification was details in following table
                        </p>
                        
                        <style>
                            table, th, td {
                            border:1px solid black;
                            border-collapse: collapse;
                            text-align: center;
                            vertical-align: middle}
                        </style>
                        
                        <table style="width:100%">
                        <tr>
                        <th>Variable names</th>
                        <th>type</th>
                        <th>description</th>
                        </tr>
                        <tr>
                        <td>node_id</td>
                        <td>INT</td>
                        <td>Id of the node</td>
                        </tr>
                        <tr>
                        <td>rank</td>
                        <td>INT</td>
                        <td>Node rank</td>
                        </tr>
                        <tr>
                        <td>branching_type</td>
                        <td>STRING</td>
                        <td>Type of branching (1: stolon, 2:vegetative bud, 3: initiated bud, 4: aborted/dried bud, 5: floral bud, 6: branch crown)</td>
                        </tr> 
                        <tr>
                        <td>complete</td>
                        <td>STRING</td>
                        <td>if the module is complete (terminated by an inflorescence, growing is complete or not (incomplete), or other (branching is not considered like a module (eg                                     undeveloped bud or stolon) </td>
                        </tr>
                        <tr>
                        <td>no_modules_branching</td>
                        <td>INT</td>
                        <td>Total number of module on the branch crown</td>
                        </tr>  
                        <tr>
                        <td>no_branch_crown_branching</td>
                        <td>INT</td>
                        <td>number of branch crown on the branch crown</td>
                        </tr>  
                        <tr>
                        <td>no_extension_crown_branching</td>
                        <td>INT</td>
                        <td>number of extension crown on the branch crown</td>
                        </tr> 
                        <tr>
                        <td>branching lenght</td>
                        <td>INT</td>
                        <td>lenght (no. nodes) of the branching, calculate based with the number of visible leaves </td>
                        </tr>
                        <tr>
                        <td>Genotype</td>
                        <td>STRING</td>
                        <td> Genotype name </td>
                        </tr>
                        <tr>
                        <td>order</td>
                        <td>INT</td>
                        <td>Order of the node </td>
                        </tr>
                        <tr>
                        <td>date</td>
                        <td>YYYY/MM/DD</td>
                        <td>Architectural date </td>
                        </tr>
                        <tr>
                        <td>plant</td>
                        <td>INT</td>
                        <td>Plant id</td>
                        </tr>
                        </table>
                        
                        <p style='text-align: justify; font-size: 18px; color: black;'>
                        <b>Note:</b> This dataframe can by exported in .csv using export table button
                        </p>
                        </body>
                        </html>
                        """)

p5_doc_single_genotype = HTML("""
                        <html>
                        <body>
                        <p style='text-align: justify; font-size: 18px; color: black;'>
                        
                        Single Genoype  group analysis perfomed genotype by genotype. 
                        In this windows you can see the distribution of axillary production for order 0: frequency  (first plot), and relative frequency (second plots)<br>
                        </p>
                        
                        </body>
                        </html>
                        """)
p5_doc_waffle = HTML("""
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                
                The waffle plots represents the states of selected variables depending on the node of the plant.
                Each plant is represented on the X axis.
                </p>
                </body>
                </html>
                 """)
