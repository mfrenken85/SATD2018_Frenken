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

##Analysis of android projects
The goal of this analysis is to test the scripts and workflow that are to be used for verifying the classifier on different ecosystems, and to get an impression of how much design TD the classifier is able to identify given projects in the android ecosystem. This is a limit analysis due to time constraints. For the full analysis the projects under inspection should be more carefully chosen, and a significant sample of the extracted comments should be manually classified.

Moreover, the comment extraction script currently in use is very primitive. The script simply exactracts comments all comments found directly before methods or within the method body. Maldonado used the following filtering heuristics in his study:
1. Remove licence comments
2. Long comments can be created by multiple single lines. Merge consecutive line comments.
3. remove commented source code
4. remove auto-generated comments
5. remove java doc comments

Note that none of the above are applied. However, a lot of potential problems are avoided by only inspecting files in the src directory of the project. Also, comments outside of methods are only inspected if they directly precede the method, hence avoiding a lot of version comments. The most problematic shortcoming is believed to be the lack of merging consecutive line comments.

For reference, these are the averages from the projects of the Maldonado study:
\# of Classes: 1,625
SLOC: 146,206
\# of Contributors: 91
\# of Comments: 25,923
\# of Comments after filtering: 6,257
\# (%) of TD Comments: 407 (1.86%)
(%) of Design Debt: 71.84
(%) of Requirement Debt: 14.24
(%) of Other Debt: 13.89


Info:
Using classifier built by tenfold script using 54500 comments from the original database created by Maldonado.
\# LOC: the total lines of code of the xml file extracted by scrml. Note that is not the exact number, but it should be close enough for the purpose of this analysis.
\# comments extracted: as extracted by extract_comments.py created by Mark Frenken. Note that this script has undergone only limited testing for correctness.
\# (%) of positives: number of comments classified as design TD by classifier

Analysis of the FP2-Launcher on design debt:
Project: Fairphone 2 Launcher: https://github.com/WeAreFairphone/FP2-Launcher
\# of Classes: 131
\# LOC: 136,191
\# of Contributors: 47
\# comments extracted: 3,431
\# (%) of positives: 63 (1.83%)

Analysis of the reddit-android-appstore on design debt:
Project: /r/Android App: https://github.com/d4rken/reddit-android-appstore
\# of Classes: 21
\# LOC: 6,756
\# of Contributors: 14
\# comments extracted: 46
\# (%) of positives: 40 (86.96%)

Analysis of the VocableTrainer-Android on design debt:
Project: VocableTrainer-Android: https://github.com/0xpr03/VocableTrainer-Android
\# of Classes: 55
\# LOC: 14,475
\# of Contributors: 3
\# comments extracted: 482
\# (%) of positives: 18 (3.73%)

Analysis of the NewPipe on design debt:
Project: NewPipe: https://github.com/TeamNewPipe/NewPipe
\# of Classes: 108
\# LOC: 35,352
\# of Contributors: 243
\# comments extracted: 993
\# (%) of positives: 15 (1.51%)

Project: android-oss: https://github.com/kickstarter/android-oss
\# of Classes: 133
\# LOC: 51,305
\# of Contributors: 23
\# comments extracted: 747
\# (%) of positives: 13 (1.74%)

## Finding more projects:
The following list appears to have some interesting projects:
https://medium.mybridge.co/38-amazing-android-open-source-apps-java-1a62b7034c40

## TODO
- Finish this readme
- Notes on how serialized classifiers were created
- Update classified comments to database?