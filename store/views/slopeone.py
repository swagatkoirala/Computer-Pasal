from __future__ import division
from django.db import connection
import numpy as np
import pandas as pd

import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("db.sqlite3")

cur = con.cursor()
hari=cur.execute("SELECT * from store_customer")

ram = pd.DataFrame(hari)
ram.to_csv('data.csv')
# import pdb;pdb.set_trace()
# df = pd.read_sql_query("SELECT * from store_customers", con)
df=pd.read_csv('data.csv')
print(df.head())

# # The result of a "cursor.execute" can be iterated over by row
# for row in cur.execute('SELECT * FROM store_product;'):
#     print(row)

# Be sure to close the connection
con.close()
#Slope One Predictor
# def slope_one(eval_mat):
#     """
#     function implement slope one algorithm
#     @param rating matrix
#     @return predicted rating matrix
#     """
#     user_num = eval_mat.shape[0]
#     item_num = eval_mat.shape[1]
#     #get average deviation
#     def get_dev_val(i, j):
#         """
#         function to get deviation of item i and item j
#         @param item pair
#         @return deviation value
#         """
#         dev_val = 0
#         users = 0
#         for row in range(user_num):
#             #if the user evaluated both product i and product j
#             if((eval_mat[row][i] != 0) and (eval_mat[row][j] != 0)):
#                 users += 1
#                 dev_val += eval_mat[row][i] - eval_mat[row][j]
#         #avoid zero division
#         if(users == 0):
#             return 0
#         return dev_val / users

#     #get average diviation
#     dev = np.zeros((item_num, item_num))
#     for i in range(item_num):
#         for j in range(item_num):
#             if i == j:
#                 #to lessen time complexity
#                 break
#             else:
#                 # dev[i][j] = -dev[j][i]
#                 dev_temp = get_dev_val(i, j)
#                 dev[i][j] = dev_temp
#                 dev[j][i] = (-1) * dev_temp
#     #get predictive evaluation matrix
#     pred_mat = np.zeros((user_num, item_num))
#     for u in range(user_num):
#         #only get rated item
#         eval_row = np.where(eval_mat[u] != 0)[0]
#         for j in range(item_num):
#             pred_mat[u][j] = (np.sum(dev[j][eval_row] + eval_mat[u][eval_row])) / len(eval_row)
#     return pred_mat