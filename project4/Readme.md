# UberEat Data Engineering  

Have you ever wondered what information is needed for building a machine learning algorithm upon a food dataset? What features would be critical? Are review numbers, review scores, and address sufficient for a model?  

In order to build a powerful model, more relevant data is better. The more information we gather for each observation, the more accurate our model will be.  

In this project, we uses UberEat dataset from Kaggle to explore the features, check what other features we can provide, and how we can furnish our data for a tentative model. In this regard, we aim to create some new informative features, and concatenate the base dataset with other usefull data to have thourough information.  
The data we use for this project are as below:  


## UberEat dataset  

This dataset is hosted on [Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/uber-eats-usa-restaurants-menus) and is free to use. This dataset is consisted of two *CSV* files: restaurants, and restaurant-menus.  

In order to use the data properly, it is recommended to extract it in the **Data** folder, and let the names be intact. 

## US Census dataset  

This dataset is available on the [United States Census Bureau](https://data.census.gov/). The dataset is free to use for everyone. The United States Census Bureau publishes several demographic information on this website and among them, we were interested to find out the median income of each area in the country based on the zip codes. Providing that, if individuals are interested to download from the website, they need to use some filtration to access proper data. However, the data has already been downloaded and is available in the **Data** folder.  

## Conutries adjectivals  

On the *UberEat* restaurant dataset, some general information is provided about the restaurant on the *Category* column. One interesting thing is whether the restaurant offers international cuisines. In this dataset, the food originality information is provided by the country name adjectival form, like American or Canadian.  
Therefore, we need a small dataset of adjectival form of countries' names. We used the information from [Education First](https://www.ef.com/wwen/english-resources/english-grammar/nationalities/). On this page, there are some tables providing the information we need to add to our dataset.  

## Summary  

In this project we use above mentioned dataset and data sources to provide more detail and relevant information for *UberEat* dataset. Some new features have been engineered and added to data like:  

Address information