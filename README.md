https://anhsapp.herokuapp.com/

<h2>1. Business Problem</h2>
Home Sales is a fictitious company specialized in buying and reselling real state. 
Our business model consists of analyzing features and locations of properties to perform advantageous buying and selling operations. 
Currently, the objective of data analysis is to find and filter those properties with safe purchase and potential profit.

<h2>2. Business Assumptions</h2>
<h4>2.1 Purchasing and selling real state:</h4>
a) Only properties with prices lower than median price of each corresponding region will be purchased;
b) Only properties in good condition (column "condition" >= 3) will be purchased;
c) Real state reselling price will be raised 20% over its original price.

<h4>2.2 Data reformulation:</h4>
a) Outliers prices won't be excluded;
b) Duplicated values in column "ID" will be excluded.

| Features            | Description                                                                                                    |
|---------------------|----------------------------------------------------------------------------------------------------------------|
| id                  | Property identification code                                                                                   |
| date                | Property selling date                                                                                          |
| price               | Price which the property was announced                                                                         |
| bedrooms            | Number of bedrooms                                                                                             |
| bathrooms           | Number of bathrooms                                                                                            |
| sqft_living         | Inside property measure                                                                                        |
| sqft_lot            | Lot space                                                                                                      |
| floors              | Number of floors                                                                                               |
| waterfront          | Indicates view for sea (0: no, 1: yes)                                                                         |
| view                | Index from 0 to 4, indicates real state quality of view (0: lowest, 4: highest)                                |
| condition           | Index from 1 to 5, indicates real state condition                                                              |
| sqft_basement       | Basement space measurement                                                                                     |
| yr_built            | Year which the property was built                                                                              |
| yr_renovated        | Year which the property was renewed (if it was renewed)                                                        |
| zipcode             | Property postal code                                                                                           |
| lat                 | Latitude coordinates                                                                                           |
| long                | Longitude coordinates                                                                                          |
| is_winter           | Indicates if the property was announced in the winter (0: no, 1: yes)                                          |
| median_price        | Median price of other properties from the same zipcode where the property is located                           |
| winter_median_price | Median price of other properties, announced in the winter, from the same zipcode where the property is located |
| is_renovated        | Indicates if property was renewed (0: no, 1: yes)                                                              |
| worth_buying        | Indicates if property should be purchased; according to the business assumptions                               |
| profit_value        | Value that represents the 20% addition over the purchasing price as profit                                     |
| selling_price       | Reselling property price                                                                                       |

<h2>3. Solution strategy</h2>
<h4>3.1 Load data from Kaggle (https://www.kaggle.com/shivachandel/kc-house-data);</h4>
<h4>3.2 Clean data:</h4>
a) Remove unnecessary columns.
<h4>3.3 Data reformulation:</h4>
a) Gather properties by zipcode and define median price value (median_price);
b) Identificate properties announced during the winter (To answer the insight: Are properties announced in the winter cheaper, due to low locomotion?);
c) Gather properties announced in the winter and define median price for winter (winter_median_price); 
d) Determine what properties are worth buying (worth_buying) and the profit value (profit_value);
e) Generate worth-buying list.
<h4>3.3 Explore and analyse data through bar charts;</h4>
<h4>3.4 Validate insights.</h4>
<h4>3.5 Develop interactive dashboard through Streamlit and Heroku;</h4>
<h4>3.6 Analyse result and conclusion;</h4>

<h2>4. Top 3 business insights</h2>
<h4>4.1 Properties announced in the winter are, at least, 20% cheaper, due to low mobility and internet competition;</h4>
a) Application: Multiple properties purchase during the winter may be more interesting, due to the possibility of a bigger discount;
<body bgcolor=”#800000">
<img align="center" alt="4_1" src="https://user-images.githubusercontent.com/86201991/178035940-1e7e0aa1-2fe7-44ae-91f1-1b7f75cdb5a2.png" /></body>
The average price of houses announced during the winter is U$544.860,00, meanwhile, the average price of those houses announced in any other season is U$527.897,00. The difference between these values is only 3.11%. Besides, even if detailing the data even more, we can't see significant difference in prices when the properties are separeted by zipcode. Therefore, as the price difference is not relevant, it comes to a conclusion that this is a false business insight.

<h4>4.2 Renewed houses and apartments are at least 30% more expensive than non-renewed ones;</h4>
a) Application: Buying non-renewed houses and renewing them later on may turn out to be interesting due to the difference between prices; 
<img align="center" alt="4_2" src="https://user-images.githubusercontent.com/86201991/178035963-536e48e0-9347-4f83-a810-5ddbee340694.png" />
As we can see in the chart, the average price of non-renovated properties is U$530.723,08, and renovated houses average price is U$761.718,50. The contrast between these prices is considerable and represents a difference of 30,32%, surpassing the estimated value of 30% and validating this business insight as true and highlighting the possibility of profit earn through the renovation of some properties.

<h4>4.3 Houses with waterfront view are, at least, 20% more expensive than other houses;</h4>
a) Application: Allows studying better possibilities of buying these properties and get a bigger profit on a resale.
<img align="center" alt="4_3" src="https://user-images.githubusercontent.com/86201991/178035976-b1e941cb-327e-4136-8ada-4251db1ca504.png" />
The first plot shows us the median price of all properties, classifying those with and without waterfront view. The difference between those values is U$950.000. In this ocasion, waterfront properties value exceeds 300% of the value of non-waterfront properties.
Besides, the second chart details even more the contrast of prices and allows us to realize the valorization of waterfront houses far beyond the estimated value of 20%. This proves the point of the insight, validating it and raising questions about the profit potential of buying waterfront houses.

After cleaning, analysing and reformulating the data, it was possible to efficiently highlight the best properties for purchase and resale, 
allowing a dynamic visualization of the properties, as well as its features and locations through graphic visualization and price comparisons.
Due to these results, the worth buying properties were listed in a document which contains the property identification (id), buying price (price) and selling price (selling_price).
An application was developed using Streamlit and Heroku, available to access the dataframe and its bar charts in any platform.
The estimated profit from the properties resale is U$777.552.813,20, standing out the real possibility of good results for a great financial feedback.
