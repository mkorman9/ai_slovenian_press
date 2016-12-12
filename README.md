My solution for Slovenian articles classification challange from scicup.com
Solutions consist of following steps:
  - Text preprocessing
  - Feature extraction
  - Learning model creation
  - Prediction

Text processing is simply normalization and removing accents. Feature extraction
uses Bags of Words and learning model is MLP neural network containing 2 hidden layers
and using ReLu activation function.

Currently gives the best score of 89,7% on the testing set.  
Running generate_model.py will train network and save model.  
generate_output.py will use generated model and save predictions for testing set  
generate_commons_predictions.py will run prediction n-times and choose best approximation.

