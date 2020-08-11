import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import os
import altair as alt
import json
from utils.images_downloader import ImageRenderDownloader
import warnings


# Agent to download images if they do not exists
download_agent = ImageRenderDownloader(256)
# Disabling UserWarnings (Boolean Series key will be reindexed to match DataFrame index)
warnings.simplefilter(action='ignore', category=UserWarning)
# Setting timezone to avoid datetime issues with pandas
os.environ['TZ'] = 'UTC'


# Dataset files
decks_path = "data/datasets/decks/data.csv"
cards_path = "data/datasets/cards/cards.json"
class_details_path = "data/datasets/app_content/class_details.json"

# Image pathes
title_path = "data/images/design/popular_cards_title_2.png"
sidebar_title_path = "data/images/logos/hs_heroes_icons_small.png"
class_icons_path = "data/images/logos/"
cards_image_path = "data/images/cards/renders/256x/"
kpi_image_path = "data/images/design/kpi.png"
top_30_path = "data/images/design/top-30_2.png"


@st.cache
def generate_df(path,datatype):
    if datatype == "csv":
        return pd.read_csv(path)
    if datatype == "json":
        return pd.read_json(path)


@st.cache(allow_output_mutation=True)
def get_deck_class(df):
    return df["deck_class"].drop_duplicates().values.tolist()


def get_deck_archetype(df):
    return df["deck_archetype"][decks_df["deck_class"] == class_selectbox].drop_duplicates().values.tolist()


def get_class_icon(class_selectbox):
    return f"{class_icons_path}{class_selectbox.lower()}.png"


def get_class_hero_n_power(class_selected_details):
    hero_path = f'{cards_image_path}{class_selected_details["hero"]["card_id"]}.png'
    hero_power_path = f'{cards_image_path}{class_selected_details["hero"]["power_id"]}.png'
    return [hero_path,hero_power_path]


@st.cache
def melt_raw_df(df,id_vars,value_vars,var_name,value_name):
    return pd.melt(df, id_vars=id_vars, value_vars=value_vars, ignore_index=False, var_name=var_name, value_name=value_name)


def generate_enhancement_card_df(df):
    return df[["dbfId","id","name","rarity","type"]].drop_duplicates()


@st.cache()
def generate_enhanced_df(melted_decks_df,enhancement_card_df):
    enhanced_decks_df = pd.merge(melted_decks_df,enhancement_card_df,how="left",left_on='card_id',right_on='dbfId')
    rename_enhanced_dict = {"id": "hs_id","name": "card_name"}
    enhanced_decks_df = enhanced_decks_df.rename(columns=rename_enhanced_dict)
    enhanced_decks_df['date'] = enhanced_decks_df['date'].str[:10]
    enhanced_decks_df['date'] = pd.to_datetime(enhanced_decks_df['date'], format='%Y-%m-%d')
    filter_columns_enhanced_list = ['date','deck_archetype','deck_class','deck_id','title','card_index','card_id','hs_id','card_name','rarity','type']
    return enhanced_decks_df[filter_columns_enhanced_list].sort_values(by=['deck_id','date'], ascending=False)


@st.cache()
def generate_cards_appearance(df):
    cards_appearance = df[["card_name","deck_id"]].rename(columns={"card_name":"cardName","deck_id":"numberOfAppearance"}, errors="raise")
    return cards_appearance.groupby(['cardName']).numberOfAppearance.count().sort_values(ascending=False)


@st.cache()
def generate_cards_appearance_unique(df):
    cards_appearance = df[["hs_id","card_name","rarity","deck_id"]].rename(columns={"hs_id":"cardId","card_name":"cardName","rarity":"cardRarity","deck_id":"numberOfAppearance"}, errors="raise")
    return cards_appearance.fillna("NOT FOUND").groupby(['cardId','cardName','cardRarity']).numberOfAppearance.nunique().sort_values(ascending=False)


def build_image(path):
    return Image.open(path)


decks_df = generate_df(decks_path, "csv")
cards_df = generate_df(cards_path, "json")


with open(class_details_path, 'r') as f:
    class_dict = json.load(f)


# -------------- SIDEBAR --------------

st.sidebar.title("Class")
sidebar_title_image = build_image(sidebar_title_path)
st.sidebar.image(sidebar_title_image, use_column_width=True)


class_list = sorted(get_deck_class(decks_df))
class_selectbox = st.sidebar.selectbox("Select a class:",class_list,0)


class_selected = get_class_icon(class_selectbox)
class_image = build_image(class_selected)
st.sidebar.image(class_image, width=120)


class_selected_details = {}
for class_object in class_dict:
    if class_object["class"] == class_selectbox:
        class_selected_details = class_object
    

st.sidebar.header(class_selected_details["hero"]["subheader"])
st.sidebar.markdown(class_selected_details["hero"]["class_description"])
card_hero_selected_path = download_agent.download(class_selected_details["hero"]["card_id"])
card_hero_power_selected_path = download_agent.download(class_selected_details["hero"]["power_id"])


st.sidebar.subheader("Hero (default)")
if card_hero_selected_path is None:
    st.sidebar.text("Card image not found :sob:")
else:
    st.sidebar.image(build_image(card_hero_selected_path),width=256)


st.sidebar.subheader("Hero Power")
if card_hero_power_selected_path is None:
    st.sidebar.text("Card image not found :sob:")
else:
    st.sidebar.image(build_image(card_hero_power_selected_path),width=256)


deck_archetype_list = sorted(get_deck_archetype(decks_df))
deck_archetype_multiselect = st.sidebar.multiselect("Decks Archetypes:",deck_archetype_list)


# -------------- MAIN --------------

title_image = build_image(title_path)
st.image(title_image, width=600)


melt_id_vars = ['date','deck_archetype','deck_class','deck_id','title']
melt_value_vars = ['card_0','card_1','card_2','card_3','card_4','card_5','card_6','card_7',
                    'card_8','card_9','card_10','card_11','card_12','card_13','card_14','card_15',
                    'card_16','card_17','card_18','card_19','card_20','card_21','card_22','card_23',
                    'card_24','card_25','card_26','card_27','card_28','card_29']
melt_var_name = 'card_index'
melt_value_name = 'card_id'


if deck_archetype_multiselect != []:
    melted_decks_df = melt_raw_df(decks_df[decks_df["deck_class"] == class_selectbox][decks_df["deck_archetype"].isin(deck_archetype_multiselect)],melt_id_vars,melt_value_vars,melt_var_name,melt_value_name)
else:
    melted_decks_df = melt_raw_df(decks_df[decks_df["deck_class"] == class_selectbox],melt_id_vars,melt_value_vars,melt_var_name,melt_value_name)


enhancement_card_df = generate_enhancement_card_df(cards_df)

enhanced_decks_df = generate_enhanced_df(melted_decks_df,enhancement_card_df)

cards_appearance = generate_cards_appearance_unique(enhanced_decks_df).reset_index()

number_of_decks = len(enhanced_decks_df["deck_id"].drop_duplicates().index)


st.header(f"**{class_selectbox}'s Analysis**")
st.image(build_image(kpi_image_path),width=150)


kpi_checkbox = st.checkbox("wanna see some nerd metrics?")


if kpi_checkbox:
    st.markdown("#### Macro")
    number_of_rows = len(enhanced_decks_df.index)
    st.write("df size",number_of_rows,"rows | number of decks",number_of_decks,
                " | number of archetypes",len(deck_archetype_list))

    rarity_list = ['NOT FOUND','FREE','COMMON','RARE','EPIC','LEGENDARY']

    st.markdown("#### Rarity")
    number_of_rarity_list = []
    for rarity in rarity_list:
        number_of_rarity_list.append(len(enhanced_decks_df['hs_id'][enhanced_decks_df['rarity'].fillna("NOT FOUND") == rarity].index))
    st.write("not found cards",number_of_rarity_list[0]," | free cards",number_of_rarity_list[1]," | common cards",number_of_rarity_list[2]," | rare cards",number_of_rarity_list[3]," | epic cards",number_of_rarity_list[4]," | legendary cards",number_of_rarity_list[5])

    number_of_rarity_list = []
    for rarity in rarity_list:
        number_of_rarity_list.append(len(enhanced_decks_df['hs_id'][enhanced_decks_df['rarity'].fillna("NOT FOUND") == rarity].drop_duplicates().index))
    st.write("not found cards (unique)",number_of_rarity_list[0]," | free cards (unique)",number_of_rarity_list[1]," | common cards (unique)",number_of_rarity_list[2]," | rare cards (unique)",number_of_rarity_list[3]," | epic cards (unique)",number_of_rarity_list[4]," | legendary cards (unique)",number_of_rarity_list[5])

    st.markdown("#### Types")
    card_type_list = sorted(cards_df['type'].drop_duplicates().to_list())
    number_of_card_type_list = []
    for card_type in card_type_list:
        number_of_card_type_list.append(len(enhanced_decks_df['hs_id'][enhanced_decks_df['type'].fillna("NOT FOUND") == card_type].index))
    st.write("enhancements",number_of_card_type_list[0]," | minions",number_of_card_type_list[4]," | spells",number_of_card_type_list[6]," | weapons",number_of_card_type_list[7])

    number_of_card_type_list = []
    for card_type in card_type_list:
        number_of_card_type_list.append(len(enhanced_decks_df['hs_id'][enhanced_decks_df['type'].fillna("NOT FOUND") == card_type].drop_duplicates().index))
    st.write("enhancements (unique)",number_of_card_type_list[0]," | minions (unique)",number_of_card_type_list[4]," | spells (unique) (unique)",number_of_card_type_list[6]," | weapons",number_of_card_type_list[7])


st.write("")
st.write("")


st.header("**Card Frequency over Decks**")
st.image(build_image(top_30_path),width=150)
st.text(f"The 30 most frequent cards used in {class_selectbox} decks")


top_30 = cards_appearance.head(30)


rarity_color_list = ['#641E16','#2ECC71','#D0D3D4','#3498DB','#8E44AD','#F7DC6F']


cards_appearance_bars = alt.Chart(top_30).mark_bar(size=20).encode(
    x=alt.X('numberOfAppearance:Q'),
    y=alt.Y('cardName:N', sort="-x"),
    color=alt.Color('numberOfAppearance:Q', legend=None, scale=alt.Scale(domain=[class_selectbox], range=[class_selected_details["color"]])),
    # TODO improvement: colors by rarity with correct sort by Q desc
    tooltip=['cardName','cardRarity','numberOfAppearance']
)
cards_appearance_text = cards_appearance_bars.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(
    text='numberOfAppearance:Q'
)
cards_appearance_chart = (cards_appearance_bars+cards_appearance_text).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
).properties(width=700,height=700)


st.write(cards_appearance_chart)


st.header("**Card Details**")


range_radio = st.radio("Select the range of cards:",["1-5","6-10","11-15","16-20","21-25","26-30"])


if range_radio == "1-5":
    range_df = top_30[0:5]
elif range_radio == "6-10":
    range_df = top_30[5:10]
elif range_radio == "11-15":
    range_df = top_30[10:15]
elif range_radio == "16-20":
    range_df = top_30[15:20]
elif range_radio == "21-25":
    range_df = top_30[20:25]
else:
    range_df = top_30[25:30]


for item in range_df.index:
    card_row = cards_df[cards_df["id"] == range_df.loc[item,"cardId"]]
    card_id = str(card_row["id"].values[0])
    card_number_of_appearance = range_df.loc[item,"numberOfAppearance"]
    card_selected_path = download_agent.download(card_id)

    if card_selected_path is None:
        st.write("Card image not found :sob:")
        st.markdown(f"**{'{:03.2f}'.format(card_number_of_appearance/number_of_decks*100)}** % of presence in *{class_selectbox}* decks")
    else:
        card_selected_image = build_image(card_selected_path)
        st.image(card_selected_image, width=200)
        st.markdown(f"**{'{:03.2f}'.format(card_number_of_appearance/number_of_decks*100)}** % of presence in *{class_selectbox}* decks")
