#!/usr/bin/env python

import math

def count_words_and_pairs(text):
    counts = {}
    word_pairs = {}
    for line in text:
        words = line.strip().split(' ')
        for key in words:
            if key in counts:
                counts[key] += 1
            else:
                counts[key] = 1
                
        for i in range(len(words)-1):
            if (words[i], words[i+1]) in word_pairs:
                word_pairs[(words[i], words[i+1])] += 1
            else:
                word_pairs[(words[i], words[i+1])] = 1
    return counts, word_pairs



def count_probabilities(word_counts, pairs_counts):
    prob = {}
    for k in pairs_counts:
        prob[k] = float(pairs_counts[k]/word_counts[k[0]])

    return prob



def sentence_probability(test_data, prob_dict):
    probability = []
    for line in test_data:
        temp = 0
        words = line.strip().split(' ')
        for i in range(len(words) - 1):
            temp += math.log(prob_dict[(words[i], words[i+1])])
        temp = math.pow(2, temp)
        probability.append(temp)

    return probability
            

    
def main():
    with open('train.txt', 'r') as f:
        text = f.readlines()
    counts, pairs = count_words_and_pairs(text)
    probabilities = count_probabilities(counts, pairs)
    with open('test.txt', 'r') as g:
        test_text = g.readlines()
    test_probability = sentence_probability(test_text, probabilities)
    print('Unsmoothed Bigram Language Model:\n---------------------------------')
    for i in range(len(test_probability)):
        print('{} has a probability of {:.2f}'.format(test_text[i].strip(), test_probability[i]))
    

        
if __name__ == '__main__':
    main()


