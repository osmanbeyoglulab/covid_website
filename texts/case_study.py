import streamlit as st

def CaseStudy():
    st.caption("This page shows example usage of COVID-19db's various modules.")
    
    st.write('To get started, users can select an analysis module and a dataset from the ones available under the dataset tab.')
    st.image('./assets/case_study/ano1.jpg')
    
    
    st.write('Under the Metadata subtab, users can read the abstract of each selected dataset.')
    st.image('./assets/case_study/ano2.PNG')
    
    st.write('Under the Visualization subtab, users can interactively explore the expression of surface protein and gene of interest ovelayed on 2D UMAPs.')

    st.image('./assets/case_study/ano3.PNG')
    
        
    st.write('Once a user has a dataset picked, it can be further explored using the surface protein or transcription factors modules.')
    st.image('./assets/case_study/ano4.jpg')
    
    st.write('The inferred activity of transcription factors of interest present in specific cell types within the selected dataset can then be visualized.')
    st.image('./assets/case_study/ano5.PNG')
    
    st.write('On the viral entry module, users can select to explore the expression and TF correlations of either surface proteins or mRNAs factors related to viral entry.')
    st.image('./assets/case_study/ano6.jpg')
    
    st.write('Under the PPI subtab, users can explore known protein protein interactions from StringDB.')
    st.image('./assets/case_study/ano7.jpg')
    
    st.write('Similarly, the Drugs subtab allows users to quickly identify drugs that target specific surface proteins or transcription factors. The method of action as well as clinical phase of each drug is also shown.')
    st.image('./assets/case_study/ano8.PNG')
    
    st.write('Under the Literature references subtab, all the relevant publications from LitCovid are aggegated and displayed.')
    st.image('./assets/case_study/ano9.jpg')
    
    
    
