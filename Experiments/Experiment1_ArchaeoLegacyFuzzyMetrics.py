




import pandas as pd



# mu functions for San Blas archaeological site
mu_use_sanblas = {
    'A2': 1.00,
    'D1': 0.25
}

mu_chronology_sanblas = {
    'c1': 0.75,
    'c2': 0.50
}

# mu functions for Hito archaeological site
mu_use_hito = {
    'A2': 0.75,
    'D1': 1.00
}

mu_chronology_hito = {
    'c1': 1.00,
    'c2': 0.75,
    'c3': 0.75,
    'c4': 0.75
}


#  DataFrames for use and chronology variables
df_use = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito'],
    'use': ['A2', 'D1', 'A2', 'D1']
})

df_chronology = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'chronology': ['c1', 'c2', 'c1', 'c2', 'c3', 'c4']
})

# DataFrame for use and chronology variables all sites
sites = pd.DataFrame({
    'site': ['SanBlas', 'SanBlas', 'Hito', 'Hito', 'Hito', 'Hito'],
    'use': ['A2', 'D1', 'A2', 'D1', 0, 0],
    'chronology': ['c1', 'c2', 'c1', 'c2', 'c3', 'c4']
})



# Obtaining mu values
def get_mu(set, mu_funcs):
    return mu_funcs.get(set, 0)
    
    
    
#  CDEG calculation by  variable (use or chronology)
def cal_cdeg_por_var(site, var, df, mu_funcs):
    cdeg_vals = []
    for index, row in df.iterrows():
        if row['site'] == site:
            set = row[var]
            degree = get_mu(set, mu_funcs)
            cdeg_vals.append(degree)
    return max(cdeg_vals)

# Calls CDEG calculation by variable (use or chronology) and by archeological site
cdeg_use_sanblas = cal_cdeg_por_var('SanBlas', 'use', sites, mu_use_sanblas)
cdeg_chronology_sanblas = cal_cdeg_por_var('SanBlas', 'chronology', sites, mu_chronology_sanblas)
cdeg_use_hito = cal_cdeg_por_var('Hito', 'use', sites, mu_use_hito)
cdeg_chronology_hito = cal_cdeg_por_var('Hito', 'chronology', sites, mu_chronology_hito)

# Calls CDEG total (*) calculation taking minimal value achieved by site
cdeg_total_sanblas = min(cdeg_use_sanblas, cdeg_chronology_sanblas)
cdeg_total_hito = min(cdeg_use_hito, cdeg_chronology_hito)

    

# CDEGprom calculation by  variable (use or chronology)
def cal_cdeg_prom_por_var(site, var, df, mu_funcs):
    values = df[df['site'] == site][var]
    degrees = [get_mu(value, mu_funcs) for value in values]
    if degrees:
        return sum(degrees) / len(degrees)
    return 0

# Calls CDEGprom calculation by  variable (use or chronology) and by archeological site
cdeg_prom_use_sanblas = cal_cdeg_prom_por_var('SanBlas', 'use', df_use, mu_use_sanblas)
cdeg_prom_chronology_sanblas = cal_cdeg_prom_por_var('SanBlas', 'chronology', df_chronology, mu_chronology_sanblas)
cdeg_prom_use_hito = cal_cdeg_prom_por_var('Hito', 'use', df_use, mu_use_hito)
cdeg_prom_chronology_hito = cal_cdeg_prom_por_var('Hito', 'chronology', df_chronology, mu_chronology_hito)



# CDEG prom (*) calculation by archaeological site
def cal_cdeg_prom_total(df):
    cdeg_prom_total_sanblas = cal_cdeg_prom_por_var('SanBlas', 'use', df_use, mu_use_sanblas) +  cal_cdeg_prom_por_var('SanBlas', 'chronology', df_chronology, mu_chronology_sanblas)
    cdeg_prom_total_hito = cdeg_prom_use_hito = cal_cdeg_prom_por_var('Hito', 'use', df_use, mu_use_hito) + cal_cdeg_prom_por_var('Hito', 'chronology', df_chronology, mu_chronology_hito)
    
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
print(f"SanBlas - CDEG(use): {cdeg_use_sanblas:.4f}")
print(f"SanBlas - CDEG(chronology): {cdeg_chronology_sanblas:.4f}")
print(f"SanBlas - CDEG(*): {cdeg_total_sanblas:.4f}")
print(f"Hito - CDEG(use): {cdeg_use_hito:.4f}")
print(f"Hito - CDEG(chronology): {cdeg_chronology_hito:.4f}")
print(f"Hito - CDEG(*): {cdeg_total_hito:.4f}")

print(f"PROPOSED METRICS & FUZZY FRAMEWORK FOR ARCHAEOLOGICAL LEGACY DATA")

# New metrics CDEGprom and FEQ results
print("\nCDEGprom by archaeological site:")
print(f"SanBlas - CDEGprom(use): {cdeg_prom_use_sanblas:.4f}")
print(f"SanBlas - CDEGprom(chronology): {cdeg_prom_chronology_sanblas:.4f}")
print(f"SanBlas - CDEGprom(*): {cdeg_prom_total_sanblas:.4f}")
print(f"Hito - CDEGprom(use): {cdeg_prom_use_hito:.4f}")
print(f"Hito - CDEGprom(chronology): {cdeg_prom_chronology_hito:.4f}")
print(f"Hito - CDEGprom(*): {cdeg_prom_total_hito:.4f}")

print(f"\nFEQ(SanBlas, Hito): {feq_sanblas_hito:.4f}")
print(f"\nFEQ(Hito, San Blas): {feq_hito_sanblas:.4f}")


