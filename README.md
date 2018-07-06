# SATD2018
CAPITA project by Mark Frenken on SATD.

## How to use
### 1. Set up the database.
Use the Maldonado database or create a new database with the required tables specified in the database section below.
### 2. Select a project.
Choose a project to extract comments from. An informal analysis has already been done on five opens-source android projects. Details can be found here: https://github.com/mfrenken85/SATD2018_Frenken/blob/master/documentation/analysis_0.md
### 3. Extract comments from a project using srcML.
3.1. Download and install srcML: https://www.srcml.org
3.2. Use srcML to convert an entire project to a single xml file. Use the following command: srcml <name of project folder> -o <name of project>.xml
Some project have already been converted to xml, they can be found here: https://github.com/mfrenken85/SATD2018_Frenken/tree/master/projects
### 4. Insert comments to database.
In py_scripts/ you can find extract_comments.py
### 5. Populate treated_commenttext.
populate_treated_commenttext.py
### 6. Classify comments manually.
Use the labeling_turorial.md found in documentation/.
### 7. Run classify_comments.py to check performance of the classifier.
Results are stored in classifier/output/. 
- classified_seq.test
- output.txt
- results.txt

## Database
