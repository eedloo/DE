# Project #3 Grading Guidelines
The purpose of this project is to undertand if there is a correlation between the topics tweeted about by confirmed Russian troll bots and the final verdict on topics fact-checked by Politifact. We'll use NLP to understand the contents in the tweets and merge that data with the Politifact results.

**The project will be graded on a scale of 0 to 100 points and will represent 20% of your overall semester grade.**

## Does it run
**20 points**
* Runs as expected.


This is a dagster project. I expect to be able to run `dagit -f file.py` and have dagster materialize all assets correctly.


## Does it produce correct results
**60 points**
* Mostly worked without any issues.  While I like how you set things up to use pre-run pickled data in some cases, that did cause an issue for me running the code.  For example, I decided to no use the pre-lemmatized data and pre-defined tags, I had to tweek your "use_dumped" default.  That's ok.


Your code may not be perfect.  That's OK. The correctness of results will be graded on a range from 0 to 60 points depending on how many of the output rows and columns are correct.  This project does not have one CORRECT answer. The results you get depend on how you've cleansed the topics.  I'll be grading based on the format and general sense of the data produced.


## Is your code good
**20 points**
* Excellently organized code with tools in place to help with testing.
* Great documentation.
* I like how you kept your pipeline clean and just called the data load/transformation functions out of the functions.py file.

Do you follow good programming practices? Have you broken up your program into logical components that are easily testable? Have you followed reasonable variable naming standards. Do you include comments and documentation?

Basically, how easy was it for me to follow what you were doing with your code?
