import os
import scanpy as sc
import squidpy as sq
import pandas as pd
import matplotlib.pyplot as plt
import anndata as ad

# data read in
base_dir = os.path.dirname(os.path.abspath(__name__))

# Define the data directory relative to the base directory
data_dir = os.path.join(base_dir, "data", "SC_DATA")
modified_dir = os.path.join(base_dir, "data", "SC_DATA", "modified")

# Read 10x Genomics filtered feature-barcode matrix
adata_5p = sc.read_10x_h5(os.path.join(data_dir, "GSM7782696_5p_count_filtered_feature_bc_matrix.h5"))
adata_5p.var_names_make_unique()

adata_3p = sc.read_10x_h5(os.path.join(data_dir, "GSM7782697_3p_count_filtered_feature_bc_matrix.h5"))
adata_3p.var_names_make_unique()

# Read spatial data
adata_spatial = sq.read.visium(counts_file = os.path.join(data_dir, "GSM7782699_filtered_feature_bc_matrix.h5"), 
                                load_images = True, 
                                path = os.path.join(data_dir))


for adata in [adata_3p, adata_5p, adata_spatial]:
    adata.obs_names_make_unique()
    adata.var_names_make_unique()


# spatial to be added to new layer
adata_sc = ad.concat([adata_3p, adata_5p], join = 'outer', keys = ['3prime', '5prime'], index_unique = "-")
adata_combined = ad.AnnData(X = None)

adata_combined.raw = adata_sc
adata_combined.uns['spatial'] = adata_spatial

adata_combined.uns['data_types'] = {
    'single_cell': 'stored in raw',
    'spatial': 'stored in uns["spatial"]'
}

adata_combined.write_h5ad(os.path.join(modified_dir, "sc_and_spatial.h5ad"), compression = "gzip")


my_feat = "CD3E"
# Create a spatial scatter plot for the gene of interest
sq.pl.spatial_scatter(
    adata_spatial,
    library_id='CytAssist_FFPE_Human_Breast_Cancer',
    color=my_feat,
    img=True,
    vmin=0,  # Set this according to your data range
    vmax=adata_spatial.raw.X[:, adata_spatial.raw.var_names == my_feat].mean(),  # Max value for the gene
    cmap='viridis'  # Choose your colormap
)

# Add a colorbar manually with a title
cbar = plt.colorbar(label=my_feat)  # Set the label for the colorbar

# Show the plot
plt.show()