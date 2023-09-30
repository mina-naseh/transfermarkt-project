#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

# In[2]:


df = pd.read_csv("total_players_data.csv")
df.sample(4)


# In[3]:


df.drop(
    [
        "Unnamed: 0",
        "player_id",
        "season",
        "team_id",
        "player_name",
        "birthdate",
        "national_team",
        "agent_name",
    ],
    axis=1,
    inplace=True,
)
df.head(2)


# In[4]:


med_height = df["height"].median()
med_age = df["age"].median()


# In[5]:


df = df.dropna(subset=["market_value"])
df["goals"].fillna(0, inplace=True)
df["own_goals"].fillna(0, inplace=True)
df["yellow_cards"].fillna(0, inplace=True)
df["red_cards"].fillna(0, inplace=True)
df["player_app"].fillna(0, inplace=True)
df["age"].fillna(med_age, inplace=True)
df["foot"].fillna(value="right", inplace=True)
df["height"].fillna(value=med_height, inplace=True)
df["main_position"].fillna(value="unknown", inplace=True)
df.sample(3)


# In[6]:


df.isna().sum()


# In[7]:


df["main_position"].value_counts()


# In[8]:


df = df[df["main_position"] != "unknown"]
df["main_position"].value_counts()


# In[9]:


class_maps = {
    "Forward": ["Centre-Forward", "Second Striker", "Attack"],
    "Midfielder": [
        "Central Midfield",
        "Defensive Midfield",
        "Attacking Midfield",
        "Left Midfield",
        "Right Midfield",
        "midfield",
    ],
    "Defender": ["Defender", "Centre-Back", "Right-Back", "Left-Back"],
    "Winger": ["Right Winger", "Left Winger"],
    "Goalkeeper": ["Goalkeeper"],
}
for key, value in class_maps.items():
    df["main_position"] = df["main_position"].apply(lambda x: key if x in value else x)
df["main_position"].value_counts()


# In[10]:


# def create_dict(lst):
#   return {value:index for index, value in enumerate(lst)}


# In[11]:


# df['main_position']=df['main_position'].map(create_dict(df['main_position'].unique()))


# In[12]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["main_position"] = le.fit_transform(df["main_position"])
classes_ = list(le.classes_)
print(classes_)
le = LabelEncoder()
df["foot"] = le.fit_transform(df["foot"])


# In[13]:


df["main_position"].value_counts()


# # Normalization

# * because we know maximum of everything in the history of footbal in this task, we can divide all the dataframes by their maximums

# In[14]:


df.columns


# In[15]:


cols = [
    "market_value",
    "height",
    "foot",
    "age",
    "assists",
    "yellow_cards",
    "red_cards",
    "injury",
    "player_app",
    "goals",
    "own_goals",
]
df[cols] = df[cols].apply(
    lambda col: col / col.max() if col.name != "main_position" else col
)
df.head(5)


# # Split

# In[16]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(df, test_size=0.1, random_state=46)
print("Number of Train data:", len(train))
print("Number of Test data:", len(test))


# In[17]:


x_train = train.drop("main_position", axis=1)
y_train = train["main_position"]
x_test = test.drop("main_position", axis=1)
y_test = test["main_position"]


# #Apply SVM Grid search

# * we first find how much time one iteration will take and set reasonable number of params for the grid search

# In[18]:


import time

from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# In[19]:


t_start = time.time()
clf = SVC(kernel="linear", random_state=42)
clf.fit(x_train, y_train)
print(time.time() - t_start)


# In[20]:


chosen_arams = {
    "C": [0.1, 1, 10, 100],
    "gamma": ["scale", "auto", 0.1, 1, 10, 100],
    # 'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
    # 'degree':[2, 3, 4]
}


# * this will be run 360x5 times and will find the best params

# In[21]:


t_start = time.time()
svc = SVC(random_state=42)
# 5 fold cross validation
grid_search = GridSearchCV(svc, chosen_arams, cv=5)

grid_search.fit(x_train, y_train)

print("Best params->", grid_search.best_params_)
print("Cros validation score->", grid_search.best_score_)
print("Elapsed Time->", time.time() - t_start, "seconds")


# In[23]:


clf = SVC(C=10, gamma=10, random_state=42)
clf.fit(x_train, y_train)


# In[24]:


from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

y_pred = clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")
print("f1 score", f1)
print("accuracy", accuracy)
print("precision", precision)
print("recall", recall)


# In[ ]:
