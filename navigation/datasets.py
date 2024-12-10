import streamlit as st

from utils.components import local_css
from texts.descriptions import DatasetDesc, Desc

import os
import hydralit_components as hc

option_data = [
   {'icon': "", 'label':i} for i in ['Metadata', 'Visualization']]

over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'white','option_active':'darkviolet'}
font_fmt = {'font-class':'h3','font-size':'50%'}


EMTAB10026proteins = ['CD163', 'CD66a', 'CD357', 'CD161', 'CD21', 'CD319', 'Phospho-Tau', 'CD258', 'TCR-Vb13-1', 'CD22', 'HLA-ABC', 'CD371', 'CD184', 'CD158', 'CD11c', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'CD137', 'CD223', 'TCR-Va24-Ja18', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'CD197', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'CD15', 'c-Met', 'CD16', 'CD86', 'TCR-Vg9', 'CD278', 'CD4', 'Podoplanin', 'CD38', 'CD25', 'CD62L', 'CD69', 'CD224', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD324', 'CD209', 'HLA-F', 'NCR3', 'CD235ab', 'CD26', 'NLRP2', 'CD158b', 'CD45', 'CD95', 'XCR1', 'CD141', 'CD49f', 'CD18', 'CD36', 'CD2', 'CD41', 'CD183', 'HLA-A2', 'CD101', 'CD44', 'IgLambdaLight', 'CD120a', 'CD150', 'Mac-2', 'CX3CR1', 'CLEC15A', 'CD314', 'CD307d', 'CD99', 'CD244', 'CD370', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD40LG', 'CD33', 'CD226', 'CD127', 'CD133', 'CD138', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD274', 'CD195', 'CD90', 'IgKappaLight', 'CD27', 'CD307e', 'TCR-G-D', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'CD62', 'IgD', 'CD328', 'CD96', 'CD39', 'CD98', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD1C', 'CD137L', 'CD196', 'ITGB7', 'CD28', 'CD71', 'CD11b', 'LOX-1', 'CD94', 'CD8', 'CD24', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'TCR-Vg2', 'CD32']
EMTAB9357proteins = ['CD357', 'CD319', 'CD101', 'HLA', 'B7', 'CD150', 'CD184', 'c', 'CD158', 'CX3CR1', 'CD307d', 'CD99', 'CD244', 'CD11c', 'CD11a', 'CD275', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'CD3', 'CD124', 'IgA', 'CD81', 'CD305', 'CD7', 'FCERIA', 'CD303', 'CD123', 'CD137', 'CD144', 'CD223', 'CD58', 'CD335', 'DR3', 'CD169', 'CD82', 'CD49d', 'CD5', 'CD257', 'CD33', 'CD85j', 'CD88', 'CD226', 'CD127', 'CD1c', 'CD197', 'TSLPR', 'CD133', 'CD73', 'CD326', 'CD138', 'CD19', 'CD45RA', 'CD155', 'CD207', 'CD336', 'CD254', 'CD360', 'CD269', 'CD56', 'CD35', 'CD122', 'Ig', 'CD16', 'CD64', 'CD337', 'CD86', 'KLRG1', 'CD278', 'CD195', 'CD4', 'CD38', 'Podoplanin', 'CD154', 'CD62L', 'CD69', 'CD30', 'CD224', 'CD178', 'CD29', 'CD47', 'CD45RO', 'CD206', 'CD52', 'CD70', 'CD107a', 'CD39', 'CD96', 'TCR', 'Tau', 'CD98', 'CD57', 'CD54', 'CD204', 'CD324', 'CD31', 'CD26', 'CD366', 'NLRP2', 'CD158b', 'CD45', 'Mac', 'CD95', 'CD137L', 'XCR1', 'CD71', 'ITGB7', 'CD28', 'CD11b', 'CD94', 'CD141', 'CD24', 'CD8', 'CD49f', 'CD36', 'CD18', 'CD2', 'CD66b', 'CD279', 'CD14', 'CD41', 'CLEC12A', 'CD183', 'CD32']
GSE155224proteins = ['CD163', 'CD357', 'CD319', 'CD161', 'CD21', 'CD258', 'HLA', 'CD22', 'CD184', 'TCR-Vr9', 'CD158', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'CD137', 'CD223', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'CD15', 'CD16', 'CD278', 'CD4', 'Podoplanin', 'CD38', 'CD154', 'CD25', 'CD62L', 'CD69', 'CD30', 'CD224', 'TCR-Va24-Jz18', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD209', 'CD324', 'HLA-F', 'CD26', 'NLRP2', 'CD158b', 'CD95', 'XCR1', 'CD141', 'CD49f', 'CD18', 'CD36', 'CD2', 'CD41', 'CLEC12A', 'CD62P', 'HLA-A2', 'CD101', 'CD150', 'Mac-2', 'CX3CR1', 'CD314', 'CD307d', 'CD244', 'CD370', 'CD40', 'CD158f', 'TIGIT', 'CD1d', 'TCR-A-B', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'integrin', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD33', 'TCR-Vb13', 'CD226', 'CD127', 'CD1c', 'CD133', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'Ig-light-chain-1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD337', 'KLRG1', 'CD274', 'CD195', 'CD90', 'Ig-light-chain-2', 'CD27', 'CD307e', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'IgD', 'CD328', 'CD96', 'CD39', 'CD98', 'TCR-Vd2', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD66', 'CD137L', 'CD196', 'CD28', 'CD71', 'LOX-1', 'CD94', 'CD24', 'CD8', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'CD32']
GSE155673proteins = ['CD163', 'CD56', 'HLA', 'CD16', 'CD86', 'CD274', 'CD4', 'CD38', 'CD370', 'CD11c', 'CD25', 'CD27', 'CD69', 'CD3', 'TCR-G-D', 'CD20', 'CD34', 'TCR-Va7-2', 'CD45RO', 'CD123', 'FCER1A', 'Anti-PE', 'CD33', 'CD28', 'CD95', 'CD127', 'CD1c', 'CD94', 'CD197', 'CD8', 'CD279', 'CD14', 'CD19', 'CD45RA']
GSE161918proteins = ['CD163', 'CD357', 'CD319', 'CD161', 'CD21', 'Phospho-Tau', 'CD258', 'CD22', 'HLA-ABC', 'CD184', 'CD158', 'CD11c', 'CD275', 'CD11a', 'CD103', 'CD3', 'CD124', 'CD66ace', 'B7-H4', 'CD34', 'FCERIA', 'CD10', 'CD123', 'CD303', 'IgG1Kiso', 'CD137', 'CD223', 'CD335', 'DR3', 'CD169', 'CD268', 'CD82', 'IgM', 'CD83', 'CD257', 'CD117', 'CD85j', 'CD88', 'CD49b', 'CD294', 'CD112', 'CD152', 'CD1a', 'CD197', 'TSLPR', 'CD73', 'CD326', 'CD19', 'CD45RA', 'CD155', 'CD336', 'CD254', 'IgG-Fc', 'CD269', 'CD360', 'CD56', 'IgG2aKiso', 'CD15', 'c-Met', 'CD16', 'CD86', 'TCR-Vg9', 'CD278', 'CD4', 'CD38', 'Podoplanin', 'CD154', 'CD25', 'CD62L', 'CD69', 'CD30', 'CD224', 'TCR-Va24-Jz18', 'CD45RO', 'CD206', 'CD52', 'TCR', 'CD324', 'CD209', 'HLA-F', 'ratIgG2bKiso', 'CD235ab', 'CD26', 'NLRP2', 'CD158b', 'CD45', 'CD95', 'XCR1', 'CD141', 'CD18', 'CD49f', 'CD36', 'CD2', 'CD41', 'CLEC12A', 'CD183', 'CD62P', 'CD101', 'CD44', 'IgLambdaLight', 'CD150', 'Mac-2', 'CX3CR1', 'CD314', 'CD307d', 'CD99', 'CD244', 'CD370', 'CD40', 'CD158f', 'CD1d', 'TIGIT', 'TCR-A-B', 'IgA', 'CD81', 'CD304', 'CD305', 'CD7', 'CD309', 'CD144', 'integrin', 'CD185', 'CD58', 'CD106', 'CD267', 'GARP', 'CD272', 'CD49d', 'CD5', 'CD33', 'CD127', 'CD226', 'CD1c', 'CD133', 'CD138', 'HLA-DR', 'Podocalyxin', 'CD158e1', 'CD146', 'CD207', 'CD35', 'CD122', 'CD193', 'CD64', 'CD337', 'KLRG1', 'CD274', 'CD195', 'CD90', 'IgKappaLight', 'CD27', 'CD307e', 'TCR-G-D', 'CD178', 'CD29', 'CD20', 'CD47', 'TCR-Va7-2', 'CD70', 'CD107a', 'CD23', 'IgD', 'CD328', 'CD39', 'CD96', 'CD98', 'TCR-Vd2', 'CD194', 'CD54', 'CD204', 'CD79b', 'CD252', 'CD31', 'CD273', 'CD366', 'CD137L', 'CD196', 'CD28', 'CD71', 'CD11b', 'LOX-1', 'CD94', 'CD8', 'CD24', 'CD66b', 'CD279', 'CD80', 'CD14', 'CD57', 'CD32']

def totags(tags):
    t = '<div>'
    for tag, color in zip(tags, ['red', 'blue', 'green', 'orange', 'purple', 'yellow']):
        t += f"<span class='highlight {color}'>{tag}</span>\t"
    t += '</div>'
    return t


def dataset_page(ds, datacore):
        
    st.markdown(f'### Dataset Browser')
    st.info(Desc.ds)
    st.caption('Select one or more datasets')
    ds2 = ds[['name', 'patients', 'cell_count', 'surface_proteins', 'transcription_factors', 'pmid']]
    
    
    
    box, p, c, pt, tf, pm = st.columns([2, 1, 1, 1, 1, 1])
    box.markdown('##### Name')
    p.markdown('##### Patients')
    c.markdown('##### Cells')
    pt.markdown('##### Proteins')
    tf.markdown('##### TFs')
    pm.markdown('##### PMID')

    bbox = {}
    
    for name, patients, cells, proteins, tfs, pmid in ds2.values:
        bbox[name] = box.checkbox(f'{name}', key=f'datasets_{name}')  
        p.write(str(patients))  
        c.write(cells)
        pt.write(str(proteins))
        tf.write(str(tfs))
        pm.markdown(f'[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)')
        

    st.markdown('---')

    
    page = hc.option_bar(
        option_definition=option_data,
        title='',
        override_theme=over_theme,
        horizontal_orientation=True
    )
    
    for name, is_selected in bbox.items():
        if is_selected:
            if page == 'Metadata':
                st.markdown('#### ' + name + ': ' + ds[ds.name==name].title.values[0])
                st.markdown(DatasetDesc[name])
                st.markdown(ds[ds.name==name].url.values[0])
                
                local_css()
                row_json = ds[ds.name==name]
            
                st.markdown(
                    totags([
                        row_json['cell_count'].values[0] + ' cells', 
                        str(row_json['patients'].values[0]) + ' patients',
                        str(row_json['surface_proteins'].values[0]) + ' surface proteins',
                        str(row_json['transcription_factors'].values[0]) + ' transcription factors',
                        
                        ],
                    ), 
                    unsafe_allow_html=True)
                
                st.markdown('---')
                
            elif page == 'Visualization':
                st.caption('Note: UMAPs were generated using mRNA expression data.')
                # try:
                umap_img, severity_img = datacore.name2ds[name].get_umap_severity()
                f, sa, sb = st.columns(3)
                s_proteins = []
                if (name == 'E-MTAB-10026'):
                    s_proteins = EMTAB10026proteins
                elif (name == 'E-MTAB-9357'):
                    s_proteins = EMTAB9357proteins
                elif (name == 'GSE155224'):
                    s_proteins = GSE155224proteins
                elif (name == 'GSE155673'):
                    s_proteins = GSE155673proteins
                elif (name == 'GSE161918'):
                    s_proteins = GSE161918proteins

                # s_proteins = list(datacore.name2ds[name].total_surface_proteins)
                # st.text(s_proteins)
                f.markdown(f'## {name}')
                # st.text(umap_img)
                # st.text(severity_img)
                umap, sev = st.columns(2)
                prot, gene = st.columns(2)
                
                # if os.path.isfile(umap_img):
                with umap:
                    with st.spinner('🎨 Coloring by Celltype...'):
                        umap.caption('Color by Celltype')
                        umap.image(umap_img)
                    
                # if os.path.isfile(severity_img):
                with sev:
                    with st.spinner('🎨 Coloring by Severity...'):
                        sev.caption('Color by Severity')
                        sev.image(severity_img)
                            
                            
                # if os.path.isfile(umap_img):
                    
                # s_genes = [i.name.split('_featurePlot_')[-1][:-4] for i in (datacore.name2ds[name].root / 'featurePlot_gene').glob('*.png')]
                s_genes = ds[ds.name==name].genes.values[0].split()
                                        
                selected_protein = sa.selectbox(
                    f"Surface protein of interest ({len(s_proteins)})",
                    s_proteins)
                
                selected_gene = sb.selectbox(
                    f"Gene of interest ({len(s_genes)})",
                    s_genes)
                    
                         
                with prot:
                    with st.spinner('🎨 Coloring by Protein...'):                    
                        prot.caption('Color by Protein Expression')
                        i = datacore.name2ds[name].get_feature_plots(selected_protein)
                        # st.text(i)
                        prot.image(i)
                        
                with gene:
                    with st.spinner('🎨 Coloring by Gene...'): 
                        gene.caption('Color by Gene Expression')                   
                        gene.image(datacore.name2ds[name].get_gene_plots(selected_gene))
                            
                # except Exception as e:
                #     st.error('No UMAPs available for this dataset')
                #     # st.write(e)
                
                st.markdown('---')  
                

        
        
