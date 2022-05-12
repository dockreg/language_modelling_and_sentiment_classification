#!/usr/bin/env python

import glob
import os
import math
import re
import csv
import random

def train_test():
    train = []
    test = []
    
    neg_path = 'review_polarity/txt_sentoken/neg/'

    #negative data
    os.chdir(neg_path)
    for file in os.listdir():
        #find test data
        if file[2]=='9':
            with open(file, 'r') as f:
                text = f.read()
                text = text.lower()
                text = re.sub(r'[^\w\s]','',text)
                text = text.replace("\n", "")
                test.append([file, text, 0])
        #find training data
        else:
            with open(file, 'r') as f:
                text = f.read()
                text = text.lower()
                text = re.sub(r'[^\w\s]','',text)
                text = text.replace("\n", "")
                train.append([file, text, 0])

    #positive data
    pos_path = '../../../review_polarity/txt_sentoken/pos/'
    os.chdir(pos_path)
    for file in os.listdir():
        #find test data
        if file[2]=='9':
            with open(file, 'r') as f:
                text = f.read()
                text = text.lower()
                text = re.sub(r'[^\w\s]','',text)
                text = text.replace("\n", "")
                test.append([file, text, 1])
        #find training data
        else:
            with open(file, 'r') as f:
                text = f.read()
                text = text.lower()
                text = re.sub(r'[^\w\s]','',text)
                text = text.replace("\n", "")
                train.append([file, text, 1])

    return train, test



def count_classes(train):
    pos = 0
    neg = 0
    #loop through each review
    for review in train:
        #find incidence where sentiment is positive
        if review[2]==1:
            pos+=1
        else:
            neg+=1
            
    return pos, neg, pos+neg



def count_words(reviews):
    pos_word_frequencies = {}
    neg_word_frequencies = {}
    total_vocab_frequencies = {}

    for review in reviews:        
        #find positive reviews
        if review[2]==1:
            words = review[1].strip().split()
            for word in words:
                if word in pos_word_frequencies:
                    pos_word_frequencies[word] += 1
                else:
                    pos_word_frequencies[word] = 1

                if word in total_vocab_frequencies:
                    total_vocab_frequencies[word] += 1
                else:
                    total_vocab_frequencies[word] = 1
                    
        #negative reviews
        else:
            words = review[1].strip().split()
            for word in words:
                if word in neg_word_frequencies:
                    neg_word_frequencies[word] += 1
                else:
                    neg_word_frequencies[word] = 1

                if word in total_vocab_frequencies:
                    total_vocab_frequencies[word] += 1
                else:
                    total_vocab_frequencies[word] = 1

    return pos_word_frequencies, neg_word_frequencies, total_vocab_frequencies



def naive_bayes(train, test):

    #training phase
    pos_loglikelihood = {}
    neg_loglikelihood = {}
    count_pos, count_neg, total_docs = count_classes(train)
    prior_pos = math.log(count_pos/total_docs)
    prior_neg = math.log(count_neg/total_docs)
    pos_dict, neg_dict, full_vocab_dict = count_words(train)
    #print(len(pos_dict), len(neg_dict), len(full_vocab_dict), total_count)


    #add positive log likelihoods
    pos_sum_counts = sum(pos_dict.values())
    for word in pos_dict:
        pos_loglikelihood[word] = math.log((pos_dict[word]+1)/(pos_sum_counts+len(full_vocab_dict)))

    neg_sum_counts = sum(neg_dict.values())
    #add negative log likelihoods
    for word in neg_dict:
        neg_loglikelihood[word] = math.log((neg_dict[word]+1)/(neg_sum_counts+len(full_vocab_dict)))

    #add likelihood for words in vocab but not in one of the dictionaries
    pos_keys = pos_dict.keys()
    neg_keys = neg_dict.keys()
    all_vocab_keys = full_vocab_dict.keys()

    #find words present in main vocab but not in positive vocab and vice versa
    pos_diff = all_vocab_keys - pos_keys
    neg_diff = all_vocab_keys - neg_keys
    
    for word in pos_diff:
        pos_loglikelihood[word] = math.log(1/(pos_sum_counts + len(full_vocab_dict)))
             
    for word in neg_diff:
        neg_loglikelihood[word] = math.log(1/(neg_sum_counts + len(full_vocab_dict)))


    #testing phase
    accurate_prediction = 0
    for review in test:
        
        pos_prob, neg_prob = 0, 0
        words = review[1].strip().split()
        for word in words:
            if word in full_vocab_dict:
                if word in pos_loglikelihood:
                    pos_prob += pos_loglikelihood[word]
                if word in neg_loglikelihood:
                    neg_prob += neg_loglikelihood[word]

        pos_prob += prior_pos
        neg_prob += prior_neg
        if pos_prob > neg_prob:
            review.append(1)
        else:
            review.append(0)
            
        if review[2]==review[3]:
            accurate_prediction+=1
        
    total_test_reviews = len(test)
    accuracy = 'The Accuracy of the Naive Bayes sentiment polarity classifier is: ' + str((accurate_prediction / total_test_reviews)*100) + '%'


    return accuracy, test


def output_samples(good, bad):
        with open('../../../ANALYSIS.md', 'w') as f:
            f.write('# Analysis of Sentiment Classifier \n \n')

            f.write('## Correct Predictions: \n \n')
            for review in good:
                sentiment = 'Positive' if review[2] == 1 else 'Negative'
                predicted = 'Positive' if review[3] == 1 else 'Negative'
                f.write('### Filename: '+ review[0] + '\n### Sentiment: '+ sentiment + '\n### Predicted: '+predicted +' \n \n### Review: \n')
                f.write(review[1] + '\n \n')

            f.write('\n \n \n \n \n ## Incorrect Predictions: \n \n')
            for review in bad:
                sentiment = 'Positive' if review[2] == 1 else 'Negative'
                predicted = 'Positive' if review[3] == 1 else 'Negative'
                f.write('### Filename: '+ review[0] + '\n### Sentiment: '+ sentiment+ '\n### Predicted: '+predicted +' \n \n### Review: \n') 
                f.write(review[1] + '\n \n')

            f.write('## Conclusion')

def sample_results(predictions):
    correct = []
    incorrect = []
    for row in predictions:
        if row[2]==row[3]:
            correct.append(row)
        else:
            incorrect.append(row)

    correct_5 = random.sample(correct, 5)
    incorrect_5 = random.sample(incorrect, 5)

    return correct_5, incorrect_5

    
def main():
    train, test = train_test()
    results, predictions = naive_bayes(train, test)
    print(results)
    correct, incorrect = sample_results(predictions)
    output_samples(correct, incorrect)

        

    
     
if __name__ == '__main__':
    main()
