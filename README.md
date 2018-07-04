# SATD2018
CAPITA project by Mark Frenken on SATD. The Maldonado database is needed to run this project.
However, if the Maldonado database is not available, the sql queries needed to build the required
tables are included in tables.sql.

## How to use
1. Set up the database. Either use the Maldonado database or create a new database and create the required tables specified in tables.sql.
2. Extract comments from a project using srcML. Some have already been included in the the projects folder.
3. Run extract_comments.py to store in Maldonado database.
4. Classify comments manually.
5. Run classify_comments.py to check performance of the classifier.

## TODO
- Finish this readme
- Notes on how serialized classifiers were created
- Update classified comments to database?