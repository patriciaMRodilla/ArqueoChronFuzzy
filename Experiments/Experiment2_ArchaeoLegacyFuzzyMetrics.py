

# Martin-Rodilla, P. Tobalina, L. 2025. Python script for replicating Illustration 2 experiment. Uncertainty in use and chronology as dependent variables in San Blas and Sta. Maria de Hito






###########################################################################################################################################################################################################################
#Instructions: The input data for replicating the experiment Illustration 2 of the article is configured in this space demarcated with #####.
#To replicate the experiment as it appears in the paper, with all its input values, simply run the script without altering anything.
#If you need to change the mu function values for another archaeological sites and/or to test other values for membership in the functionality and/or chronology categories:
#1. Remember that the script is designed to calculate the fuzzy metrics for two archaeological sites and compare them with each other. For each site, you must specify two mu membership functions as explained in the paper: one per functionality and one per chronology, with the specified categories and a fuzzy value between 0 and 1 per category. 
# In this specific experiment, functionality fuzzy values are also organized in chronology phases focusing on the functionality variable as a chronology-dependent variable.
#2. Once you have defined the functionality mu functions in chronological phases for each archaeologial site (two are required), you assigned each mu functionality membership function by phase to a cronological category:
# (i.e. 'c1': mu_func_SanBlasPhase1['A2'],  # c1 is associated with Phase 1 of San Blas)
# 3. with these two types of membership functions defined by archaeological site (two are required), you can now run the script again, and it will give you the values for the framework metrics for your two new archaeological sites input data.


import pandas as pd


#Experiment Illustration 2: fuzzy membership functions of both sites (San Blas and Sta. Maria de Hito) focusing on their variable functionality as a chronology-dependent variable. 
# mu functions for functionality variable in different phases
mu_func_SanBlasPhase1 = { 'A2': 1 }
mu_func_SanBlasPhase2 = { 'A1': 0.25 }
mu_func_HitoPhase1 = { 'A2': 0.75 }
mu_func_HitoPhase2 = { 'D1': 1 }
mu_func_HitoPhase3 = { 'D1': 1 }
mu_func_HitoPhase4 = { 'D1': 1 }

# mu functions for functionality as dependent of chronology variable
mu_chronology_sanblas = {
    'c1': mu_func_SanBlasPhase1['A2'],  # c1 is associated with Phase 1 of San Blas
    'c2': mu_func_SanBlasPhase2['A1']   # c2 is associated with Phase 2 of San Blas
}

mu_chronology_hito = {
    'c1': mu_func_HitoPhase1['A2'],  # c1 is associated with Phase 1 of Hito
    'c2': mu_func_HitoPhase2['D1'],  # c2 is associated with Phase 2 of Hito
    'c3': mu_func_HitoPhase3['D1'],  # c3 is associated with Phase 3 of Hito
    'c4': mu_func_HitoPhase4['D1']   # c4 is associated with Phase 4 of Hito
}

###########################################################################################################################################################################################################






# DataFrame 
sites = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'func': ['A2', 'A1', 'A2', 'D1', 'D1', 'D1'],
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
def cal_cdeg_star(site, df, mu_funcs_func, mu_funcs_chronology):
    cdeg_func = cal_cdeg_por_var(site, 'func', df, mu_funcs_func)
    cdeg_chronology = cal_cdeg_por_var(site, 'chronology', df, mu_funcs_chronology)
    return min(cdeg_func, cdeg_chronology)

# Function for calculating CDEGprom
def cal_cdeg_prom(site, df, mu_funcs_func, mu_funcs_chronology):
    degrees = []
    for index, row in df.iterrows():
        if row['site'] == site:
            func_set = row['func']
            chronology_set = row['chronology']
            func_degree = get_mu(func_set, mu_funcs_func)
            chronology_degree = get_mu(chronology_set, mu_funcs_chronology)
            degrees.append(func_degree)
            degrees.append(chronology_degree)
    return sum(degrees) / len(degrees) if degrees else 0

# Function for calculating CDEGprom(functionality)
def cal_cdeg_prom_func(site, df, mu_funcs_func):
    degrees = []
    for index, row in df.iterrows():
        if row['site'] == site:
            func_set = row['func']
            func_degree = get_mu(func_set, mu_funcs_func)
            degrees.append(func_degree)
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
cdeg_star_sanblas = cal_cdeg_star('SanBlas', sites, mu_func_SanBlasPhase1, mu_chronology_sanblas)
cdeg_star_hito = cal_cdeg_star('Hito', sites, mu_func_HitoPhase1, mu_chronology_hito)

cdeg_prom_sanblas = cal_cdeg_prom('SanBlas', sites, mu_func_SanBlasPhase1, mu_chronology_sanblas)
cdeg_prom_hito = cal_cdeg_prom('Hito', sites, mu_func_HitoPhase1, mu_chronology_hito)

cdeg_prom_func_sanblas = cal_cdeg_prom_func('SanBlas', sites, mu_func_SanBlasPhase1)
cdeg_prom_func_hito = cal_cdeg_prom_func('Hito', sites, mu_func_HitoPhase1)

cdeg_prom_chronology_sanblas = cal_cdeg_prom_chronology('SanBlas', sites, mu_chronology_sanblas)
cdeg_prom_chronology_hito = cal_cdeg_prom_chronology('Hito', sites, mu_chronology_hito)


print("ILLUSTRATION 2 EXPERIMENT. RESULTS")

print("CDEG(*) San Blas:", cdeg_star_sanblas)
print("CDEG(*) Hito:", cdeg_star_hito)

print("CDEGprom San Blas:", cdeg_prom_sanblas)
print("CDEGprom Hito:", cdeg_prom_hito)

print("CDEGprom(functionality) San Blas:", cdeg_prom_func_sanblas)
print("CDEGprom(functionality) Hito:", cdeg_prom_func_hito)

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
