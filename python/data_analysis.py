import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def main():
    st.title("Test App")
    st.header("Aoooba porra fdp passei na AWS heuheuehue")
    st.subheader("E agora, será que vai pagar bem?")
    st.markdown('Markdown **Test**')


    my_placeholder = st.empty()
    my_placeholder.text("Hello world!")

    'write vs text :smile:'
    st.write("CHEVARAVAGA TCHEVARAANCHORI")
    st.text("CHEVARAVAGA TCHEVARAANCHORI")

    df1 = pd.DataFrame(
        np.random.randn(50, 10),
        columns=('col %d' % i for i in range(10)))

    df2 = pd.DataFrame(
        np.random.randn(50, 10),
        columns=('col %d' % i for i in range(10)))

    my_table = st.dataframe(df1)
    my_table.add_rows(df2)     

    x = st.slider('x',0,20)
    y_title = st.sidebar.markdown("### Filter Y")
    y = st.sidebar.slider('y',0.0,20.0,[0.0,10.0],0.5,'%f','y_slider')
    st.write(x, 'squared is', x * x)
    x, 'squared is', x * x
    y, 'y'

    code = '''def hello():
        print("Hello, Streamlit!")'''
    st.code(code, language='python')

    active_checkbox = st.checkbox('Deseja usar C-4?',False)

    if active_checkbox:
        st.write('OLHA A BOOOOOOOOMBA')
  
    validation_button = st.sidebar.button('Validation','validation_button')
    
    if validation_button:
        st.markdown('### Validation **[ON]**')
    else:
        st.markdown('### Validation **[OFF]**')

    anime_list = ['Naruto','Bleach','Fairy Tail']

    anime_selectbox = st.selectbox('Animes',anime_list,0)

    @st.cache
    def generate_anime_df():
        hero_df = pd.DataFrame({'id': [1,2,3],'name': ['Naruto','Ichigo','Natsu'],'anime': anime_list})
        filtered_hero_df = hero_df['anime'] == anime_selectbox
        return hero_df[filtered_hero_df]
    
    df = generate_anime_df()
    df

    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
        option = st.selectbox('Which number do you like best?',
            chart_data['a'])
        'You selected: ', option
        c = alt.Chart(chart_data).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
        
        chart_data

        st.write(c)
        st.line_chart(chart_data)
        st.area_chart(chart_data)
        st.bar_chart(chart_data)

    arr = np.random.normal(1, 1, size=100)
    plt.hist(arr, bins=20)

    st.pyplot()

    # 'Starting a long computation...'

    # latest_iteration = st.empty()
    # bar = st.progress(0)

    # for i in range(10):
    #     latest_iteration.text(f'Iteration {i+1}')
    #     bar.progress(i + 1)
    #     time.sleep(0.1)

    # '...and now we\'re done!'

    genre = st.radio(
        "What's your favorite movie genre",
        ('Comedy', 'Drama', 'Documentary'))
    if genre == 'Comedy':
        st.write('You selected comedy.')
    else:
        st.write("You didn't select comedy.")

    options = st.multiselect(
        'What are your favorite colors',
        ['Green', 'Yellow', 'Red', 'Blue'],
        ['Yellow', 'Red'])
    st.write('You selected:', options)

    st.json({"id": "1","attributes": {"a": "A", "b": "B",}})


    image = Image.open('/Users/Yamada/Downloads/3-2-coming-soon-picture.png')
    if st.checkbox('Night King'):
        image = Image.open('/Users/Yamada/Downloads/got-sentences-analysis.jpg')

    st.image(image, caption='Sunrise by the mountains',use_column_width=True)

    title = st.text_input('Movie title', 'Life of Brian')
    st.write('The current movie title is', title)

    number = st.number_input('Insert a number')
    st.write('The current number is ', number)

    analyzer = SentimentIntensityAnalyzer()
    def run_sentiment_analysis(sentence):
        return analyzer.polarity_scores(sentence)['compound']

    txt = st.text_area('Text to analyze',value='''
        It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''',height=200,max_chars=5000)
    st.write('Sentiment:', run_sentiment_analysis(txt))

    d = st.date_input(
        "When's your birthday",
        datetime.date(2019, 7, 6))
    st.write('Your birthday is:', d)
    t = st.time_input('Set an alarm for', datetime.time(8, 45))
    st.write('Alarm is set for', t)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", encoding='utf-8')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(f'Num. of rows of the uploaded file: {len(data.index)}')
        st.write(data)

    color = st.beta_color_picker('Pick A Color', '#00f900')
    st.write('The current color is', color)

    def get_user_name():
        return 'John'

    with st.echo():
        def get_punctuation():
            return '!!!'

        greeting = "Hi there, "
        value = get_user_name()
        punctuation = get_punctuation()

        st.write(greeting, value, punctuation)

        st.write('Done!')

    import time

    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

    st.info('This is a purely informational message')

    with st.spinner('Wait for it...'):
        time.sleep(5)
        st.success('Done!')
        st.balloons()
        st.error('This is an error')
        st.warning('This is a warning')
        e = RuntimeError('This is an exception of type RuntimeError')
        st.exception(e)

    

if __name__ == '__main__':
    main() 