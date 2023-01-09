
## Latent intent classifier for car make and model
**Available online [here](https://car-intent.herokuapp.com/search?phrase=ferrari%20italia).**
It is a GET endpoint returning JSON like:

`https://car-intent.herokuapp.com/search?phrase=ferrari italia`
```json
{
  "make":"FERRARI",
  "model":"458"
}
```
## Method
#### Classification
Classification happens using Complement Naive Bayes classifier 
which performs slightly better then a regular Multinomial Naive Bayes in imbalanced datasets (Rennie et al., 2003). 
There are about 480 classes, and 15 000 training examples, 
with an imbalanced distribution of classes. 
The algorithm can and should be simple for this many classes and a small examples/class ratio. 
I found Naive Bayes most appropriate.

**Accuracy of the model trained on ~ 12 000 examples is 0.896**

Full code for generating the model is available as a 
**[notebook](https://gitlab.com/team4hire-open-source/car-intent-classifier/-/blob/master/model_training/train_model.ipynb)**

There is no direct detection of the make nor the 
model in this classifier. Everything the model knows, it has "learned" from the queries.

#### Vectorization
The queries are vectorized using count vectorizer with a vocabulary of
unigrams and bigrams that occured in the existing queries. 
In other words, I took the "bag of n-grams" approach. 
Partially disregarding the order of phrases in mining search queries does 
not have a significant negative effect on performance (Yin, Wenpeng, et al.,  2017).
It is also a very simple approach.

It may be interesting to explore entropy-based slimming of the vocabulary,
but for now it is a full set.

#### Labelling
The label set comes from https://autotrader.co.uk/ 
([script](https://gitlab.com/team4hire-open-source/car-intent-classifier/-/blob/master/model_training/get_make_and_model.py))
The dataset was labelled based on which, if any, make and model of the car 
occured in the URL of the web page. 
I used those URLs that contained only one make and model (about 15 000).

#### Correcting typos
To account for typos, every word is substituted with its closest match from the vocabulary,
measured with edit distance, with an arbitrary maximum cutoff distance.

#### Performance
The classification with Naive Bayes is fast both in training and classification (about 100-150ms). 
The requests take extra 2s per word with a typo. 
The slow part is fuzzy matching of the phrases with the known vocabulary. 
In production I would probably use Elastic's 
[fuzzy query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html) 
to match the correct the search phrases quicker or have a "most common typos and fixes" store.

 ## Development
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```
Run a development server
```
flask run
```
 
 ### Examples I like:
```
a1 => {"make":"AUDI","model":"A1"}
dino => {"make":"FERRARI","model":"246"}
Jeep reneade => {"make":"JEEP","model":"RENEGADE"}
daytona => {"make":"DODGE","model":"CHARGER"}
chevy ss => {"make":"CHEVROLET","model":"CAMARO"}
range river discovery => {"make":"LAND ROVER","model":"DISCOVERY"} #the Defender was not in the label set
porsche 4x4 => {"make":"PORSCHE","model":"CAYENNE"}
```

### Examples I like less:
```
toyota 4x4 => {"make":"FORD","model":"F150"} # also 4x4
fast ford => {"make":"INFINITI","model":"G"}
```

### References:

Rennie, J. D., Shih, L., Teevan, J., & Karger, D. R. (2003). Tackling the poor assumptions of naive bayes text classifiers. In ICML (Vol. 3, pp. 616-623). https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf

Yin, Wenpeng, et al. “Comparative Study of CNN and RNN for Natural Language Processing.” ArXiv:1702.01923 [Cs], Feb. 2017. arXiv.org, http://arxiv.org/abs/1702.01923.

first draft of model generation was based on: https://towardsdatascience.com/naive-bayes-document-classification-in-python-e33ff50f937e
