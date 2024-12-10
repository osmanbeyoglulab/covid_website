import streamlit as st

def download_page():
    st.markdown(f'### Data Download')
    st.caption('The SPaRTAN module predicts transcription factor from gene expression and protein profile. We run the SPaRTAN model for each cell type and each patient. The download links below contain predicted TF for each dataset organized by cell type and patient.')
    st.markdown('##### GSE161918')
    st.write(f'{"Original Data:  "} https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE161918')
    st.write('SPaRTAN Output:  https://sites.pitt.edu/~xim33/data/Covid19/GSE155673.zip')
    st.write('---')
    
    st.markdown('##### GSE155673')
    st.write(f'{"Original Data:  "} https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155673')
    st.write('SPaRTAN Output:  https://sites.pitt.edu/~xim33/data/Covid19/GSE155673.zip')
    st.write('---')
    
    st.markdown('##### GSE155224')
    st.write(f'{"Original Data:  "} https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE155224')
    st.write('SPaRTAN Output:  https://sites.pitt.edu/~xim33/data/Covid19/GSE155224.zip')
    st.write('---')
    
    st.markdown('##### E-MTAB-10026')
    st.write(f'{"Original Data:  "} https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=E-MTAB-10026')
    st.write('SPaRTAN Output:  https://sites.pitt.edu/~xim33/data/Covid19/E-MTAB-10026.zip')
    st.write('---')
    
    st.markdown('##### E-MTAB-9357')
    st.write(f'{"Original Data:  "} https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=E-MTAB-9357')
    st.write('SPaRTAN Output:  https://sites.pitt.edu/~xim33/data/Covid19/E-MTAB-9357.zip')
    st.write('---')
