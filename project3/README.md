# Project #3 Description

"Falsehood flies, and Trush comes limping after it" - Jonathan Swift, 1710

There is lots of misinformation on the internet. Some simply because the internet is not peer (or expert) reviewed. Some because there are bad actors actively spreading lies to mislead and pursuade people to believe things that aren't true and act on those lies.

With the ease at which information spreads around the world, now, more than ever, we need to be able to understand what is true and what is not. Setting aside any philosophical or religious debate on if there are any absolute truths, let's do some work on truth finding.  Or at least understanding how lies spread on the internet!

## Data about Truth and Lies
For this project, we're going to work with two data sets.  The first is a large database of tweets made by Rusian Troll bots. We can assume for purposes of this project that the trolls were not posting truths. Consider all of these tweets to be made in an effort to spread misinformation.  [These tweets](https://www.kaggle.com/datasets/rmisra/politifact-fact-check-dataset) were collected by the political prognosticators at 538.

Our [other data set](https://github.com/fivethirtyeight/russian-troll-tweets/) is a file with a list of things said by political and public figures that were fact checked by Politifact. This file includes who said it, what they said, and the final verdict the fact checkers had on the statement: from True to False or _Pants on Fire!_

Our goal with this project is to deconstruct the statements in each data set using primative natural language processing. We'll then cross-reference the "top 20" topics addressed by the Rusian Troll bots with the statements from real people. The output will be a sort of correlation matrix showing how often each of the "top 20" topics shows up in quotes from real people saying things that are True, Mostly-True, Mostly-False, False, or Pants-on-Fire.

Before you start, make a hypothesis.  Do you think Rusian Trolls are trying to spread information more often about things that are true or things that will light your pants on fire?

## Requirements
* Remove typical stop words
* Assume that the only words we care about are "Nouns" and "Named Entities" in the tweets and comments
* Focus on just the "top 20" words
* If there is other "cleanup" you think is important for the analysis, please include it!

# Project Deliverables

## Final Data Set:
The final data set should be a cross-reference between the top 20 topics addressed in the Rusian Troll tweets and verdits from the Politifact findings. The number at the intersection should be how many of the Politifact findings with that verdict touched on that topic.

| Verdict | Topic 1 | Topic 2 | Topic 3 | ... | Topic 20 |
|---------|---------|---------|---------|-----|----------|
| True    |   1,234 |     987 |     456 |     |   10,342 |
| Mostly-True|  456 |   1,456 |     789 |     |    1,832 |
| Mostly-False| 888 |   2,789 |   3,123 |     |       33 |
| False   |   8,123 |   9,234 |   7,456 |     |    6,456 |
| Pants-on-Fire|  9 |   1,448 |   3,998 |     |    2,334 |
|         |         |         |         |     |          |

## Code:
Use **dagster** as your toolkit again. Create a DAG that takes your input data sources and produces the required Final Data Set described above. As usual, I'll grade on three criteria:
1. Does your code run?
2. Does your code produce the right output?
3. Did you write code that follows good practices and is easy to understand?

I'm not so very concerned about exactly the right answer. Since there are multiple ways to generate a solution, I'm not going to provide an exact answer to try to match. I look forward to reviewing your solutions.

## NLP Resources:
I recommend using the Python NLTK library for doing the NLP work with this project. Here's a [Getting Started with NLTK article from RealPython](https://realpython.com/nltk-nlp-python/).  Also see the `nlp_demo.ipynb` in this repository for another example.

## Diagram:
Create a simple visual diagram describing your DAG. Store it as a PNG file in your project repository.
