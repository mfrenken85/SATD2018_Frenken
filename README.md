# SATD2018
CAPITA project by Mark Frenken on SATD.

## How to use
### 1. Set up the database.
Use the Maldonado database or create a new database with the required tables specified in the database section below.
### 2. Select a project.
Choose a project to extract comments from. An informal analysis has already been done on five opens-source android projects. Details can be found here: https://github.com/mfrenken85/SATD2018_Frenken/blob/master/documentation/analysis_0.md
### 3. Convert project to xml using srcML.
- Download and install srcML: https://www.srcml.org
- Use srcML to convert an entire project to a single xml file. Use the following command: srcml \<name of project folder\> -o \<name of project\>.xml

Some project have already been converted to xml, they can be found here: https://github.com/mfrenken85/SATD2018_Frenken/tree/master/projects
### 4. Extract comments from xml and insert into database.
A script for comment extraction is included in the github. However, this script does not meet the requirements outlined by Maldonado. A more advanced script is needed. The basic script for comment extraction can be found in the py_scripts folder.
### 5. Populate treated_commenttext.
Comments need to be cleaned in order for the classifier to work. The extraction script from this github automatically does this when inserting comments into the database. However, if a different script for comment extraction is used, the comments may need to be treated. The script populate_treated_commenttext.py found in the py_scripts folder can do this.
### 6. Classify comments manually.
Use the labeling turorial by Maldonado found here: https://github.com/mfrenken85/SATD2018_Frenken/blob/master/documentation/labeling_turorial.md
### 7. Run classify_comments.py to check performance of the classifier.
Results are stored in classifier/output/ in the following three files:
- classified_seq.test: the input of the classifier containing the data that is to be classified. Note this file also includes the id of each comment.
- output.txt: the output of the classifier containing the labels given to the data by the classifier.
- results.txt: contains statistics on the classification.

Please note that running the script again will overwrite these files. If the results need to be stored, move the files to a different folder. For example, create a new folder with the project name in classifier/output/ as was done with previous projects.

## Database
