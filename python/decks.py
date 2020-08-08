import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import os


os.environ['TZ'] = 'UTC'

decks_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/decks/data.csv"
cards_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/datasets/cards/cards.json"


cards_sample_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/hearthstone_cards_sample.png_2.png"
hearthstone_logo_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/logos/hearthstone_title_small.png"
medivh_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/medivh_logo.png"
innkeeper_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/innkeeper.png"
innkeeper_2_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/innkeeper_2.png"
heroes_path = "/Users/Yamada/Git/git-projects/hs-decks-analysis/data/images/design/heroes_hs.png"


def build_image(path):
    return Image.open(path)


@st.cache
def generate_df(path,datatype):
    if datatype == "csv":
        return pd.read_csv(path)
    if datatype == "json":
        return pd.read_json(path)


decks_df = generate_df(decks_path, "csv")
cards_df = generate_df(cards_path, "json")

# ---------------------- Sidebar (Filters) ----------------------

@st.cache
def get_min_max_date(df):
    return {"min": df["date"].min(),"max": df["date"].max()}

date_dict = get_min_max_date(decks_df)
min_date = datetime.strptime(date_dict["min"],'%Y-%m-%d')
max_date = datetime.strptime(date_dict["max"],'%Y-%m-%d')


@st.cache
def get_min_max_craft_cost(df):
    return {"min": df["craft_cost"].min(),"max": df["craft_cost"].max()}

craft_cost_dict = get_min_max_craft_cost(decks_df)
min_craft_cost = int(craft_cost_dict["min"])
max_craft_cost = int(craft_cost_dict["max"])


@st.cache()
def get_deck_class(df):
    return df["deck_class"].drop_duplicates().values.tolist()


@st.cache()
def get_deck_set(df):
    return df["deck_set"].drop_duplicates().values.tolist()


@st.cache()
def get_deck_type(df):
    return df["deck_type"].drop_duplicates().values.tolist()


@st.cache
def get_min_max_rating(df):
    return {"min": df["rating"].min(),"max": df["rating"].max()}

rating_dict = get_min_max_rating(decks_df)
min_rating = int(rating_dict["min"])
max_rating = int(rating_dict["max"])


hearthstone_logo_image = build_image(hearthstone_logo_path)
st.sidebar.image(hearthstone_logo_image, use_column_width=True)


st.sidebar.title("Dataframe Filters")


date_slider = st.sidebar.slider('Date',min_date,max_date,[min_date,max_date])

craft_cost_slider = st.sidebar.slider('Craft Cost',min_craft_cost,max_craft_cost,[min_craft_cost,max_craft_cost])

deck_archetype_text_input = st.sidebar.text_input("Deck Archetype")

list_class = get_deck_class(decks_df)
class_multiselect = st.sidebar.multiselect('Deck Class',list_class,list_class)

# list_set = get_deck_set(decks_df)
# set_multiselect = st.sidebar.multiselect('Deck Set',list_set,list_set)

list_type = get_deck_type(decks_df)
type_multiselect = st.sidebar.multiselect('Deck Type',list_type,list_type)

rating_slider = st.sidebar.slider('Rating',min_rating,max_rating,[min_rating,max_rating])

# innkeeper_image = build_image(innkeeper_path)
# st.sidebar.image(innkeeper_image, use_column_width=True)

# ---------------------------------------------------------------

# ---------------------------- Main -----------------------------

# -------------------------- Dataframe --------------------------


st.title("Decks Analysis")

medivh_image = build_image(medivh_path)
st.image(medivh_image, use_column_width=True)


melt_id_vars = ['craft_cost','date','deck_archetype','deck_class','deck_format','deck_id','deck_set','deck_type','rating','title','user']
melt_value_vars = ['card_0','card_1','card_2','card_3','card_4','card_5','card_6','card_7','card_8','card_9','card_10','card_11','card_12','card_13','card_14','card_15','card_16','card_17','card_18','card_19','card_20','card_21','card_22','card_23','card_24','card_25','card_26','card_27','card_28','card_29']
melt_var_name = 'card_index'
melt_value_name = 'card_id'

@st.cache
def melt_raw_df(df,id_vars,value_vars,var_name,value_name):
    return pd.melt(df, id_vars=id_vars, value_vars=value_vars, ignore_index=False, var_name=var_name, value_name=value_name)


melted_decks_df = melt_raw_df(decks_df,melt_id_vars,melt_value_vars,melt_var_name,melt_value_name)


@st.cache
def generate_enhancement_card_df(df):
    return df[["dbfId","id","name"]].drop_duplicates()


enhancement_card_df = generate_enhancement_card_df(cards_df)


@st.cache()
def generate_enhanced_df():
    enhanced_decks_df = pd.merge(melted_decks_df,enhancement_card_df,how="left",left_on='card_id',right_on='dbfId')

    rename_enhanced_dict = {"id": "hs_id","name": "card_name"}
    enhanced_decks_df = enhanced_decks_df.rename(columns=rename_enhanced_dict)


    enhanced_decks_df['date'] = enhanced_decks_df['date'].str[:10]
    enhanced_decks_df['date'] = pd.to_datetime(enhanced_decks_df['date'], format='%Y-%m-%d')


    filter_columns_enhanced_list = ['craft_cost','date','deck_archetype','deck_class','deck_format','deck_id','deck_set','deck_type','rating','title','user','card_index','card_id','hs_id','card_name']
    return enhanced_decks_df[filter_columns_enhanced_list].sort_values(by=['deck_id','date'], ascending=False)

enhanced_decks_df = generate_enhanced_df()


st.write("Enhanced Decks DF: ",len(enhanced_decks_df.index),"rows")
st.write("Validation: ",len(decks_df.index),"(rows in the raw dataframe) * ",30," (number of cards in a deck) =",len(decks_df.index)*30)
if len(enhanced_decks_df.index) == len(decks_df.index)*30:
    st.success('Calculation correct!')
else:
    st.error("The result number of rows aren't correct")

st.markdown("## **Result Dataframe (sample)**")
st.text("Use the filters on the left sidebar to explore the dataframe below")


if deck_archetype_text_input != '':
    result_df = enhanced_decks_df[enhanced_decks_df['deck_class'].isin(class_multiselect)
                    & enhanced_decks_df['deck_type'].isin(type_multiselect)
                    & enhanced_decks_df['deck_archetype'].str.contains(deck_archetype_text_input)]
else:
    result_df = enhanced_decks_df[enhanced_decks_df['deck_class'].isin(class_multiselect)
                    & enhanced_decks_df['deck_type'].isin(type_multiselect)]

if date_slider[0]!=min_date or date_slider[1]!=max_date:
    result_df = result_df[result_df['date'].between(date_slider[0], date_slider[1])]

if craft_cost_slider[0]!=min_craft_cost or craft_cost_slider[1]!=max_craft_cost:
    result_df = result_df[result_df['craft_cost'].between(craft_cost_slider[0], craft_cost_slider[1])]

if rating_slider[0]!=min_rating or rating_slider[1]!=max_rating:
    result_df = result_df[result_df['rating'].between(rating_slider[0], rating_slider[1])]

st.dataframe(result_df.head(3000))

st.write("Showing",3000,"rows (= 100 decks)")
st.write(len(result_df.index),"rows total in the dataframe")

st.write("**KPIs (Result DF)** :mag:")

def calculate_kpis(df):
    return df

kpis = calculate_kpis(result_df)
st.dataframe(result_df)

innkeeper_2_image = build_image(innkeeper_2_path)
st.image(innkeeper_2_image, width=400)

# ---------------------------------------------------------------

# ---------------------------- Cards -----------------------------

st.title("Cards Analysis")

cards_sample_image = build_image(cards_sample_path)
st.image(cards_sample_image, use_column_width=True)

