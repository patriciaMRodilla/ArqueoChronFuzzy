import pandas as pd


#Experiment 2: fuzzy membership functions of both sites (San Blas and Sta. Maria de Hito) focusing on their variable use as a chronology-dependent variable. 
# mu functions for use variable in different phases
mu_use_SanBlasPhase1 = { 'A2': 1 }
mu_use_SanBlasPhase2 = { 'A1': 0.25 }
mu_use_HitoPhase1 = { 'A2': 0.75 }
mu_use_HitoPhase2 = { 'D1': 1 }
mu_use_HitoPhase3 = { 'D1': 1 }
mu_use_HitoPhase4 = { 'D1': 1 }

# mu functions for use as dependent of chronology variable
mu_chronology_sanblas = {
    'c1': mu_use_SanBlasPhase1['A2'],  # c1 is associated with Phase 1 of San Blas
    'c2': mu_use_SanBlasPhase2['A1']   # c2 is associated with Phase 2 of San Blas
}

mu_chronology_hito = {
    'c1': mu_use_HitoPhase1['A2'],  # c1 is associated with Phase 1 of Hito
    'c2': mu_use_HitoPhase2['D1'],  # c2 is associated with Phase 2 of Hito
    'c3': mu_use_HitoPhase3['D1'],  # c3 is associated with Phase 3 of Hito
    'c4': mu_use_HitoPhase4['D1']   # c4 is associated with Phase 4 of Hito
}
# DataFrame 
sites = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'use': ['A2', 'A1', 'A2', 'D1', 'D1', 'D1'],
    'chronology': ['c1', 'c2', 'c1', 'c2', 'c3', 'c4']
})

# Function for obtaining mu values
def get_mu(set, mu_funcs):
    return mu_funcs.get(set, 0)

# Function for obtaining CDEG by variable
def cal_cdeg_por_var(site, var, df, mu_funcs):
    cdeg_vals = []
    for index, row in df.iterrows():
        if row['site'] == site:
            set = row[var]
            degree = get_mu(set, mu_funcs)
            cdeg_vals.append(degree)
    return max(cdeg_vals)

# Function for calculating CDEG(*)
def cal_cdeg_star(site, df, mu_funcs_use, mu_funcs_chronology):
    cdeg_use = cal_cdeg_por_var(site, 'use', df, mu_funcs_use)
    cdeg_chronology = cal_cdeg_por_var(site, 'chronology', df, mu_funcs_chronology)
    return min(cdeg_use, cdeg_chronology)

# Function for calculating CDEGprom
def cal_cdeg_prom(site, df, mu_funcs_use, mu_funcs_chronology):
    degrees = []
    for index, row in df.iterrows():
        if row['site'] == site:
            use_set = row['use']
            chronology_set = row['chronology']
            use_degree = get_mu(use_set, mu_funcs_use)
            chronology_degree = get_mu(chronology_set, mu_funcs_chronology)
            degrees.append(use_degree)
            degrees.append(chronology_degree)
    return sum(degrees) / len(degrees) if degrees else 0

# Function for calculating CDEGprom(use)
def cal_cdeg_prom_use(site, df, mu_funcs_use):
    degrees = []
    for index, row in df.iterrows():
        if row['site'] == site:
            use_set = row['use']
            use_degree = get_mu(use_set, mu_funcs_use)
            degrees.append(use_degree)
    return sum(degrees) / len(degrees) if degrees else 0

# Function for calculating CDEGprom(chronology)
def cal_cdeg_prom_chronology(site, df, mu_funcs_chronology):
    degrees = []
    for index, row in df.iterrows():
        if row['site'] == site:
            chronology_set = row['chronology']
            chronology_degree = get_mu(chronology_set, mu_funcs_chronology)
            degrees.append(chronology_degree)
    return sum(degrees) / len(degrees) if degrees else 0

# Calculation of CDEG(*) and CDEGprom for each site with the new membership functions
cdeg_star_sanblas = cal_cdeg_star('SanBlas', sites, mu_use_SanBlasPhase1, mu_chronology_sanblas)
cdeg_star_hito = cal_cdeg_star('Hito', sites, mu_use_HitoPhase1, mu_chronology_hito)

cdeg_prom_sanblas = cal_cdeg_prom('SanBlas', sites, mu_use_SanBlasPhase1, mu_chronology_sanblas)
cdeg_prom_hito = cal_cdeg_prom('Hito', sites, mu_use_HitoPhase1, mu_chronology_hito)

cdeg_prom_use_sanblas = cal_cdeg_prom_use('SanBlas', sites, mu_use_SanBlasPhase1)
cdeg_prom_use_hito = cal_cdeg_prom_use('Hito', sites, mu_use_HitoPhase1)

cdeg_prom_chronology_sanblas = cal_cdeg_prom_chronology('SanBlas', sites, mu_chronology_sanblas)
cdeg_prom_chronology_hito = cal_cdeg_prom_chronology('Hito', sites, mu_chronology_hito)

print("CDEG(*) San Blas:", cdeg_star_sanblas)
print("CDEG(*) Hito:", cdeg_star_hito)

print("CDEGprom San Blas:", cdeg_prom_sanblas)
print("CDEGprom Hito:", cdeg_prom_hito)

print("CDEGprom(use) San Blas:", cdeg_prom_use_sanblas)
print("CDEGprom(use) Hito:", cdeg_prom_use_hito)

print("CDEGprom(chronology) San Blas:", cdeg_prom_chronology_sanblas)
print("CDEGprom(chronology) Hito:", cdeg_prom_chronology_hito)

# Function for calculating CDEGprom(*) by archaeological site
def cal_cdeg_prom_star(site, df, mu_funcs_chronology):
    degrees = []
    for index, row in df[df['site'] == site].iterrows():
        chronology_set = row['chronology']
        chronology_degree = get_mu(chronology_set, mu_funcs_chronology)
        degrees.append(chronology_degree)
    return sum(degrees) / len(degrees) if degrees else 0

# Calculation of CDEGprom(*) by archaeological site (chronology as independent variable, use as dependent variable)
cdeg_prom_star_sanblas = cal_cdeg_prom_star('SanBlas', sites, mu_chronology_sanblas)
cdeg_prom_star_hito = cal_cdeg_prom_star('Hito', sites, mu_chronology_hito)

print("CDEGprom(*) para San Blas:", cdeg_prom_star_sanblas)
print("CDEGprom(*) para Hito:", cdeg_prom_star_hito)