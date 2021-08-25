from ipywidgets import HTML


p1_doc = HTML("""   
                <html>
                <body>
                <p style='text-align: justify; font-size: 18px; color: black;'>
                The MTG import tab allows you to import MTG files (tab IMPORT FILES) and to obtain a description of the files (Tab Description files).
                <ul>
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
                The Visualisation tab provides a 2D (2D visualization windows) and 3D visualisation of the plants (3D visualization windows)
                
                The 2D visualization is a schematic representation of strawberry plant architecture The 2D schematic visualization  of the plant architecture highlights the sympodial branching as well as the different structures of the plant. This representation makes it possible to highlight apparent axes, distinguishing the main axis (succession of extension crowns deriving from the primary crown) from the branches (succession of extension crowns deriving from a branch crown).
                We proposed you two type of 2D visualizations (if several genotype are present in MTG files, you can select the genotype using genotype button):
                <ul>
                <li> First visualization (left), allows to visualize one plant, you can select the plant visualized using plant id button. </li>
                <li> A second visualization (right), show the most central individual according to date. The most central plant is calculate using robust standardized distance  based on few global variables (number of flowers, number of leaves, number of stolons, maximum module order and number of branch and extension crowns)</li> 
                </ul>
                </p>
                </body>
                </html>
                """)

p2_doc_visu3d = "Awsome description o"

p3_doc_extraction = "Awsome description o"

p3_doc_analyses = "Awsome description o"

p4_doc_extraction = "Awsome description o"

p4_doc_single = "Awsome description o"

p4_doc_multiple = "Awsome description o"

p4_doc_waffle = "Awsome description o"

p5_doc_waffle = "Awsome description o"

