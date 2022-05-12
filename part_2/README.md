## CA4023 Part 2 - Unsmoothed Bigram Language Model

This section of the assignment involves creating a bigram language model built from the `train.txt` data and is used on the `test.txt` data.

It assigns probabilities to each sentence using log probabilities and does not involve any smoothing.

#### Running the code

To run this code:

```
git clone https://gitlab.computing.dcu.ie/dockreg2/ca4023_assignment_1.git
cd part_2
python3 bigram_language_model.py
```

This will output the following:

Unsmoothed Bigram Language Model:

- b has a probability of 0.38
- a has a probability of 0.38
- a b has a probability of 0.15
- a a has a probability of 0.15
- a b a has a probability of 0.06
