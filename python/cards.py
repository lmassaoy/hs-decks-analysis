import pandas as pd

import streamlit as st
from PIL import Image


all_cards = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.json"
collectible_cards = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.collectible.json"
hs_logo = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/logos/hearthstone_title.png"
cards_photo = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/hearthstone_cards_sample.png"

hs_logo_image = Image.open(hs_logo)
cards_image = Image.open(cards_photo)

st.title("Hearthstone Cards - Exploration Module")
st.image(cards_image, use_column_width=True)

@st.cache
def generate_json_df(file_path):
    return pd.read_json(file_path)

cards_df = generate_json_df(collectible_cards)


# --------------- Filters ---------------
st.sidebar.header("**Filters**")


specific_card_text = st.sidebar.text_input('Card Name')


@st.cache()
def get_list_card_class(dataframe):
    return dataframe["cardClass"].drop_duplicates().values.tolist()

list_class = get_list_card_class(cards_df)
class_multiselect = st.sidebar.multiselect('Classes',list_class,list_class)


@st.cache
def get_list_rarity(dataframe):
    return dataframe["rarity"].drop_duplicates().values.tolist()

list_rarity = get_list_rarity(cards_df)
rarity_multiselect = st.sidebar.multiselect('Rarity',list_rarity,list_rarity)


@st.cache
def get_list_type(dataframe):
    return dataframe["type"].drop_duplicates().values.tolist()

type_rarity = get_list_type(cards_df)
type_multiselect = st.sidebar.multiselect('Type',type_rarity,type_rarity)


@st.cache()
def get_min_max_costs(dataframe):
    min_card_cost = dataframe["cost"].min()
    max_card_cost = dataframe["cost"].max()
    return {"min": min_card_cost, "max": max_card_cost}

dict_min_max_cost = get_min_max_costs(cards_df)
min_card_cost = int(dict_min_max_cost["min"])
max_card_cost = int(dict_min_max_cost["max"])

cost_slider = st.sidebar.slider('Card Cost',min_card_cost,max_card_cost,[min_card_cost,max_card_cost],1)


st.sidebar.header("**Card Selection**")


@st.cache
def get_list_cards(dataframe):
    return dataframe["name"].drop_duplicates().values.tolist()

list_cards = sorted(get_list_cards(cards_df))
specific_card_selectbox = st.sidebar.selectbox('Select a card',list_cards)

# --------------- Dataframe ---------------

st.subheader(f"DF Size: {len(cards_df.index)} :speak_no_evil:")
st.subheader("Sample data")


if specific_card_text != '':
    cards_df = cards_df[cards_df['name'] == specific_card_text]
else:
    cards_df = cards_df[cards_df['cardClass'].isin(class_multiselect)
                    & cards_df['rarity'].isin(rarity_multiselect)
                    & cards_df['type'].isin(type_multiselect)
                    & cards_df['cost'].between(cost_slider[0], cost_slider[1])]

st.dataframe(cards_df.head(100))

st.image(hs_logo_image, use_column_width=True)