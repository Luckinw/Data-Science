import pandas as pd  # Importing the pandas library for data manipulation
import numpy as np  # Importing the numpy library for numerical operations
from sklearn.model_selection import train_test_split  # Importing train_test_split function from sklearn.model_selection

data = 'titanic.csv'  # Specify the path to the Titanic dataset
df = pd.read_csv(data, encoding='utf-8')  # Read the CSV file into a pandas DataFrame, specifying the encoding as 'utf-8'

# Remove unnecessary columns ('name', 'cabin', 'ticket', 'fare', 'boat', 'body', 'home.dest') and drop rows with missing values
df = df.drop(['name', 'cabin', 'ticket', 'fare', 'boat', 'body', 'home.dest'], axis=1).dropna()

embarked = {'C': 0, 'Q': 1, 'S': 2}  # Create a dictionary mapping 'C', 'Q', 'S' to 0, 1, 2 respectively
sex = {'male': 0, 'female': 1}  # Create a dictionary mapping 'male' and 'female' to 0 and 1 respectively

df['embarked'] = df['embarked'].map(embarked)  # Map 'embarked' column values using the 'embarked' dictionary
df['sex'] = df['sex'].map(sex)  # Map 'sex' column values using the 'sex' dictionary

x = df.drop(['survived'], axis=1).dropna()  # Create input features (x) by dropping the 'survived' column and any remaining rows with missing values
y = df['survived'].dropna()  # Create the target variable (y) by selecting the 'survived' column and dropping any rows with missing values

# Split the data into training and testing sets using train_test_split function, with a test size of 0.2 (20% of the data) and a random state of 42 for reproducibility
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)

from sklearn.linear_model import LogisticRegression  # Importing the LogisticRegression class from sklearn.linear_model

log = LogisticRegression()  # Create an instance of the LogisticRegression model

log.fit(x_train, y_train)  # Fit the model to the training data

def if_survive(pclass, sex, age, sibsp, parch, embarked):
    data = [pclass, sex, age, sibsp, parch, embarked]  # Create a list of input data
    columns = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'embarked']  # Define the column names
    df = pd.DataFrame([data], columns=columns)  # Create a new DataFrame with the input data
    return "Congratulations, you've just won a one-way trip to the 'Resting in Pieces' resort!" if int(log.predict(df)[0]) == 0 else 'You took the blows and kept standing tall. Surviving like a champ!'  # Predict survival using the logistic regression model and return the corresponding message
