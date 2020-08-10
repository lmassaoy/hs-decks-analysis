# Hearthstone Decks Analysis

[![hs-decks-analysis-README.png](https://i.postimg.cc/WzW15w9f/hs-decks-analysis-README.png)](https://postimg.cc/V0tw6nPj)

**Medivh** is calling you to join us in a journey through Karazhan, to experience something ***new***.

This project is a POC of data analysis using [Streamlit](https://www.streamlit.io/) to support us on the data exploration, reading data from decks built on [Hearthpwn](https://www.hearthpwn.com/) using [pandas](https://pandas.pydata.org/) and with help of the open API [hearthstonejson](https://hearthstonejson.com/) to enhance data about the cards.
The main dataset we'll be using here was downloaded from [Kaggle](https://www.kaggle.com/romainvincent/history-of-hearthstone), so I'd to thanks the creator of this dataset for share it with us, allowing us to navigate and analyze 3 years of deck building.

Please enjoy :)

## Running local
Make sure you install everything necessary (available in [requirements.txt](https://github.com/lmassaoy/hs-decks-analysis/blob/master/devops/requirements.txt)).

## Data Apps
### [Decks](https://github.com/lmassaoy/hs-decks-analysis/blob/master/python/decks.py)
[![cards-decks.png](https://i.postimg.cc/ZqcYWjDn/cards-decks.png)](https://postimg.cc/p9mM7QvM)

This data app is about to explore decks and the cards used to build them.
You can drive yourself through the data by using the filters on the left panel. Every filter applied will reflect over the dataframe (which shows a sample of the data) and the data visualizations.
You can initialize it by running:
```
$ streamlit run python/decks.py
```

### [Popular Cards](https://github.com/lmassaoy/hs-decks-analysis/blob/master/python/popular_decks.py)
[![OG-317.png](https://i.postimg.cc/K8k1P35f/OG-317.png)](https://postimg.cc/87GkD59f) [![WE1-036.png](https://i.postimg.cc/xqr1gt5P/WE1-036.png)](https://postimg.cc/7JV4Z1pC) [![AT-072.png](https://i.postimg.cc/RhtHM3bX/AT-072.png)](https://postimg.cc/jns5cjT7)

This data app is about to explore the most used cards, seeing cards' details and their presence in the decks built in Hearthpwn.
Here you go:
```
$ streamlit run python/popular_decks.py
```

### Running in a container
Coming soon :)

