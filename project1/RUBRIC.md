# Project #1 Grading Guidelines
The main purpose of this first project is to work on understanding underlying data structures, relationships between hierarchical data in JSON format, and being able to transform that into a flat (denormalized) format that a data anlyst or data scientist could use more easily.  This kind of denormalization also helps create files for analytical databases like a data warehouse.

**The project will be graded on a scale of 0 to 100 points and will represent 20% of your overall semester grade.**

## Does it run
**0 or 20 points**

I expect to be able to use `pytest` to verify that your code is working correctly and produces the right output.  I've provided a testing framework and test files so that you can focus your efforts on the data engineering part of this project.

I've included a sample file that will fail when you first try to run `pytest`.  That's just to show what a failure will look like.  Before you submit your final version, please remove the `./test/simple.json` and `./test/simple2.json` test files.  Your final code does not need to handle those files.


## Does it produce correct results
**Range of 0 to 60 points**

Your code may not be perfect.  That's OK. The correctness of results will be graded on a range from 0 to 40 points depending on how many of the output rows and columns are correct.  For instance, if your output produces all the correct columns of data, but not all of the expected rows, you will lose some points, but not all. If your output produces all the rows expected, but some of the columns have the wrong data, you will lose some points, but not all.

If your program does not run at all, I will review your source code in detail and try to determine what portion of data is being processed correctly.  It will be better if your code runs, though.


## Is your code good
**Range of 0 to 20 points**

Do you follow good programming practices? Have you broken up your program into logical components that are easily testable? Have you followed reasonable variable naming standards. Do you include comments and documentation?

Basically, how easy was it for me to follow what you were doing with your code?
