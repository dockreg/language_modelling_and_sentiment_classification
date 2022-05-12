## CA4023 Part 3 - Naive Bayes Sentiment Polarity Classifier

This section of the assignment creates a sentiment polarity classifier model using Naive Bayes to determine the sentiment of a colection of movie reviews.

The data used for this section can be found at https://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz and contains 100 positive rviews and 100 negative reviews. The data has been split into training and testing with the final 100 files from each folder used as the tst set (files starting with CV9).

The model is case insensitive and ignores punctuation and predicts the likelihood of the sentiment being Positive (1) or Negative (0) based on the words used in the review. The program also outputs a random selection of correct predictions and incorrect predictions to the ANALYSIS.md file for further inspection.

### Running the code

To run this code:

```
git clone https://gitlab.computing.dcu.ie/dockreg2/ca4023_assignment_1.git
cd part_3
python3 nb_sentiment_polarity_classifier.py
```

*ensure the data has been downloaded and moved to ca4023_assignment_1/part_3/*

This will output an accuracy score and will write to the ANALYSIS.md file with the randomly chosen correct and incorrect results.

### Results

The accuracy for this model is **83.5%**. The model can be found in the `nb_sentiment_polarity_classifier.py` file and there is also a jupyter notebook `naive_bayes_sentiment_classifier.ipynb` that provides further insight into the functions used and concepts behind Naive Bayes and its use in this task.

