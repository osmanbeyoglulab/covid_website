from navigation.contact import contact_page
from navigation.datasets import dataset_page
from navigation.doc import doc_page
from navigation.home import home_page
from navigation.download import download_page
from navigation.multi_dataset_search import multi_dataset_page
from navigation.protein import protein_page
from navigation.stats import stats_page
from navigation.tf import tf_page
from navigation.viral_entry import viral_entry_page
from utils.components import footer_style, footer
from utils.dataloaders import make_datacore
from PIL import Image

import streamlit as st
import hydralit_components as hc

st.set_page_config(
        page_title='COVID-19db of Immune Cell States',
        page_icon="./assets/logos/spartan.png",
        initial_sidebar_state="expanded",
)

def define_layout(max_width, padding_top='0rem', padding_right='0rem', padding_left='0rem', padding_bottom='0rem'):


    st.markdown(
        f"""
        <style>
            .appview-container .main .block-container{{
                max-width: {max_width};
                padding-top: {padding_top};
                padding-right: {padding_right};
                padding-left: {padding_left};
                padding-bottom: {padding_bottom};
            }}
          
        </style>
        """,
        unsafe_allow_html=True,
    )


define_layout(max_width='80%', padding_top='2rem', padding_right='0rem', padding_left='0rem', padding_bottom='0rem')

# max_width_str = f"max-width: {75}%;"
# st.markdown(f"""
#         <style>
#         .appview-container .main .block-container{{{max_width_str}}}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 0rem;
#                     padding-bottom: 0rem;
                    
#                 }
#         </style>
#         """, unsafe_allow_html=True)


Image.MAX_IMAGE_PIXELS = None

HOME = "Home"
DATASET = "Datasets"
TF = "Transcription factors"
PROTEINS = "Surface proteins"
VIRAL_ENTRY = "Viral-entry related factors"
MULTI = "Multi datasets"
DOC = "Docs"
CONTACT = "Contact"
STATS = "Usage"
DOWNLOAD = "Download"


datacore =  make_datacore()()
ds = datacore.metadata

st.markdown(footer_style, unsafe_allow_html=True) ## Footer

tabs = [
    HOME,
    DATASET,
    PROTEINS,
    TF,
    VIRAL_ENTRY,
    DOC, 
    STATS,
    CONTACT,
    DOWNLOAD
]

option_data = [
   {'icon': "🏠", 'label':HOME},
   {'icon':"💾",'label':DATASET},
   {'icon': "🔎", 'label':PROTEINS},
   {'icon': "🔎", 'label':TF},
   {'icon': "🌡", 'label':VIRAL_ENTRY},
   {'icon': "🎛", 'label':"Multi datasets"},
   {'icon': "📑", 'label':DOC},
   {'icon': "📞", 'label':CONTACT},
   {'icon': "📈", 'label':STATS},
   {'icon': "📥", 'label':DOWNLOAD},
   
]

over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'red'}
font_fmt = {'font-class':'h3','font-size':'50%'}

chosen_tab = hc.option_bar(
    option_definition=option_data,
    title='',
    key='PrimaryOptionx',
    override_theme=over_theme,
    horizontal_orientation=True)


if chosen_tab == HOME:
    home_page()
    
elif chosen_tab == CONTACT:
    contact_page()
    
elif chosen_tab == DATASET:
    dataset_page(ds, datacore)
    
elif chosen_tab == TF:
    tf_page(datacore)
    
elif chosen_tab == PROTEINS:
    protein_page(datacore)
        
elif chosen_tab == VIRAL_ENTRY:
    viral_entry_page(datacore)
        
elif chosen_tab == MULTI:
    multi_dataset_page(datacore)
          
elif chosen_tab == DOC:
    doc_page()
    
elif chosen_tab == STATS:
    stats_page()
    
elif chosen_tab == DOWNLOAD:
    download_page()


for i in range(6):
    st.markdown('#')
st.markdown(footer,unsafe_allow_html=True)
        
# st.markdown(icons, unsafe_allow_html=True)
