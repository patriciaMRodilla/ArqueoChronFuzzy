
# Martin-Rodilla, P. Tobalina, L. 2025. Python script for replicating Illustration 1 experiment. Uncertainty in functionality and chronology as independent variables in San Blas and Sta. Maria de Hito archaeological sites.



import pandas as pd

###################################################################################################################################################################################
#Instructions: The input data for replicating the experiment in Figure 1 of the article is configured in this space demarcated with #####.
#To replicate the experiment as it appears in the paper, with all its input values, simply run the script without altering anything.
#If you need to change the mu function values for another archaeological sites and/or to test other values for membership in the functionality and/or chronology categories:
#1. Remember that the script is designed to calculate the fuzzy metrics for two arcaheological sites and compare them with each other. For each site, you must specify two mu membership functions as explained in the paper: one for functionality and one for chronology, with the specified categories and a fuzzy value between 0 and 1 per category.
#2. Once you have defined the functionality and chronology mu functions for each arcaheologial site (two are required), you can run the script again, and it will give you the values for the framework metrics for your two new archaeological sites input data.


# mu functions for San Blas archaeological site, one per functionality, one per chronologyExplanations on the fuzzy values assigned are in the paper.
mu_func_sanblas = {
    'A2': 1.00,
    'D1': 0.25
}

mu_chronology_sanblas = {
    'c1': 0.75,
    'c2': 0.50
}

# mu functions for Hito archaeological site, one per functionality, one per chronologyExplanations on the fuzzy values assigned are in the paper.
mu_func_hito = {
    'A2': 0.75,
    'D1': 1.00
}

mu_chronology_hito = {
    'c1': 1.00,
    'c2': 0.75,
    'c3': 0.75,
    'c4': 0.75
}

#####################################################################################################################################################################################


#  Construction oh the DataFrames for functionality and chronology variables
df_func = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito'],
    'func': ['A2', 'D1', 'A2', 'D1']
})

df_chronology = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'chronology': ['c1', 'c2', 'c1', 'c2', 'c3', 'c4']
})

# DataFrame for functionality and chronology variables all sites
sites = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'func': ['A2', 'D1', 'A2', 'D1', 0, 0],
    'chronology': ['c1', 'c2', 'c1', 'c2', 'c3', 'c4']
})



# Obtaining mu values
def get_mu(set, mu_funcs):
    return mu_funcs.get(set, 0)
    
    
    
#  CDEG calculation by  variable (functionality or chronology)
def cal_cdeg_por_var(site, var, df, mu_funcs):
    cdeg_vals = []
    for index, row in df.iterrows():
        if row['site'] == site:
            set = row[var]
            degree = get_mu(set, mu_funcs)
            cdeg_vals.append(degree)
    return max(cdeg_vals)

# Calls CDEG calculation by variable (functionality or chronology) and by archeological site
cdeg_func_sanblas = cal_cdeg_por_var('SanBlas', 'func', sites, mu_func_sanblas)
cdeg_chronology_sanblas = cal_cdeg_por_var('SanBlas', 'chronology', sites, mu_chronology_sanblas)
cdeg_func_hito = cal_cdeg_por_var('Hito', 'func', sites, mu_func_hito)
cdeg_chronology_hito = cal_cdeg_por_var('Hito', 'chronology', sites, mu_chronology_hito)

# Calls CDEG total (*), calculation taking minimal value achieved by site
cdeg_total_sanblas = min(cdeg_func_sanblas, cdeg_chronology_sanblas)
cdeg_total_hito = min(cdeg_func_hito, cdeg_chronology_hito)

    

# CDEGprom calculation by  variable (use or chronology)
def cal_cdeg_prom_por_var(site, var, df, mu_funcs):
    values = df[df['site'] == site][var]
    degrees = [get_mu(value, mu_funcs) for value in values]
    if degrees:
        return sum(degrees) / len(degrees)
    return 0

# Calls CDEGprom calculation by  variable (functionality or chronology) and by archeological site
cdeg_prom_func_sanblas = cal_cdeg_prom_por_var('SanBlas', 'func', df_func, mu_func_sanblas)
cdeg_prom_chronology_sanblas = cal_cdeg_prom_por_var('SanBlas', 'chronology', df_chronology, mu_chronology_sanblas)
cdeg_prom_func_hito = cal_cdeg_prom_por_var('Hito', 'func', df_func, mu_func_hito)
cdeg_prom_chronology_hito = cal_cdeg_prom_por_var('Hito', 'chronology', df_chronology, mu_chronology_hito)



# CDEG prom (*) calculation by archaeological site
def cal_cdeg_prom_total(df):
    cdeg_prom_total_sanblas = cal_cdeg_prom_por_var('SanBlas', 'func', df_func, mu_func_sanblas) +  cal_cdeg_prom_por_var('SanBlas', 'chronology', df_chronology, mu_chronology_sanblas)
    cdeg_prom_total_hito = cdeg_prom_use_hito = cal_cdeg_prom_por_var('Hito', 'func', df_func, mu_func_hito) + cal_cdeg_prom_por_var('Hito', 'chronology', df_chronology, mu_chronology_hito)
    
    # 
    cdeg_prom_total_sanblas = cdeg_prom_total_sanblas/2
    cdeg_prom_total_hito= cdeg_prom_total_hito/2
    return cdeg_prom_total_sanblas, cdeg_prom_total_hito
    
    
    
# Call CDEG prom (*) calculation by archaeological site
cdeg_prom_total_sanblas, cdeg_prom_total_hito=cal_cdeg_prom_total(sites)


# FEQ calculation by pair of archaeological sites
def cal_feq(cdeg_prom_total_sites, site_A, site_B):
    return cdeg_prom_total_sites[site_A] / cdeg_prom_total_sites[site_B]

# Call FEG SanBlas/Hito
cdeg_prom_total_sites = {'SanBlas': cdeg_prom_total_sanblas, 'Hito': cdeg_prom_total_hito}
feq_sanblas_hito = cal_feq(cdeg_prom_total_sites, 'SanBlas', 'Hito')

# Call FEG Hito/SanBlas
cdeg_prom_total_sites = {'Hito': cdeg_prom_total_hito, 'SanBlas': cdeg_prom_total_sanblas}
feq_hito_sanblas= cal_feq(cdeg_prom_total_sites, 'Hito','SanBlas')



# CDEG First results
print("\nCDEG by archaeological site:")
print(f"SanBlas - CDEG(func): {cdeg_func_sanblas:.4f}")
print(f"SanBlas - CDEG(chronology): {cdeg_chronology_sanblas:.4f}")
print(f"SanBlas - CDEG(*): {cdeg_total_sanblas:.4f}")
print(f"Hito - CDEG(func): {cdeg_func_hito:.4f}")
print(f"Hito - CDEG(chronology): {cdeg_chronology_hito:.4f}")
print(f"Hito - CDEG(*): {cdeg_total_hito:.4f}")

print(f"PROPOSED METRICS & FUZZY FRAMEWORK FOR ARCHAEOLOGICAL LEGACY DATA")

# New metrics CDEGprom and FEQ results
print("\nCDEGprom by archaeological site:")
print(f"SanBlas - CDEGprom(func): {cdeg_prom_func_sanblas:.4f}")
print(f"SanBlas - CDEGprom(chronology): {cdeg_prom_chronology_sanblas:.4f}")
print(f"SanBlas - CDEGprom(*): {cdeg_prom_total_sanblas:.4f}")
print(f"Hito - CDEGprom(func): {cdeg_prom_func_hito:.4f}")
print(f"Hito - CDEGprom(chronology): {cdeg_prom_chronology_hito:.4f}")
print(f"Hito - CDEGprom(*): {cdeg_prom_total_hito:.4f}")

print(f"\nFEQ(SanBlas, Hito): {feq_sanblas_hito:.4f}")
print(f"\nFEQ(Hito, San Blas): {feq_hito_sanblas:.4f}")


