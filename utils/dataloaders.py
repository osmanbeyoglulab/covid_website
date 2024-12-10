from pathlib import Path
from typing import Tuple
import pandas as pd
import streamlit as st
from texts.references import CELL_NAMES, CELL_NAMES_REVERSE
import toml

cutsize_from = 30
cutsize_to = 10000

fuzzy_match = lambda root, fname: list(root.glob(fname))[0]

gse2auth = {
    'GSE161918' : 'LIU',
    'E-MTAB-9357' : 'SU',
    'GSE155673' : 'AR',
    'GSE155224' : 'UN',
    'E-MTAB-10026' : 'ST'
}

IMG_REPO = 'https://raw.githubusercontent.com/osmanbeyoglulab/covid19_webapp/main/data/'
IMG_REPO2 = 'https://raw.githubusercontent.com/matthewlu2/spartan_webapp_data/main'
IMG_REPO3 = 'https://raw.githubusercontent.com/matthewlu2/covid_data/main'

class Dataset:

    def __init__(self, root):
        self.root = root
        self.name = self.root.name
        self.celltypes = [CELL_NAMES.get(i.name, i.name) for i in self.root.iterdir()]
        self.celltypes = list(filter(lambda x: x != "metadata.toml", self.celltypes))
        self.celltypes = list(filter(lambda x: "featurePlot" not in x, self.celltypes))
        
        self.umap = str(Path('./data/umaps/') / f'UMAP_{self.name}.png')
        
    
    def counts(self, option_protein, is_protein):
        self.celltype2counts = {}
        for cell_type in self.celltypes:
            try:
                if is_protein:
                    csv, img = self.get_viral_protein_data(cell_type, option_protein)
                else:
                    csv, img = self.get_viral_mrna_data(cell_type, option_protein)
                return pd.read_csv(csv).group.value_counts()
            except:
                return pd.DataFrame()
                    
    def get_tf_pvals(self, celltype: str, protein: str) -> Tuple[float, float]:
        celltype = CELL_NAMES_REVERSE[celltype]
        pth =  (self.root / celltype).glob('TFrank_wilcox_pvalues_*.csv')
        pth = [i for i in pth if 'viral' not in str(i)][0]
        pvals = pd.read_csv(pth)        
        _, pval, adj_pval = pvals[pvals.features_all==protein].values[0]
        return pval, adj_pval
    
    def get_protein_pvals(self, celltype: str, protein: str) -> Tuple[float, float]:
        celltype = CELL_NAMES_REVERSE[celltype]
        pth =  (self.root / celltype).glob('protein_wilcox_pvalues_*.csv')
        pth = [i for i in pth if 'viral' not in str(i)][0]
        pvals = pd.read_csv(pth)
        _, pval, adj_pval = pvals[pvals.features_all==protein].values[0]
        return pval, adj_pval
    
        
    def surface_proteins(self, celltype: str) -> list:
        celltype = CELL_NAMES_REVERSE[celltype]
        proteins = (self.root / celltype / 'protein-TFs_highCorr').iterdir()
        proteins = [i.name.split('~TFs_highCorr_corrcut_')[0] for i in proteins]
        proteins = list(filter(lambda x: x != ".gitkeep" or x!= "metadata.toml", proteins))
        return proteins
        
    @property
    def total_surface_proteins(self) -> list:
        proteins = set()
        for ct in self.celltypes:
            ct = CELL_NAMES_REVERSE[ct]
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'proteins_all_*~*_withGroup.csv')).columns:
                proteins.add(p)
        proteins = proteins.difference({'Unnamed: 0', 'group'})
        return proteins
    
    @property
    def total_transcription_factors(self) -> list:
        tfs = set()
        for ct in self.celltypes:
            ct = CELL_NAMES_REVERSE[ct]
            for p in pd.read_csv(fuzzy_match((self.root / ct), 'TFs_rank_all_*~*_withGroup.csv')).columns:
                tfs.add(p)
        tfs = tfs.difference({'Unnamed: 0', 'group'})
        return tfs
    
    def transcription_factors(self, celltype: str) -> list:
        celltype = CELL_NAMES_REVERSE[celltype]
        tfs = (self.root / celltype / 'TF-proteins_highCorr').iterdir()
        tfs = [i.name.split('~proteins_highCorr_corrcut_')[0] for i in tfs]
        tfs = list(filter(lambda x: x != ".gitkeep", tfs))
        return tfs
    
    
    def get_protein_tf_data(self, celltype: str, protein: str) -> list:
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'protein-TFs_highCorr'
        #github
        # img =  list((base / 'Figure').glob(f'{protein}~TFs_highCorr*'))[0]
        img = f'{IMG_REPO3}/{self.name}/{celltype}/protein-TFs_highCorr/Figure/{protein}~TFs_highCorr_corrcut.png'
        csv = list((base).glob(f'{protein}~TFs_highCorr*.csv'))[0]        
        return (str(csv), str(img))
    
    def get_tf_target_gene_img(self, celltype: str, tf: str) -> str:
        celltype = CELL_NAMES_REVERSE[celltype]
        # base = self.root / celltype / 'TF-mRNAs_highCorr' / 'Figure'
        #github
        # img =  list(base.glob(f'{tf}~mRNAs_highCorr_corrcut_*'))[0]
        img = f'{IMG_REPO3}/{self.name}/{celltype}/TF-mRNAs_highCorr/Figure/{tf}~mRNAs_highCorr_corrcut.png'
        return str(img)
    
    
    def get_tf_protein_data(self, celltype: str, tf: str) -> Tuple[str, str]:
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'TF-proteins_highCorr'   
        #github
        # img = list((base / 'Figure').glob(f'{tf}~proteins_highCorr_corrcut_*'))[0]   
        img = f'{IMG_REPO3}/{self.name}/{celltype}/TF-proteins_highCorr/Figure/{tf}~proteins_highCorr_corrcut.png'   
        csv = list((base).glob(f"{tf}~proteins_highCorr_corrcut_*.csv"))[0]
        return (str(csv), str(img))
    
    
    def get_feature_plots(self, protein: str) -> str:
        # img = self.root / 'featurePlot_protein' / f'{gse2auth[self.name]}_featurePlot_{protein}.png'
        img = f'{IMG_REPO2}/{self.name}/featurePlot_protein/{gse2auth[self.name]}_featurePlot_{protein}.png'
        return str(img)
    
    def get_gene_plots(self, gene: str) -> str:
        # img = self.root / 'featurePlot_gene' / f'{gse2auth[self.name]}_gene_featurePlot_{gene}.png'
        img = f'{IMG_REPO}/{self.name}/featurePlot_gene/{gse2auth[self.name]}_gene_featurePlot_{gene}.png'
        return str(img)
        
    def get_umap_severity(self) -> Tuple[str, str]:
        # umap = self.root / 'featurePlot_protein' / f'{gse2auth[self.name]}_UMAP.png'
        umap = f'{IMG_REPO2}/{self.name}/featurePlot_protein/{gse2auth[self.name]}_UMAP.png'
        # severity = self.root / 'featurePlot_protein' / f'{gse2auth[self.name]}_severityPlot.png'
        severity = f'{IMG_REPO2}/{self.name}/featurePlot_protein/{gse2auth[self.name]}_severityPlot.png'
        return str(umap), str(severity)
            
    
    def get_tf_df(self, celltype: str, protein: str) -> pd.DataFrame:
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'TFs_rank_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    
    def get_protein_df(self, celltype: str, protein: str) -> pd.DataFrame:
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'proteins_all_*~*_withGroup.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    
    def get_viral_proteins(self, celltype: str) -> list:
        celltype = CELL_NAMES_REVERSE[celltype]
        proteins = (self.root / celltype / 'protein-TFs_highCorr_viral').iterdir()
        proteins = [i.name.split('~TFs_highCorr_corrcut_')[0] for i in proteins]
        proteins = list(filter(lambda x: x != ".gitkeep" or x != "metadata.toml", proteins))
        return list(set(proteins))
    
    
    def get_viral_mrnas(self, celltype: str) -> list:
        celltype = CELL_NAMES_REVERSE[celltype]
        proteins = (self.root / celltype / 'mRNA-TFs_highCorr_viral').iterdir()
        try:
            proteins = [i.name.split('~TFs_highCorr_corrcut_')[0] for i in proteins]
            proteins = list(filter(lambda x: x != ".gitkeep" or x != "metadata.toml", proteins))
        except:
            proteins = []
        return list(set(proteins))
    
    
    def get_viral_protein_data(self, celltype: str, protein: str) -> Tuple[str, str]:
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'protein-TFs_highCorr_viral'
        # img =  list((base / 'Figure').glob(f'{protein}~TFs_highCorr*'))[0]
        img = f'{IMG_REPO3}/{self.name}/{celltype}/protein-TFs_highCorr_viral/Figure/{protein}~TFs_highCorr_corrcut.png'
        csv = list((base).glob(f'{protein}~TFs_highCorr*.csv'))[0]        
        return (str(csv), str(img))
    
    
    def get_viral_mrna_data(self, celltype: str, protein: str) -> Tuple[str, str]:
        celltype = CELL_NAMES_REVERSE[celltype]
        base = self.root / celltype / 'mRNA-TFs_highCorr_viral'
        # img =  list((base / 'Figure').glob(f'{protein}~TFs_highCorr*'))[0]
        img = f'{IMG_REPO3}/{self.name}/{celltype}/mRNA-TFs_highCorr_viral/Figure/{protein}~TFs_highCorr_corrcut.png'
        csv = list((base).glob(f'{protein}~TFs_highCorr*.csv'))[0]        
        return (str(csv), str(img))
    
    def get_viral_mrna_df(self, celltype: str, protein: str) -> pd.DataFrame:
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'mRNAs_all_*~*_withGroup_viral.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
    
    def get_viral_protein_df(self, celltype: str, protein: str) -> pd.DataFrame:
        celltype = CELL_NAMES_REVERSE[celltype]
        df_data = pd.read_csv(fuzzy_match((self.root / celltype), 'proteins_all_*~*_withGroup_viral.csv'))
        df_plt = pd.DataFrame([df_data.group, df_data[protein]]).T
        df_plt.columns = ['patient_group', 'Pair_correlations']
        return df_plt
    
      
      

        
        
    

class Datacore:
    
    def __init__(self):
        self.root_path = Path('./data/')
        datasets = list(filter(lambda x: x != ".gitkeep" or x != "metadata.toml", (self.root_path / 'data').iterdir()))
        self.datasets = [Dataset(i) for i in datasets]
        self.name2ds = dict(zip([ds.name for ds in self.datasets], self.datasets))
        self.metadata = pd.DataFrame([toml.load(ds.root / 'metadata.toml') for ds in self.datasets])

# @st.experimental_singleton
def make_datacore():
    return Datacore

