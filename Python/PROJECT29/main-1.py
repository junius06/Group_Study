import streamlit as st

data_list = {1,2,3,4,5,6,7,8,9,10}
st.write('''
샘플데이터
''')

st.line_chart(data_list)