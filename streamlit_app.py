import streamlit as st
import stqdm
from deta import Deta
from hashlib import sha256 as sha

lrc_blocks=[
    'f1faf95f339150330bf72fc9daff2369ef5d4b346aa173a300f45b4064a58c4b',
    '783fc694d088fddf2a4b13144544645c4e698a13ddbbf2c492cfbfa5547d3906',
    'f5bc5e7189a5c8ccc597710f83e5e33506c7983fa268b7367c1b6021bf936e25',
    'bc494e4b600e613f41e03ec6c539bd6039e699f36787b6d2ee2d153e46105fba',
    '8b6f7ee494871bfd25ef93bea67814abd8d332b653ad8678edbbc5ec00574af8'
]


bb_blocks=[
    '9bb327731ca9c466dc1109c47447ca6de720f31bcf3a3e8b1511f681cdf96fb0',
    '899152068433cd428e4dafe4f43afb861cb87a386dc5dadb59ab99665d9f492',
    'c3787403c3fd32c79bd10922e82321cf79e5c664939737bc875cbfcd21946ef3',
    '2982ce3dcbaf60b9a248d97664ae8cc324d8cd5304f1233cd23024ac576c4f61',
    'b7eaeb16da92bb9dd2871cac61d7e58e9fe771a8efb9b44e820d6159ffb93bf6'
]



with st.form("form"):
    block = st.text_input("Mined Block")
    currency = st.selectbox(
        'Currency',
            (
                'BlockBit',
                'LRCOIN'
            )
    )
    username = st.text_input("Username")
    submitted = st.form_submit_button("Verify")

def sha256(string:str):
    return sha(string.encode()).hexdigest()

deta = Deta('a0HtVaaJbFqo_C4ec5QJ4LwEMSdmFw1uqSneCyyVdkjpj')

db = deta.Base("BlockDB")

if submitted:
    def on_submit():
        try:
            blocks = [i for i in block.split(':') if i!='']
            if currency == 'BlockBit':
                if not blocks[0] in bb_blocks:
                    st.error(f'Invalid Genesis Block: {blocks[0]}')
                else:
                    st.empty().info('Verifying block')
        except:
            st.error('Unknown error occured.')
    on_submit()
            

"---"
"Mined Blocks"
# This reads all items from the database and displays them to your app.
# db_content is a list of dictionaries. You can do everything you want with it.
db_content = db.fetch().items
st.write(db_content)

