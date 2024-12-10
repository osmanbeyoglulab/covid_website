import random
import pandas as pd
import streamlit as st
import hydralit_components as hc
from navigation.protein_pages.expression import display_protein_expressions
from navigation.protein_pages.litcovid import display_litcovid_data
from navigation.protein_pages.protein_tf_corr import display_protein_tf_corr_data

from utils.api import litcov_search
from utils.components import display_ppi_data
from io import BytesIO
from PIL import Image
import requests

EMTAB10026proteins = ['CD163', 'CD66a', 'CD357', 'CD161', 'CD21', 'CD319', 'Phospho-Tau', 'CD258', 'TCR-Vb13-1', 'CD22', 'HLA-ABC', 'CD371', 'CD184', 'CD158', 'CD11c', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'CD137', 'CD223', 'TCR-Va24-Ja18', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'CD197', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'CD15', 'c-Met', 'CD16', 'CD86', 'TCR-Vg9', 'CD278', 'CD4', 'Podoplanin', 'CD38', 'CD25', 'CD62L', 'CD69', 'CD224', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD324', 'CD209', 'HLA-F', 'NCR3', 'CD235ab', 'CD26', 'NLRP2', 'CD158b', 'CD45', 'CD95', 'XCR1', 'CD141', 'CD49f', 'CD18', 'CD36', 'CD2', 'CD41', 'CD183', 'HLA-A2', 'CD101', 'CD44', 'IgLambdaLight', 'CD120a', 'CD150', 'Mac-2', 'CX3CR1', 'CLEC15A', 'CD314', 'CD307d', 'CD99', 'CD244', 'CD370', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD40LG', 'CD33', 'CD226', 'CD127', 'CD133', 'CD138', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD274', 'CD195', 'CD90', 'IgKappaLight', 'CD27', 'CD307e', 'TCR-G-D', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'CD62', 'IgD', 'CD328', 'CD96', 'CD39', 'CD98', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD1C', 'CD137L', 'CD196', 'ITGB7', 'CD28', 'CD71', 'CD11b', 'LOX-1', 'CD94', 'CD8', 'CD24', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'TCR-Vg2', 'CD32']
EMTAB9357proteins = ['CD357', 'CD319', 'CD101', 'HLA', 'B7', 'CD150', 'CD184', 'c', 'CD158', 'CX3CR1', 'CD307d', 'CD99', 'CD244', 'CD11c', 'CD11a', 'CD275', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'CD3', 'CD124', 'IgA', 'CD81', 'CD305', 'CD7', 'FCERIA', 'CD303', 'CD123', 'CD137', 'CD144', 'CD223', 'CD58', 'CD335', 'DR3', 'CD169', 'CD82', 'CD49d', 'CD5', 'CD257', 'CD33', 'CD85j', 'CD88', 'CD226', 'CD127', 'CD1c', 'CD197', 'TSLPR', 'CD133', 'CD73', 'CD326', 'CD138', 'CD19', 'CD45RA', 'CD155', 'CD207', 'CD336', 'CD254', 'CD360', 'CD269', 'CD56', 'CD35', 'CD122', 'Ig', 'CD16', 'CD64', 'CD337', 'CD86', 'KLRG1', 'CD278', 'CD195', 'CD4', 'CD38', 'Podoplanin', 'CD154', 'CD62L', 'CD69', 'CD30', 'CD224', 'CD178', 'CD29', 'CD47', 'CD45RO', 'CD206', 'CD52', 'CD70', 'CD107a', 'CD39', 'CD96', 'TCR', 'Tau', 'CD98', 'CD57', 'CD54', 'CD204', 'CD324', 'CD31', 'CD26', 'CD366', 'NLRP2', 'CD158b', 'CD45', 'Mac', 'CD95', 'CD137L', 'XCR1', 'CD71', 'ITGB7', 'CD28', 'CD11b', 'CD94', 'CD141', 'CD24', 'CD8', 'CD49f', 'CD36', 'CD18', 'CD2', 'CD66b', 'CD279', 'CD14', 'CD41', 'CLEC12A', 'CD183', 'CD32']
GSE155224proteins = ['CD163', 'CD357', 'CD319', 'CD161', 'CD21', 'CD258', 'HLA', 'CD22', 'CD184', 'TCR-Vr9', 'CD158', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'CD137', 'CD223', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'CD15', 'CD16', 'CD278', 'CD4', 'Podoplanin', 'CD38', 'CD154', 'CD25', 'CD62L', 'CD69', 'CD30', 'CD224', 'TCR-Va24-Jz18', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD209', 'CD324', 'HLA-F', 'CD26', 'NLRP2', 'CD158b', 'CD95', 'XCR1', 'CD141', 'CD49f', 'CD18', 'CD36', 'CD2', 'CD41', 'CLEC12A', 'CD62P', 'HLA-A2', 'CD101', 'CD150', 'Mac-2', 'CX3CR1', 'CD314', 'CD307d', 'CD244', 'CD370', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'TCR-A-B', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'integrin', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD33', 'TCR-Vb13', 'CD226', 'CD127', 'CD1c', 'CD133', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'Ig-light-chain-1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD337', 'KLRG1', 'CD274', 'CD195', 'CD90', 'Ig-light-chain-2', 'CD27', 'CD307e', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'IgD', 'CD328', 'CD96', 'CD39', 'CD98', 'TCR-Vd2', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD66', 'CD137L', 'CD196', 'CD28', 'CD71', 'LOX-1', 'CD94', 'CD24', 'CD8', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'CD32']
GSE155673proteins = ['CD163', 'CD56', 'HLA', 'CD16', 'CD86', 'CD274', 'CD4', 'CD38', 'CD370', 'CD11c', 'CD25', 'CD27', 'CD69', 'CD3', 'TCR-G-D', 'CD20', 'CD34', 'TCR-Va7-2', 'CD45RO', 'CD123', 'FCER1A', 'Anti-PE', 'CD33', 'CD28', 'CD95', 'CD127', 'CD1c', 'CD94', 'CD197', 'CD8', 'CD279', 'CD14', 'CD19', 'CD45RA']
GSE161918proteins = ['CD163', 'CD357', 'CD319', 'CD161', 'CD21', 'Phospho-Tau', 'CD258', 'CD22', 'HLA-ABC', 'CD184', 'CD158', 'CD11c', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'CD66ace', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'IgG1Kiso', 'CD137', 'CD223', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'CD197', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'IgG2aKiso', 'CD15', 'c-Met', 'CD16', 'CD86', 'TCR-Vg9', 'CD278', 'CD4', 'CD38', 'Podoplanin', 'CD154', 'CD25', 'CD62L', 'CD69', 'CD30', 'CD224', 'TCR-Va24-Jz18', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD324', 'CD209', 'HLA-F', 'ratIgG2bKiso', 'CD235ab', 'CD26', 'NLRP2', 'CD158b', 'CD45', 'CD95', 'XCR1', 'CD141', 'CD18', 'CD49f', 'CD36', 'CD2', 'CD41', 'CLEC12A', 'CD183', 'CD62P', 'CD101', 'CD44', 'IgLambdaLight', 'CD150', 'Mac-2', 'CX3CR1', 'CD314', 'CD307d', 'CD99', 'CD244', 'CD370', 'CD40', 'CD158f', 'CD1d', 'TIGIT', 'TCR-A-B', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'integrin', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD33', 'CD127', 'CD226', 'CD1c', 'CD133', 'CD138', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD337', 'KLRG1', 'CD274', 'CD195', 'CD90', 'IgKappaLight', 'CD27', 'CD307e', 'TCR-G-D', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'IgD', 'CD328', 'CD39', 'CD96', 'CD98', 'TCR-Vd2', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD137L', 'CD196', 'CD28', 'CD71', 'CD11b', 'LOX-1', 'CD94', 'CD8', 'CD24', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'CD32']


def generate_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number
   
protein_bar = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'blue'}

def download_button(desc: str, data, fname: str, label: str = 'Download', format: str ='text/csv'):
    left_col, right_col = st.columns([2, 1])
    right_col.download_button(
        label='📥 '+label,
        data=data,
        file_name=fname,
        mime=format,
    )
        
    left_col.write(desc)

def img_path2buffer(img_path: str):
    response = requests.get(img_path)
    img = Image.open(BytesIO(response.content))
    # img = Image.open(img_path)
    buf = BytesIO()
    img.save(buf, format='PNG')
    png = buf.getvalue()
    return png



def protein_page(datacore):
    st.markdown(f'### Analysis by surface protein')
    
    st.info('Search surface protein across COVID-19 patients and health individuals, depending on availability. For a single surface protein, SPaRTAN COVID-19db supports exploring its expression for each cell type, correlated transcription factors, protein-protein interactions and relevant literature.')
    
    _, _, edge = st.columns(3)
    
    checkbox = edge.checkbox('Show high correlations only')    
    a, b, c = st.columns(3)
    st.session_state['datasets'] = ["GSE155673"]
    datasets = datacore.name2ds.keys()
    p_ds = a.selectbox(f'Dataset ({len(datasets)})', datasets, 0)
    cell_types = datacore.name2ds[p_ds].celltypes
    cell_type = b.selectbox(f'Cell Type ({len(cell_types)})', cell_types, 0)
    
    if not checkbox:
        if (p_ds == 'E-MTAB-10026'):
            s_proteins = EMTAB10026proteins
        elif (p_ds == 'E-MTAB-9357'):
            s_proteins = EMTAB9357proteins
        elif (p_ds == 'GSE155224'):
            s_proteins = GSE155224proteins
        elif (p_ds == 'GSE155673'):
            s_proteins = GSE155673proteins
        elif (p_ds == 'GSE161918'):
            s_proteins = GSE161918proteins
    else:
        s_proteins = list(datacore.name2ds[p_ds].surface_proteins(cell_type))

    selected_protein = c.selectbox(
        f"Surface protein of interest ({len(s_proteins)})",
        s_proteins)
            
    try:    
        litcovdf = litcov_search(selected_protein)
    except:
        litcovdf = pd.DataFrame([])
        
    subtabs = ['Protein expression', 'Protein-TF correlation', 'Drugs', f'Literature references ({len(litcovdf)})', 'PPI', 'Download']

    option_data2 = [{'icon': icon, 'label':label} for 
            label, icon in zip(
                subtabs, 
                ['📈', '🔗', '💊', '📚', ' 🔄','📩']
            )
    ]
    
    chosen_subtab = hc.option_bar(
        option_definition=option_data2,
        title='',
        key='Sub2',
        override_theme=protein_bar,
        horizontal_orientation=True)
        
        
    if chosen_subtab == 'Protein expression':
        st.info(cell_type)
        display_protein_expressions(selected_protein, datacore.name2ds[p_ds], cell_type)
        st.caption('Note: Density plots were generated using the mean of the protein expression across cells.')
        
        
    elif chosen_subtab == 'Protein-TF correlation':
        display_protein_tf_corr_data(selected_protein, cell_type, datacore.name2ds[p_ds])
        
    elif chosen_subtab == 'Drugs':
        drugs_df = pd.read_csv('./data/drugs/repurposing_drugs_20180907.txt', sep='\t')
        drugs_df = drugs_df.dropna(subset=['target'], axis=0)
        st.caption('Examples: CD44, CD38...')
        # for p in s_proteins:
        #     _drugs_df = drugs_df[drugs_df.target.apply(lambda x: p in x.split('|'))]
        #     if len(_drugs_df) > 0:
        #         st.title(p)
        #         # st.table(_drugs_df)
        #         st.write(_drugs_df.to_dict())
        
                    
        _drugs_df = drugs_df[drugs_df.target.apply(lambda x: selected_protein in x.split('|'))]
        if len(_drugs_df) > 0:
            # st.title(selected_protein)
            st.table(_drugs_df.drop('target', axis=1))     
            
        else:
            st.warning(f'No drugs found for {selected_protein}.')       

            
    elif 'Literature references' in chosen_subtab:
        display_litcovid_data(litcovdf, selected_protein)
    
    elif chosen_subtab == 'PPI':
        display_ppi_data(selected_protein)
        
        
    elif chosen_subtab == 'Download':
        info = st.empty()
        info.info('⌛ Generating files')
        pbar = st.progress(10)
        
        tf_activities = display_protein_expressions(
            selected_protein, datacore.name2ds[p_ds], cell_type, disabled=True) 
        pbar.progress(25)
        pbar.progress(30)
        
        csv_path, img_path = display_protein_tf_corr_data(
            selected_protein, cell_type, datacore.name2ds[p_ds], disabled = True)
        pbar.progress(40)
        
        html_ppi, wiki_csv =  display_ppi_data(selected_protein, disabled = True)
        
        if tf_activities is not None:
            buf = BytesIO()
            tf_activities.save(buf, format='PNG')
            png = buf.getvalue()
            
            pbar.progress(45)
            
            download_button(
                    desc = f'{selected_protein} expression density plots\n',
                    label = 'Download as PNG', 
                    data = png, 
                    fname = f'{selected_protein}_tf_activities.png',
                    format="application/octet-stream"
            )

        pbar.progress(55)
        
        pbar.progress(65)
                
        download_button(
                desc = 'Literature references\n', 
                label = 'Download as CSV', 
                data = litcovdf.to_csv(), 
                fname = f'{selected_protein}_litcovid_references.csv'
        )
        
        pbar.progress(75)
        if img_path:
            download_button(
                    desc = f'{selected_protein} protein-tf correlation heatmap\n', 
                    label = 'Download as PNG', 
                    data = img_path2buffer(img_path), 
                    fname = f'{selected_protein}_protein-TF_corr.png'
            )
            
            
            pbar.progress(85)
            
            download_button(
                    desc = f'{selected_protein} tf-protein correlation csv\n', 
                    label = 'Download as CSV', 
                    data = pd.read_csv(csv_path).to_csv(), 
                    fname = f'{selected_protein}_TF-protein_corr.csv'
        )
        
        if html_ppi:
            download_button(
                    desc = f'{selected_protein} StringDB network\n', 
                    label = 'Download as PNG', 
                    data = html_ppi, 
                    fname = f'{selected_protein}_ppi.html'
            )
            
        

        pbar.progress(100)
        info.success('Downloads ready!')
        
        

            
            
        

