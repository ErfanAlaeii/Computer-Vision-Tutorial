# Importing necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Loading the dataset
data = load_iris()
X = data.data
y = data.target

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Defining a function to build and evaluate different models
def evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        'Random Forest': RandomForestClassifier(),
        'SVM': SVC(),
        'K-Nearest Neighbors': KNeighborsClassifier()
    }

    param_grids = {
        'Random Forest': {
            'clf__n_estimators': [50, 100, 200],
            'clf__max_depth': [None, 10, 20]
        },
        'SVM': {
            'clf__C': [0.1, 1, 10],
            'clf__gamma': ['scale', 'auto']
        },
        'K-Nearest Neighbors': {
            'clf__n_neighbors': [3, 5, 7],
            'clf__weights': ['uniform', 'distance']
        }
    }

    best_estimators = {}

    for model_name, model in models.items():
        print(f"Training {model_name}...")

        # Creating a pipeline for standardization and classification
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', model)
        ])

        # Using GridSearchCV to find the best hyperparameters
        grid_search = GridSearchCV(pipeline, param_grids[model_name], cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Best estimator
        best_estimator = grid_search.best_estimator_
        best_estimators[model_name] = best_estimator

        # Predictions and evaluation
        y_pred = best_estimator.predict(X_test)

        print(f"Best parameters for {model_name}: {grid_search.best_params_}")
        print(f"Accuracy for {model_name}: {accuracy_score(y_test, y_pred):.2f}")
        print(f"Classification report for {model_name}:\n{classification_report(y_test, y_pred)}")
        print(f"Confusion matrix for {model_name}:\n{confusion_matrix(y_test, y_pred)}\n")

    return best_estimators


# Evaluating models and getting the best estimators
best_models = evaluate_models(X_train, X_test, y_train, y_test)

# Saving the best model (for example, Random Forest)
best_model = best_models['Random Forest']
joblib.dump(best_model, 'best_random_forest_model.pkl')
print("Best model saved as 'best_random_forest_model.pkl'.")

# To load the model in future, you can use:
# loaded_model = joblib.load('best_random_forest_model.pkl')
