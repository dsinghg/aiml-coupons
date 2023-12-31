# python code to analyze the data about different types of drivers acceopting bar, restaurant coupons


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Read in the coupons.csv file
# data = pd.read_csv('/Users/dsgarcha/Downloads/assignment_5_1_starter/data/coupons.csv')
data = pd.read_csv('./coupons.csv')

# Review data, 12684 rows, 26 columns
data.head()
data.info()


# Investigate the dataset for missing or problematic data

missing_values = data.isnull().sum().sort_values() # check for any missing values
missing_values

# car column has 99% missing values, so drop it
# direction_opp has just inverse values than direction_same, so drop it
data2 = data.drop(['car', 'direction_opp'], axis=1)
data2.info()

# Replace missing values (nan) in Bar, RestaurantLessThan20, CarryAway, Restaurant20To50, CoffeeHouse with '1~3'
data2[['Bar', 'RestaurantLessThan20', 'CarryAway', 'Restaurant20To50', 'CoffeeHouse']] = data2[['Bar', 'RestaurantLessThan20', 'CarryAway', 'Restaurant20To50', 'CoffeeHouse']].fillna('1~3')

# Use a bar plot to visualize the coupon column
plt.bar(data2['coupon'].unique(),data2['coupon'].value_counts())
plt.xlabel('Coupon Type')
plt.ylabel('Count')
plt.title('Count by Coupon Types')

# Use a histogram to visualize the temperature column
plt.title('Histogram of Temperature')
plt.xlabel('Temperature')
plt.hist(data2['temperature'])

# Create a new DataFrame that contains just the bar coupons.
data_bar = data2[['Bar', 'income', 'occupation', 'maritalStatus', 'age', 'passanger', 'RestaurantLessThan20', 'Y']]
data_bar.info()

# What proportion of bar coupons were accepted?
bar_coupons_accpet = data_bar['Y'].value_counts()[1] / len(data_bar.index)
bar_coupons_accpet # 56.84%

# create new DataFrames for those accpeting the coupons and not accepting them
data_bar_yes = data_bar.loc[data_bar.Y == 1]
data_bar_no = data_bar.loc[data_bar.Y == 0]

# Compare the acceptance rate between those who went to a bar 3 or fewer times a month to those who went more
lt3_bar = data_bar['Bar'].value_counts()['never'] + data_bar['Bar'].value_counts()['less1'] + data_bar['Bar'].value_counts()['1~3']
lt3_bar_yes = data_bar_yes['Bar'].value_counts()['never'] + data_bar_yes['Bar'].value_counts()['less1'] + data_bar_yes['Bar'].value_counts()['1~3']
lt3_bar_accept = lt3_bar_yes / lt3_bar
lt3_bar_accept # 55.67%

gt3_bar = data_bar['Bar'].value_counts()['4~8'] + data_bar['Bar'].value_counts()['gt8']
gt3_bar_yes = data_bar_yes['Bar'].value_counts()['4~8'] + data_bar_yes['Bar'].value_counts()['gt8']
gt3_bar_accept = gt3_bar_yes / gt3_bar
gt3_bar_accept # 62.25%


# dataset with ages greater than 25
data_bar_gt25 = data_bar.loc[data_bar['age'].isin(['46', '26', '31', '41', '50plus', '36'])]
data_bar_gt25_yes = data_bar_gt25.loc[data_bar_gt25.Y == 1]
data_bar_gt25_yes.info()

# acceptance rate between drivers who go to a bar more than once a month and are over the age of 25 to the all others
gt1_bar25 = data_bar_gt25['Bar'].value_counts()['1~3'] + data_bar_gt25['Bar'].value_counts()['4~8'] + data_bar_gt25['Bar'].value_counts()['gt8']
gt1_bar25_yes = data_bar_gt25_yes['Bar'].value_counts()['1~3'] + data_bar_gt25_yes['Bar'].value_counts()['4~8'] + data_bar_gt25_yes['Bar'].value_counts()['gt8']
gt1_bar25_accept = gt1_bar25_yes / gt1_bar25
gt1_bar25_accept # 61.74%

bar_others = len(data_bar.index) - gt1_bar25
bar_others_yes = len(data_bar_yes.index) - gt1_bar25_yes
bar_others_accept = bar_others_yes / bar_others
bar_others_accept # 55.40%

# Observation: Acceptance rate between drivers who go to a bar more than once a month and are over the age of 25 is 61.74 % as compared to 55.40% for all others

# dataset of driver who go to bars more than once a month
data_bar_gt1 = data_bar.loc[data_bar['Bar'].isin(['1~3', '4~8', 'gt8'])]
data_bar_gt1_yes = data_bar_gt1.loc[data_bar_gt1.Y == 1]
data_bar_gt1.info()

# drivers: going more than once, no child passages, not farmers
data_bar_gt1_pass_occ = data_bar_gt1.loc[data_bar_gt1['passanger'].isin(['Alone', 'Friend(s)', 'Partner'])].loc[data_bar_gt1['occupation'] != 'Farming Fishing & Forestry']
data_bar_gt1_pass_occ_yes = data_bar_gt1_pass_occ.loc[data_bar_gt1_pass_occ.Y == 1]

gt1_pass_occ_accept = len(data_bar_gt1_pass_occ_yes.index) / len(data_bar_gt1_pass_occ.index)
gt1_pass_occ_accept #61.96%

# drivers other than: going more than once, no child passages, not farmers
gt1_pass_occ_others = len(data_bar.index) - len(data_bar_gt1_pass_occ.index)
gt1_pass_occ_others_yes = len(data_bar_yes.index) - len(data_bar_gt1_pass_occ_yes.index)
gt1_pass_occ_others_accept = gt1_pass_occ_others_yes / gt1_pass_occ_others
gt1_pass_occ_others_accept # 54.67%

# go to bars more than once a month, had passengers that were not a kid, and were not widowed 
data_bar_gt1_pass_nw = data_bar_gt1.loc[data_bar_gt1['passanger'].isin(['Alone', 'Friend(s)', 'Partner'])].loc[data_bar_gt1['maritalStatus'] != 'Widowed']
data_bar_gt1_pass_nw_yes = data_bar_gt1_pass_nw.loc[data_bar_gt1_pass_nw.Y == 1]
gt1_pass_nw_accept = len(data_bar_gt1_pass_nw_yes.index) / len(data_bar_gt1_pass_nw.index)
gt1_pass_nw_accept   # 61.96%

# go to bars more than once a month and are under the age of 30
data_bar_gt1_u30 = data_bar_gt1.loc[data_bar_gt1['age'].isin(['21', '26', 'below21'])]
data_bar_gt1_u30_yes = data_bar_gt1_u30.loc[data_bar_gt1_u30.Y == 1]
gt1_pass_u30_accept = len(data_bar_gt1_u30_yes.index) / len(data_bar_gt1_u30.index)
gt1_pass_u30_accept # 62.84%

# go to cheap restaurants more than 4 times a month and income is less than 50K.
data_bar_cheap_rest = data_bar.loc[data_bar['RestaurantLessThan20'].isin(['4~8', 'gt8'])].loc[data_bar['income'].isin(['Less than $12500', '$12500 - $24999', '$25000 - $37499', '$37500 - $49999'])]
data_bar_cheap_rest_yes = data_bar_cheap_rest.loc[data_bar_cheap_rest.Y == 1]
data_bar_cheap_rest.info()

gt1_pass_cheap_rest_accept = len(data_bar_cheap_rest_yes.index) / len(data_bar_cheap_rest.index)
gt1_pass_cheap_rest_accept # 60.07%


