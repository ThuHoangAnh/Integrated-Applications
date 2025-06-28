import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image

st.set_page_config(page_title='Integrated Application', page_icon='🚀', layout='wide')
st.markdown(
    "<h1 style='text-align: center;'>Applications</h1>",
    unsafe_allow_html=True
)

app = st.sidebar.selectbox(label='Choose an app:', options=('Select', 'App 1: Score Analysis', 'App 2: Factorial Calculator'))

if app == 'Select':
    st.image('image.jpg', use_container_width=True)

if app == 'App 1: Score Analysis':
    def calculate_average(scores):
        return sum(scores) / len(scores)

    def distribute_score(scores):
        dictionary_of_score = {'90 - 100': 0,
                            '80 - 89': 0,
                            '70 - 79': 0,
                            '60 - 69': 0,
                            '< 60': 0}
        for score in scores:
            if score >= 90:
                dictionary_of_score['90 - 100'] += 1
            elif score >= 80:
                dictionary_of_score['80 - 89'] += 1
            elif score >= 70:
                dictionary_of_score['70 - 79'] += 1
            elif score >= 60:
                dictionary_of_score['60 - 69'] += 1
            else:
                dictionary_of_score['< 60'] += 1
        return dictionary_of_score

    def draw_chart(distribution_of_score):
        ranking = list(distribution_of_score.keys())
        value = list(distribution_of_score.values())
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(aspect='equal'))
        ax.pie(x=value, 
            autopct='%1.1f%%', 
            textprops=dict(color='white', fontsize=12))
        ax.set_title('Distribution of scores')

        ax.legend(ranking, title='Ranking', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        #st.pyplot(fig=fig)

        buff = io.BytesIO() # Create an in-memory buffer
        fig.savefig(buff, format='png', dpi=300, bbox_inches='tight') # Save the current figure as an image to that buffer
        img = Image.open(buff) # Open that image as a PIL image object
        st.image(img) # Show that image

    def main():
        st.title('Score Analysis Application :sunglasses:')
        # Upload file
        uploaded_file = st.file_uploader(label='Choose your file', type='xlsx')
        if uploaded_file is not None:
            # To read files
            df = pd.read_excel(uploaded_file)
            st.write(df)

            # Calculate average scores
            scores = list(df['Điểm số'])
            average_score = calculate_average(scores)
            total_number = len(scores)
            st.write(f'Total number of students is {total_number}')
            st.write(f'Average score is {average_score}')

            # Calculate distribution of score
            distribution_of_score = distribute_score(scores)
            #st.write(distribution_of_score)

            # Draw a pie chart to show distribution of score
            pie_chart = draw_chart(distribution_of_score)

    if __name__ == '__main__':
        main()

if app == 'App 2: Factorial Calculator':
    # Initialize session variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''

    def factorial(n):
        if n < 0:
            return 'Must be a positive number'
        if n == 0 or n == 1:
            return 1
        if n > 1:
            return n * factorial(n - 1)
        
    def show_calculator():
        st.title('Factorial Calculator')
        input_number = st.number_input(label='Enter a number', 
                                min_value=0,
                                max_value=999, 
                                step=1,
                                value=None,
                                placeholder='Type a number')
        if input_number:
            st.write(f'Your number is {input_number}')

            result = factorial(input_number)
            button = st.button(label='Calculate', type='secondary', icon='🚨')
            if button:
                st.write(f'The factorial of {input_number} is {result}')   

    def log_in_page():
        st.title('Welcome to the app') 
        choose_role = st.selectbox(label='Choose or add an option', 
                    options=('Admin', 'New_user'), 
                    index=None, 
                    placeholder='Select one')
        return choose_role

    def main():
        user = log_in_page()
        if user is None:
            st.info('Please select a role to continue.')

        elif user == 'Admin':
            show_calculator()

        elif user == 'New_user':
            if not st.session_state.authenticated:
                name = st.text_input(label='Enter your name', 
                                    value=None, 
                                    placeholder='Put your name')
                if name == 'Thu':
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.success('Welcome {name}')
                    st.rerun()
                elif name:
                    st.error('Access denied. You are not registered.')

            else:
                st.success(f'Welcome back {st.session_state.user_name}!')
                show_calculator()

                if st.button('Log out'):
                    st.session_state.authenticated = False
                    st.session_state.user_name = ''
                    st.rerun()

    if __name__ == '__main__':
        main()
