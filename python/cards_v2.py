import pandas as pd
import streamlit as st
from PIL import Image
import json


all_cards = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.json"
collectible_cards = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.collectible.json"
hs_logo = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/logos/hearthstone_title.png"
cards_photo = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/hearthstone_cards_sample.png"

hs_logo_image = Image.open(hs_logo)
cards_image = Image.open(cards_photo)


st.image(hs_logo_image, use_column_width=True)
st.title("Cards - Exploration Module")
st.image(cards_image, use_column_width=True)

@st.cache
def generate_json_df(file_path):
    return pd.read_json(file_path)

cards_df = generate_json_df(all_cards)

with open(all_cards) as f:
  dict_cards = json.load(f)


# --------------- Card Selection (Sidebar) ---------------

st.sidebar.header("**Filters**")

specific_card_text = st.sidebar.text_input("Card Name")


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
def get_list_set(dataframe):
    return dataframe["set"].drop_duplicates().values.tolist()

list_set = get_list_set(cards_df)
set_multiselect = st.sidebar.multiselect('Set',list_set,list_set)


@st.cache
def get_list_race(dataframe):
    return dataframe["race"].drop_duplicates().values.tolist()

list_race = get_list_race(cards_df)
race_multiselect = st.sidebar.multiselect('Race',list_race,list_race)


@st.cache
def get_list_type(dataframe):
    return dataframe["type"].drop_duplicates().values.tolist()

list_type = get_list_type(cards_df)
type_multiselect = st.sidebar.multiselect('Type',list_type,list_type)


elite_checkbox = st.sidebar.checkbox('Only elite cards?')


@st.cache()
def get_min_max_costs(dataframe):
    min_card_cost = dataframe["cost"].min()
    max_card_cost = dataframe["cost"].max()
    return {"min": min_card_cost, "max": max_card_cost}

dict_min_max_cost = get_min_max_costs(cards_df)
min_card_cost = int(dict_min_max_cost["min"])
max_card_cost = int(dict_min_max_cost["max"])

cost_slider = st.sidebar.slider('Card Cost',min_card_cost,max_card_cost,[min_card_cost,max_card_cost],1)


@st.cache()
def get_min_max_attack(dataframe):
    min_card_attack = dataframe["attack"].min()
    max_card_attack = dataframe["attack"].max()
    return {"min": min_card_attack, "max": max_card_attack}

dict_min_max_attack = get_min_max_attack(cards_df)
min_card_attack = int(dict_min_max_attack["min"])
max_card_attack = int(dict_min_max_attack["max"])

attack_slider = st.sidebar.slider('Attack',min_card_attack,max_card_attack,[min_card_attack,max_card_attack],1)


@st.cache()
def get_min_max_health(dataframe):
    min_card_health = dataframe["health"].min()
    max_card_health = dataframe["health"].max()
    return {"min": min_card_health, "max": max_card_health}

dict_min_max_health = get_min_max_health(cards_df)
min_card_health = int(dict_min_max_health["min"])
max_card_health = int(dict_min_max_health["max"])

health_slider = st.sidebar.slider('Health',min_card_health,max_card_health,[min_card_health,max_card_health],1)


# --------------- Dataframe ---------------

kpis = f"""
### **Classes**: {len(list_class)} |  **Rarity**: {len(list_rarity)} | **Set**: {len(list_set)} | **Race**: {len(list_race)} | **Type**: {len(list_type)}
"""
st.markdown(kpis)


st.header("**Cards Dataframe**")
st.text("Use the filters in the left to explore the dataframe")


if specific_card_text != '':
    sample_df = cards_df[cards_df['name'].str.contains(specific_card_text)]
else:
    sample_df = cards_df[cards_df['cardClass'].isin(class_multiselect)
                    & cards_df['rarity'].isin(rarity_multiselect)
                    & cards_df['type'].isin(type_multiselect)
                    & cards_df['set'].isin(set_multiselect)
                    & cards_df['race'].isin(race_multiselect)]


if elite_checkbox:
    sample_df = sample_df[sample_df['elite'] == 1]

if cost_slider[0]!=min_card_cost or cost_slider[1]!=max_card_cost:
    sample_df = sample_df[sample_df['cost'].between(cost_slider[0], cost_slider[1])]

if attack_slider[0]!=min_card_attack or attack_slider[1]!=max_card_attack:
    sample_df = sample_df[sample_df['attack'].between(attack_slider[0], attack_slider[1])]

if health_slider[0]!=min_card_health or health_slider[1]!=max_card_health:
    sample_df = sample_df[sample_df['health'].between(health_slider[0], health_slider[1])]


st.dataframe(sample_df)

st.write("**Full DF Size**: ", len(cards_df.index), " | ", "**Filtered DF Size**: ", len(sample_df.index))

# --------------- Card Selection ---------------

st.sidebar.header("**Card Selection**")

@st.cache
def get_list_cards(dataframe):
    return dataframe["name"].drop_duplicates().values.tolist()

list_cards = sorted(get_list_cards(cards_df))
specific_card_selectbox = st.sidebar.selectbox('Select a card',list_cards)

specific_card_index = cards_df.index[cards_df["name"] == specific_card_selectbox].tolist()

card_id = cards_df["id"][cards_df["name"] == specific_card_selectbox].tolist()[0] + '.png'
image_render_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/cards/renders/256x/"

card_image = Image.open(image_render_path+card_id)

st.sidebar.image(card_image)

st.sidebar.subheader("**Card - Json Object**")

st.sidebar.json(dict_cards[specific_card_index[0]])