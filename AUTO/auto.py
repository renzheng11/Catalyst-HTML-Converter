f = open("demo.md", "r")

logo = f.readline()
print(logo)


# f.write("""
#     <html>

# <head>
#     <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
#     <meta content="text/html; charset=UTF-8" http-equiv="content-type">
#     <meta charset="UTF-8">
#     <meta name="description" content="Data Surrogates as Hosts: Politics of Environmental Governance">
#     <meta name="keywords"
#         content="keywords">
#     <meta name="author" content="Author Name">

#     <!--PAGE STYLING-->

#     <!--INCLUDE ALL CSS CLASSES HERE-->

#     <style type="text/css">
#         /* For all hyperlinks */
#         a {
#             color: #000099;
#         }

#         /* CSS class for authorBio*/
#         .authorBio {
#             margin: 0;
#             color: #000000;
#             font-size: 12pt !important;
#             font-family: 'Catamaran', sans-serif !important;
#         }

#         /* CSS class for authorBio*/
#         .authorName {
#             color: #000099;
#             font-size: 13pt;
#             font-family: 'Catamaran', sans-serif;
#         }

#         /* For all normal text */
#         .c1 {
#             color: #000000;
#             font-weight: 400;
#             text-decoration: none;
#             vertical-align: baseline;
#             font-size: 12pt;
#             line-height: 1.6;
#             font-family: 'Catamaran', sans-serif;
#             font-style: normal;
#         }

#         /* For the whole <body> shape */
#         .c5 {
#             background-color: #ffffff;
#             max-width: 600pt;
#             padding: 72pt 72pt 72pt 150pt;
#         }

#         /* For when your quote itself has another quote/dialog */
#         .doubleIndent {
#             font-size: 12pt;
#             position: relative;
#             margin-left: 50px;
#             width: 545px;
#         }

#         .figure {
#             height: Auto;
#             max-width: 100%;
#             position: relative;
#         }

#         /* For image captions */
#         .imagetext {
#             position: relative;
#             padding-top: 10pt;
#             color: dimgray;
#             font-weight: 700;
#             text-decoration: none;
#             vertical-align: baseline;
#             font-size: 10pt;
#             font-family: 'Catamaran', sans-serif;
#             font-style: normal;

#         }

#         /* For list formatting */
#         ol {
#             margin: 0;
#             padding: 0;
#         }

#         /* For list item formatting */
#         li {
#             color: #000000;
#             font-size: 11.5pt;
#             font-family: 'Catamaran', sans-serif;
#         }

#         /*Only used for gap between Catalyst Logo and paper title/type*/
#         .logoGap {

#             padding-top: 18pt;
#             color: #666666;
#             font-size: 24pt;
#             padding-bottom: 4pt;
#             font-family: 'Catamaran', sans-serif;
#             line-height: 1.8909090215509587;
#             page-break-after: avoid;
#             font-style: italic;
#             text-align: left;
#         }

#         .notes {
#             font-size: 12pt;
#             line-height: 1.2;
#         }

#         /*Baseline paragraph formatting*/
#         p {
#             margin: 0;
#             color: #000000;
#             font-size: 12pt;
#             font-family: 'Catamaran', sans-serif;
#         }

#         .paperTitle {
#             font-family: 'Catamaran', sans-serif;
#             font-size: 18pt;
#             color: #000099;
#         }

#         /* CSS class for poem */
#         .poem {
#             font-style: italic;
#             font-size: 11.5pt;
#             font-family: 'Catamaran', sans-serif;
#         }

#         .quotes {
#             font-size: 11.5pt;
#             font-family: 'Catamaran', sans-serif;
#             position: relative;
#             margin-left: 50px;
#             width: 645px;
#             line-height: 1.35;
#         }

#         /*CSS class for references*/
#         .reference {
#             margin: 0;
#             color: #000000;
#             font-size: 11.5pt !important;
#             font-family: 'Catamaran', sans-serif !important;
#             line-height: 1.35 !important;
#             margin-bottom: 11pt;
#         }

#         .sectionTitle {
#             font-size: 17pt;
#         }

#         .subsectionTitle {
#             font-size: 14pt;
#             /* font-weight: bold; */
#         }

#         .sub_subsectionTitle {
#             font-size: 12pt;
#             font-weight: bold;
#         }

#         table td,
#         table th {
#             padding: 0;
#         }


#         /*Making the webpage responsive*/
#         @media only screen and (max-device-width: 480px) {
#             body {
#                 width: 112% !important;
#                 margin-left: 4px;

#             }

#             .logo {
#                 position: relative;
#                 right: 27%;
#                 width: 451px;
#                 height: 164px
#             }

#             .c5 {
#                 max-width: 100%;
#             }

#             .type {
#                 font-size: 33px;
#             }
#         }
#     </style>

#     <!--PAGE STYLING ENDS-->

# </head>

# <body class="c5">
#     <img class="logo" style="width: 377px; height: 105px; position: relative; right:1%; top: 5%; display: block;"
#         alt="Catalyst logo" src="https://drive.google.com/uc?export=view&id=1Y40wZQ6cQZFlrMDNx9n9jECr6xG-gbMK"
#         align="right">

#     <p class="logoGap">&nbsp;</p>
#     <p class="logoGap">&nbsp;</p>


#     <div class="c1"></div>
#     <p class="c1 type">Type / Section</p>

#     <p class="paperTitle">
#         Paper title
#     </p>


#     <p class="c1">&nbsp;</p>
#     <p class="c1">&nbsp;</p>


#     <p class="authorName">
#         Author Name
#     </p>
#     <p class="c1">
#         University name<br>
#         contact email
#     </p>

#     <p class="c1">&nbsp;</p>
#     <p class="c1">&nbsp;</p>

#     <!--Main Body-->
#     <p class="c1 sectionTitle">Abstract</p>
#     <p class="c1">Abstract paragraph</p>

#     <p class="c1">&nbsp;</p>
#     <p class="c1">&nbsp;</p>

#     <p class="c1 sectionTitle">
#         Keywords
#     </p>
#     <p class="c1">
#         governance, critical environmental justice, abstraction, surrogates, hosting, social reproduction
#     </p>


#     <p class="c1">&nbsp;</p>
#     <p class="c1">&nbsp;</p>



#     <p class="c1 sectionTitle">Introduction</p>
#     <p class="c1">
#         Introduction paragraph
#     </p>


#     <p class="c1">&nbsp;</p>
#     <p class="c1 sectionTitle"> Section Title </p>
#     <p class="c1">
#         Paragraph 1 <sup><a href="#note1b" id="note1t">1</a></sup>
#         <br><br>
#         Paragraph 2
#     </p>

#     <p class="c1">&nbsp;</p>
#     <p class="c1 subsectionTitle">
#         Subsection Title
#     </p>
#     <p class="c1">&nbsp;</p>

#     <img src="sivakumarfigure1.png" alt="" style="height: Auto; max-width: 100%;;position: relative;">
#     <p class="c1">&nbsp;</p>
#     <p class="imagetext">Figure 1. Figure description</p>
#     <p class="c1">&nbsp;</p>

#     <p class="c1">&nbsp;</p>
#     <p class="c1 sectionTitle">Conclusion</p>

#     <p class="c1">
#         Conclusion paragraph
#     </p>
#     <p class="c1">&nbsp;</p>

#     <!-- Notes -->
#     <p class="c1">&nbsp;</p>
#     <p class="c1 sectionTitle">Notes
#     </p>
#     <div id="note1b">
#         <p class="notes">
#             <sup><a href="#note1t">1</a></sup> Note 1
#         </p>
#     </div>
#     <p class="notes">&nbsp;</p>

#     <div id="note2b">
#         <p class="notes">
#             <sup><a href="#note2t">2</a></sup> Note 2
#         </p>
#     </div>

#     <!-- References -->
#     <p class="c1">&nbsp;</p>
#     <p class="c1 sectionTitle">References
#     </p>

#     EXPORTED REFERENCES

#     <!--reference END-->

#     <!--Author Bios Start-->
#     <p class="c1">&nbsp;</p>
#     <p class="c1">&nbsp;</p>
#     <p class="c1 sectionTitle">Author Bios</p>

#     </p>
#     <p class="c1">
#         <b>First Last</b> description
#     </p>
#     <p class="c1">&nbsp;</p>

#     <!--Author Bios End-->

# </body>

# </html>
# """)


f.close()