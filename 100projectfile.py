# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import os
from faker import Faker
from faker_food import FoodProvider
import random
from scipy.stats import gamma

# defining function to make random number generators
def get_gamma_distribution(mean, sd):
    return gamma(mean,sd)

# set path
os.chdir("C:/Users/Lana/Desktop/1.00/project")

# read in data from csv
data = pd.read_csv("Food_Production.csv")

# display(data)
#print(list(data.columns.values))

# remove unwanted columns
data = data.drop(['Land use change', 'Animal Feed', 'Farm', 'Processing', 'Transport', 'Packging', 
                  'Retail','Eutrophying emissions per kilogram (gPO₄eq per kilogram)', 
                  'Eutrophying emissions per 100g protein (gPO₄eq per 100 grams protein)', 
                  'Freshwater withdrawals per 100g protein (liters per 100g protein)', 
                  'Freshwater withdrawals per kilogram (liters per kilogram)',  
                  'Greenhouse gas emissions per 100g protein (kgCO₂eq per 100g protein)', 
                  'Land use per kilogram (m² per kilogram)', 
                  'Land use per 100g protein (m² per 100g protein)', 
                  'Scarcity-weighted water use per kilogram (liters per kilogram)', 
                  'Scarcity-weighted water use per 100g protein (liters per 100g protein)'], axis=1)

# calculate mean and standard deviation of each column
mean = data.mean(axis=0)
sd = data.std(axis=0)

# create gamma distributions for each column
total_emissions = get_gamma_distribution(mean['Total_emissions'], sd['Total_emissions'])
eutrophying_emissions = get_gamma_distribution(mean['Eutrophying emissions per 1000kcal (gPO₄eq per 1000kcal)'], sd['Eutrophying emissions per 1000kcal (gPO₄eq per 1000kcal)'])
freshwater_withdrawals = get_gamma_distribution(mean['Freshwater withdrawals per 1000kcal (liters per 1000kcal)'], sd['Freshwater withdrawals per 1000kcal (liters per 1000kcal)'])
greenhouse_gas_emissions = get_gamma_distribution(mean['Greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)'], sd['Greenhouse gas emissions per 1000kcal (kgCO₂eq per 1000kcal)'])
land_use = get_gamma_distribution(mean['Land use per 1000kcal (m² per 1000kcal)'], sd['Land use per 1000kcal (m² per 1000kcal)'])
scarcity_weighted_water_use = get_gamma_distribution(mean['Scarcity-weighted water use per 1000kcal (liters per 1000 kilocalories)'], sd['Scarcity-weighted water use per 1000kcal (liters per 1000 kilocalories)'])

# establishing faker 
fake = Faker()
fake.add_provider(FoodProvider)

# create fake data
fake_data = [
    {'Food':fake.unique.ingredient(),
    'Total Emissions':total_emissions.rvs(),
    'Eutrophying Emissions':eutrophying_emissions.rvs(),
    'Freshwater Withdrawals':freshwater_withdrawals.rvs(),
    'Greenhouse Gas Emissions':greenhouse_gas_emissions.rvs(),
    'Land Use':land_use.rvs(),
    'Scarcity weighted water use':scarcity_weighted_water_use.rvs(),
    } for x in range(0,470)]

# print the names of the foods
# for x in range(0,485):
#     print(fake_data[x]['Food']) 

# creating a pandas dataframe of fake data
fake_df = pd.DataFrame(fake_data)
display(fake_df)

# plot histograms of fake data
#fake_df.hist(bins=10, figsize=(20,15))
#plt.show()


##############################################################
# calculate and display mean and standard deviation of each column in fake data
mean_fake = fake_df.mean(axis=0)
sd_fake = fake_df.std(axis=0)

# add points column to fake data
fake_df["Points"] = 0

# print column names, mean, and standard deviation of fake data
# print(list(fake_df.columns.values))
# print(mean_fake)
# print(sd_fake)

# iterate through each food in each column of fake data and compare to mean and standard deviation
print(fake_df.iloc[1,7])
for x in range(1,7):
    for y in range(0,470):
        if fake_df.iloc[y,x] >= mean_fake[x-1] + sd_fake[x-1]:
            fake_df.iloc[y,7] += 30
        elif fake_df.iloc[y,x] < mean_fake[x-1] + sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] + 0.75*sd_fake[x-1]:
            fake_df.iloc[y,7] += 37
        elif fake_df.iloc[y,x] < mean_fake[x-1] + 0.75*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] + 0.5*sd_fake[x-1]:
            fake_df.iloc[y,7] += 44
        elif fake_df.iloc[y,x] < mean_fake[x-1] + 0.5*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] + 0.25*sd_fake[x-1]:
            fake_df.iloc[y,7] += 51
        elif fake_df.iloc[y,x] < mean_fake[x-1] + 0.25*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1]:
            fake_df.iloc[y,7] += 58
        elif fake_df.iloc[y,x] < mean_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] - 0.25*sd_fake[x-1]:
            fake_df.iloc[y,7] += 72
        elif fake_df.iloc[y,x] < mean_fake[x-1] - 0.25*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] - 0.5*sd_fake[x-1]:
            fake_df.iloc[y,7] += 79
        elif fake_df.iloc[y,x] < mean_fake[x-1] - 0.5*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] - 0.75*sd_fake[x-1]:
            fake_df.iloc[y,7] += 86
        elif fake_df.iloc[y,x] < mean_fake[x-1] - 0.75*sd_fake[x-1] and fake_df.iloc[y,x] >= mean_fake[x-1] - sd_fake[x-1]:
            fake_df.iloc[y,7] += 93
        elif fake_df.iloc[y,x] < mean_fake[x-1] - sd_fake[x-1]:
            fake_df.iloc[y,7] += 100
        else:
            fake_df.iloc[y,7] += 0

# print average of points column
# print(fake_df["Points"].mean(axis=0))
# print(mean_fake[1])
# print(sd_fake[1])

# calculating score column
fake_df["Score"] = fake_df["Points"]/6

# plot histograms of score column
#fake_df.hist(column="Score", bins=10, figsize=(20,15))
#plt.show()

# print the top 10 foods
print("Top 10 foods: ",fake_df.nlargest(10, 'Score'))

# print the bottom 10 foods
print("Bottom 10 foods: ",fake_df.nsmallest(10, 'Score'))

# print the score of a food
input = input("Enter a food to see its sustainability score: ")
if input in fake_df.values:
    score = fake_df.loc[fake_df['Food'] == input]['Score']
    score_df = score.to_frame()

    if score_df.iloc[0,0] >= 90:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is very sustainable!")
    elif score_df.iloc[0,0] >= 80 and score_df.iloc[0,0] < 90:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is sustainable!")
    elif score_df.iloc[0,0] >= 70 and score_df.iloc[0,0] < 80:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is somewhat sustainable.")
    elif score_df.iloc[0,0] >= 60 and score_df.iloc[0,0] < 70:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is not very sustainable.")
    elif score_df.iloc[0,0] >= 50 and score_df.iloc[0,0] < 60:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is not sustainable.")
    else:
        print("Score: ", score_df.iloc[0,0], "out of 100 --> This food is very unsustainable!")





