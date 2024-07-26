import streamlit as st
import time,os,math,random
import pandas as pd

from deta import Deta
import hashlib
from detadb import Database



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
    global block
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
    return hashlib.sha256(string.encode()).hexdigest()

deta = Deta(os.environ['DETA'])

db = deta.Base("BlockDB")
p_db = Database("Pepper")




def count_zeros(hash):
    zeros = 0
    while hash[zeros]=='0':zeros+=1
    return zeros

def verify_block(hashes):
    genesis = hashes[0]
    hashes = hashes[1:]
    current = genesis
    for hash in hashes:
        current = sha256(current)
        if hash != current:
            return [False,]
    return True,hashes[-1]

def check_mined(mined_block):
    return db.get(sha256(mined_block)) == None

def pepper(hg,hr):
    if not count_zeros(hr) > 6:
        return
    else:
        p = "p"+hr.replace("0","a")
        p = list(p);random.shuffle(p)
        p = str(p)+str(random.getrandbits(2048))
        p = sha256(p)
        p_db[hg] = (p+"/c:lrc") if hg in lrc_blocks else (p+"/c:bb")

def list_replace(lst, old=1, new=10):
    i = -1
    try:
        while True:
            i = lst.index(old, i + 1)
            lst[i] = new
    except ValueError:
        pass

def copy_block():pass

if submitted:
    def on_submit():
        try:
            lrc_ppr = lrc_blocks
            bb_ppr = bb_blocks
            for k,v in p_db.items:
                if v.endswith("/c:lrc"):
                    lrc_ppr.pop(k)
                    lrc_ppr.append(v.split("/")[0])
                else:
                    bb_ppr.pop(k)
                    bb_ppr.append(v.split("/")[0])
            hashes = [i for i in block.split(':') if i!='']
            if currency == 'BlockBit':
                if not hashes[0] in bb_ppr:
                    st.error(f'Invalid Genesis Hash: {hashes[0]}')
                else:
                    verification = st.empty().info('Verifying block')
                    v_block = verify_block(hashes)
                    if v_block[0]:
                        verification = verification.success('Block correct. Adding to Mined Blocks')
                        zeros = count_zeros(v_block[1])
                        mining_data = f'{hashes[0]} -> {v_block[1]}'
                        if zeros > 2:
                            if not check_mined(mining_data):
                                db.put({
                                    'username':username,
                                    'block':mining_data,
                                    'zeros':zeros,
                                    'timestamp':math.floor(time.time())
                                    },sha256(mining_data)
                                    )
                                pepper(hashes[0],hashes[-1])
                                st.rerun()
                            else:
                                st.error('Already mined')
                        else:
                            st.error('Not enough zeros (less than 3 zeros found).')
                    else:
                        verification = verification.error('Invalid Block.')
            if currency == 'LRCOIN':
                if not hashes[0] in lrc_ppr:
                    st.error(f'Invalid Genesis Hash: {hashes[0]}')
                else:
                    verification = st.empty().info('Verifying block')
                    v_block = verify_block(hashes)
                    if v_block[0]:
                        verification = verification.success('Block correct. Adding to Mined Blocks')
                        zeros = count_zeros(v_block[1])
                        if zeros > 2:
                            if not check_mined(mining_data):
                                db.put({
                                    'username':username,
                                    'block':mining_data,
                                    'zeros':zeros,
                                    'timestamp':math.floor(time.time())
                                    },sha256(mining_data)
                                    )
                            else:
                                st.error('Already mined')
                        else:
                            st.error('Not enough zeros (less than 3 zeros found).')
                    else:
                        verification = verification.error('Invalid Block.')

        except Exception as e:
            st.error(f'Unknown error occured ({e})')
    on_submit()
            


"---"
"Mined Blocks"

class MinedBlock:
    def __init__(self,username,item_block,zeros,timestamp,mining_hash):
        self.username,self.block,self.zeros,self.timestamp,self.hash = username,item_block,zeros,timestamp,mining_hash
    def df(self):
        return self.__dict__.values()



db_mined = []

for item in db.fetch().items:

    db_mined.append(MinedBlock(item['username'],item['block'],item['zeros'],item['timestamp'],item['key']))

dataframe = [['Miner Username','Mining data','Amount of zeros found','Timestamp','Hash of mining data']]

for minedblock in db_mined:
    minedblock:MinedBlock = minedblock
    dataframe.append(minedblock.df())

lrc_ppr = lrc_blocks
bb_ppr = bb_blocks
for k,v in p_db.items:
    if v.endswith("/c:lrc"):
        lrc_ppr.pop(k)
        lrc_ppr.append(v.split("/")[0])
    else:
        bb_ppr.pop(k)
        bb_ppr.append(v.split("/")[0])

st.dataframe(pd.DataFrame(dataframe))

'---'
'Available Blocks'

available = [list(x) for x in zip(bb_ppr,lrc_ppr)]

available.insert(0,['BlockBit','LRCOIN'])

st.dataframe(pd.DataFrame(available))

'---'

st.button('Get block for LRCOIN')

st.button('Get block for LRCOIN',on_click=c)