# Project #2 Grading Guidelines
The purpose of this project is to demonstrate your ability to work with a basic dagster project and to merge multiple datasets together.

**The project will be graded on a scale of 0 to 100 points and will represent 20% of your overall semester grade.**

## Does it run
**20 points - runs correctly**

I expect to be able to use `dagit` to verify that your code is working correctly and produces the right output.


## Does it produce correct results
**60 points - output looks correct**

Your code may not be perfect.  That's OK. The correctness of results will be graded on a range from 0 to 40 points depending on how many of the output rows and columns are correct.  For instance, if your output produces all the correct columns of data, but not all of the expected rows, you will lose some points, but not all. If your output produces all the rows expected, but some of the columns have the wrong data, you will lose some points, but not all.

If your program does not run at all, I will review your source code in detail and try to determine what portion of data is being processed correctly.  It will be better if your code runs, though.


## Is your code good
**19 points**
* I like your separation of logic (in Pipeline.py) and the data flow (in Dagster.py)
* Good comments in your Pipeline.py file but not Dagster.py
* Suggestions: Use docstring style comments in your dagster file. It will put that into the GUI.
* You ocassionally mix in TitleCase variable names into your code. I recommend sticking with one convention (lowercase is my preference)
* Something to consider - You crammed a lot of steps into `car_stocks()`.  Would it have made sense to keep those as separate steps in Dagster?

Do you follow good programming practices? Have you broken up your program into logical components that are easily testable? Have you followed reasonable variable naming standards. Do you include comments and documentation?

Basically, how easy was it for me to follow what you were doing with your code?
