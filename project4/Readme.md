# UberEat Data Engineering  

Have you ever wondered what information is needed for building a machine learning algorithm upon a food dataset? What features would be critical? Are review numbers, review scores, and address sufficient for a model?  
In order to build a powerful model, more relevant data is better. The more information we gather for each observation, the more accurate our model will be.  
In this project, we use UberEat dataset from Kaggle to explore the features, check what other features we can provide, and how we can furnish our data for a tentative model. In this regard, we aim to create some new informative features, and concatenate the base dataset with other usefull data to have thourough information.  
The data we use for this project are as below:  

## UberEat dataset  

This dataset is hosted on [Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus) is the base for this project, and is free to use. The dataset is consisted of two *CSV* files: restaurants, and restaurant-menus. Full description of the dataset is provided on the webpage.  
In order to use the data properly, it is recommended to extract it in the **Data** folder, and let the names be intact. 

## US Census dataset  

This dataset is available on the [United States Census Bureau](https://data.census.gov/). The dataset is free to use for everyone. The United States Census Bureau publishes several demographic information on the website and among them, we were interested to find out the median income of each area in the country based on the zip codes. It can be argued that the income of family has a relationship with the number of times they go out for dinner.  
If individuals are interested to download from the website, they need to use some filtration to access proper data. However, the data has already been downloaded and is available in the **Data** folder.  

## Countries adjectivals  

In the *UberEat* restaurant dataset, some general information is provided about the restaurant on the *Category* column. One interesting thing is whether the restaurant offers international cuisines. In this dataset, the food originality information is provided by the country name adjectival form, like American or Thai.  
Therefore, we need a resource for adjectival form of countries' names. We used the information from [Education First](https://www.ef.com/wwen/english-resources/english-grammar/nationalities/) to catch the information and feed to pipeline. On the webpage, there are some tables providing the information we need to add to our dataset.  