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

This data app you are about to explore is about decks and the cards used to build them. You can drive yourself through the data by using the filters on the left panel. Every filter applied will reflect over the dataframe (which shows a sample of the data) and the data visualizations.

You can initialize it by running:
```
$ streamlit run python/decks.py
```

### [Popular Cards](https://github.com/lmassaoy/hs-decks-analysis/blob/master/python/popular_cards.py)
[![hearthstone-post.gif](https://i.postimg.cc/N0kJ4mty/hearthstone-post.gif)](https://postimg.cc/nsMGVsCZ)

This data app you are about to explore is about the most used cards, seeing cards' details and their presence in the decks built in Hearthpwn.

Here you go:
```
$ streamlit run python/popular_cards.py
```

Screenshot of the app

[![popular-cards-screenshot.png](https://i.postimg.cc/ncFYqrcz/popular-cards-screenshot.png)](https://postimg.cc/Z0QdSTNt)

### Running in a container
Coming soon :)
