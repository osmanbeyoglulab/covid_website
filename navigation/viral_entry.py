import streamlit as st

from utils.components import ridge_plot, severity_order
import hydralit_components as hc
import pandas as pd
import numpy as np

def viral_entry_page(datacore):
    st.markdown(f'### Analysis by viral entry related factors')
    
    st.info("""Search for viral entry related factors by cell type. COVID-19db supports exploring the proteins, TFs, mRNAs and mRNA-TF profiles for different viral entry related factors. Users can explore the protein or mRNA expression distribution patterns for select genes for a particular cell type, depending on availability.            
""")
    
    st.caption('Click on any image to enlarge it.')
    aa, ba, ca = st.columns(3)
    a, b, c = st.columns(3)
    
    
    datasets = datacore.name2ds.keys()
    aa.caption('Select a dataset, the cell type and either viral entry related surface proteins or mRNAs.')
#     ba.caption('Note: Only viral entry related factors present in each dataset and cell type are shown.')
        
    p_ds = a.selectbox(f'Dataset ({len(datasets)-1})', filter(lambda x: x!='GSE155673', datasets), 0)
    dss = datacore.name2ds[p_ds]
    cell_types = dss.celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    st.write(f'Plots for viral entry related factors in {cell_type}')
    
    
    with ca:
        protein_only = st.radio(f'Viral entry related factors', options=['Surface Proteins', 'mRNAs'])
    
    if protein_only == 'Surface Proteins':
        option_protein = c.selectbox('Proteins', dss.get_viral_proteins(cell_type))
    else:
        option_protein = c.selectbox('mRNAs', dss.get_viral_mrnas(cell_type))
            
    a, b = st.columns(2)

    if protein_only == 'Surface Proteins' and option_protein:
        
        
        a.caption('protein distributions')
        b.caption('protein-TF correlations')
        
        with a:
            with hc.HyLoader(f'🎨 Distributing {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                df = datacore.name2ds[p_ds].get_viral_protein_df(cell_type, option_protein)
                img = ridge_plot(df, xlabel=f'{option_protein} surface protein expression', column=None)
                xx, yy = img.size
                dd = 3
                xx = int(xx/dd)
                yy = int(yy/dd)
                st.image(img.resize((xx, yy)))
                
        with b:
            with hc.HyLoader(f'🎨 Correlating {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                csv, img = datacore.name2ds[p_ds].get_viral_protein_data(cell_type, option_protein)
                st.image(img)
                
         
        
    elif protein_only == 'mRNAs' and option_protein:
        a.caption('mRNA expression distributions')
        b.caption('mRNA-TF correlations')
        
               
        with a:
            with hc.HyLoader(f'🎨 Distributing {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                df = datacore.name2ds[p_ds].get_viral_mrna_df(cell_type, option_protein)
                img = ridge_plot(df, xlabel=f'{option_protein} mRNA expression', column=None)
                xx, yy = img.size
                dd = 3
                xx = int(xx/dd)
                yy = int(yy/dd)
                st.image(img.resize((xx, yy)))
                
                
        with b:
            with hc.HyLoader(f'🎨 Correlating {option_protein}', hc.Loaders.standard_loaders,index=[3]):
                csv, img = datacore.name2ds[p_ds].get_viral_mrna_data(cell_type, option_protein)
                st.image(img)
    
    else:
        st.error(f'No viral entry related factors found in dataset {dss.name} for cell type {cell_type}', icon='❌')

    
    # df = pd.DataFrame(pd.read_csv(csv).group.value_counts()).T
    # df.index = ['severity group']
    # a.caption('Number of patients in each severity group:')
    # a.dataframe(df[np.intersect1d(df.columns, severity_order)])