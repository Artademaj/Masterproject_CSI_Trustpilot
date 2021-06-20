### Check current working directory and import packages###
import os
wd = os.getcwd() 
print(wd)

import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
from numpy import corrcoef
import seaborn as sns
import pingouin as pg
import warnings
warnings.filterwarnings("ignore")

### Create postgres connection, read in tables and clean data
engine = create_engine('postgresql://localhost/')

# Read final tables from Database
final_reviews_animals_pets = pd.read_sql_table(
    "final_reviews_animals_pets",
    con=engine
)

final_reviews_beauty_wellbeing = pd.read_sql_table(
    "final_reviews_beauty_wellbeing",
    con=engine
)

final_reviews_business_services = pd.read_sql_table(
    "final_reviews_business_services",
    con=engine
)

final_reviews_construction_manufactoring = pd.read_sql_table(
    "final_reviews_construction_manufactoring",
    con=engine
)

final_reviews_education_training = pd.read_sql_table(
    "final_reviews_education_training",
    con=engine
)

final_reviews_electronics_technology = pd.read_sql_table(
    "final_reviews_electronics_technology",
    con=engine
)

final_reviews_events_entertainment = pd.read_sql_table(
    "final_reviews_events_entertainment",
    con=engine
)

final_reviews_food_beverages_tobacco = pd.read_sql_table(
    "final_reviews_food_beverages_tobacco",
    con=engine
)

final_reviews_health_medical = pd.read_sql_table(
    "final_reviews_health_medical",
    con=engine
)

final_reviews_hobbies_crafts = pd.read_sql_table(
    "final_reviews_hobbies_crafts",
    con=engine
)

final_reviews_home_garden = pd.read_sql_table(
    "final_reviews_home_garden",
    con=engine
)

final_reviews_home_services = pd.read_sql_table(
    "final_reviews_home_services",
    con=engine
)

final_reviews_legal_services_government = pd.read_sql_table(
    "final_reviews_legal_services_government",
    con=engine
)

final_reviews_media_publishing = pd.read_sql_table(
    "final_reviews_media_publishing",
    con=engine
)

final_reviews_money_insurance = pd.read_sql_table(
    "final_reviews_money_insurance",
    con=engine
)

final_reviews_public_local_services = pd.read_sql_table(
    "final_reviews_public_local_services",
    con=engine
)

final_reviews_restaurants_bars = pd.read_sql_table(
    "final_reviews_restaurants_bars",
    con=engine
)

final_reviews_shopping_fashion = pd.read_sql_table(
    "final_reviews_shopping_fashion",
    con=engine
)

final_reviews_sports = pd.read_sql_table(
    "final_reviews_sports",
    con=engine
)

final_reviews_travel_vacation = pd.read_sql_table(
    "final_reviews_travel_vacation",
    con=engine
)

final_reviews_utilities = pd.read_sql_table(
    "final_reviews_utilities",
    con=engine
)

final_reviews_vehicles_transportation = pd.read_sql_table(
    "final_reviews_vehicles_transportation",
    con=engine
)

### Combine all final df for final calculations
Final_steps = final_reviews_animals_pets.append([final_reviews_beauty_wellbeing, final_reviews_business_services, final_reviews_construction_manufactoring, final_reviews_education_training, final_reviews_electronics_technology, final_reviews_events_entertainment, final_reviews_food_beverages_tobacco, final_reviews_health_medical, final_reviews_hobbies_crafts, final_reviews_home_garden, final_reviews_home_services, final_reviews_legal_services_government, final_reviews_media_publishing, final_reviews_money_insurance, final_reviews_public_local_services, final_reviews_restaurants_bars, final_reviews_shopping_fashion, final_reviews_sports, final_reviews_travel_vacation, final_reviews_utilities, final_reviews_vehicles_transportation])
#Final_steps = final_reviews_animals_pets.append([final_reviews_beauty_wellbeing, final_reviews_business_services, final_reviews_construction_manufactoring, final_reviews_education_training])
Final_steps.dropna(subset = ["company_market"], inplace=True)
# Round numers to 2 decimals
Final_steps.round(2)
# Fill NAN values with 0
Final_steps.fillna(0)
# delete index column
del Final_steps['index']
Final_steps
#rename column names
Final_steps.columns.values[2] = "Sustainability Index" 
Final_steps.columns.values[3] = "Social Index" 
Final_steps.columns.values[4] = "Environmental Index" 
Final_steps.columns.values[5] = "Economic Index" 
Final_steps.columns.values[7] = "Sentiment" 
Final_steps

# See which dimension is the most common one
print(Final_steps['Social Index'].sum())
print(Final_steps['Environmental Index'].sum())
print(Final_steps['Economic Index'].sum())

# Calculate the mean 
Final_steps["Sustainability Index"].mean()
Final_steps["price"].mean()

# Calculating the correlation between two columns
pg.corr(x=Final_steps['Sustainability Index'], y=Final_steps['price'])
pg.corr(x=Final_steps['Social Index'], y=Final_steps['price'])
pg.corr(x=Final_steps['Environmental Index'], y=Final_steps['price'])
pg.corr(x=Final_steps['Economic Index'], y=Final_steps['price'])

# Calculate the correlation and visualize it
Final_steps.corr().round(2)
corrs = Final_steps.corr()
mask = np.zeros_like(corrs)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corrs, cmap='Spectral_r', mask=mask, square=True, vmin=-.4, vmax=.4)
plt.title('Correlation matrix')