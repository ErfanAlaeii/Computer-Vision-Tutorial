# Import necessary libraries
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Load the saved model
model = joblib.load('best_random_forest_model.pkl')

# Assume we have new data for prediction
# Example new data (the shape should be (n_samples, n_features))
new_data = np.array([
    [5.1, 3.5, 1.4, 0.2],  # Sample 1
    [6.7, 3.0, 5.2, 2.3]   # Sample 2
])

# The saved model includes preprocessing, so we can directly use it
predictions = model.predict(new_data)

# Output predictions
print("Predictions for the new data:")
print(predictions)



# If you want to see the predicted class labels:
class_names = ['setosa', 'versicolor', 'virginica'] 
predicted_labels = [class_names[p] for p in predictions]
print("Predicted class labels:")
print(predicted_labels)
