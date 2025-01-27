import pandas as pd



mu_use_sanblas1 = {'A2': 1.00,'D1': 0.25, 'E': 0.50}
mu_use_sanblas2= {'A2': 0.75,'D1': 0.1, 'E': 0.25}


# DataFrame 
sites = pd.DataFrame({
    'site': ['SanBlas1', 'SanBlas1', 'SanBlas2', 'SanBlas2', 'SanBlas2', 'SanBlas2'],
    'use': ['A2', 'D1', 'E', 'A2', 'D1', 'E'],
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

# Calls CDEG calculation by intervention
cdeg_use_sanblas1 = cal_cdeg_por_var('SanBlas1', 'use', sites, mu_use_sanblas1)
cdeg_use_sanblas2 = cal_cdeg_por_var('SanBlas2', 'use', sites, mu_use_sanblas2)

#Call
print("\nCDEG by archaeological site interventions:")
print(f"SanBlas1 - CDEG(use): {cdeg_use_sanblas1:.4f}")
print(f"SanBlas2 - CDEG(use): {cdeg_use_sanblas2:.4f}")


# CDEGprom calculation by intervention
def cal_cdeg_prom_por_var(site, var, df, mu_funcs):
    values = df[df['site'] == site][var]
    degrees = [get_mu(value, mu_funcs) for value in values]
    if degrees:
        return sum(degrees) / len(degrees)
    return 0

# Calls CDEGprom calculation by intervention
cdeg_prom_use_sanblas1 = cal_cdeg_prom_por_var('SanBlas1', 'use', sites, mu_use_sanblas1)
cdeg_prom_use_sanblas2 = cal_cdeg_prom_por_var('SanBlas2', 'use', sites, mu_use_sanblas2)

print(f"PROPOSED METRICS & FUZZY FRAMEWORK FOR ARCHAEOLOGICAL LEGACY DATA")

# New metrics CDEGprom and FEQ results
print("\nCDEGprom by interventions:")
print(f"SanBlas1 - CDEGprom(use): {cdeg_prom_use_sanblas1:.4f}")
print(f"SanBlas2 - CDEGprom(use): {cdeg_prom_use_sanblas2:.4f}")



# CDEG prom (*) calculation by intervention (It's the same as CDEGprom(use) because we are only evaluationg one variable (use))
def cal_cdeg_prom_total(df):
    cdeg_prom_total_sanblas1 = cdeg_prom_use_sanblas1
    cdeg_prom_total_sanblas2 = cdeg_prom_use_sanblas2
    # 
    cdeg_prom_total_sanblas1 = cdeg_prom_total_sanblas1/1
    cdeg_prom_total_sanblas2= cdeg_prom_total_sanblas2/1
    return cdeg_prom_total_sanblas1, cdeg_prom_total_sanblas2
    
    
    
# Call CDEG prom (*) calculation by archaeological site
cdeg_prom_total_sanblas1, cdeg_prom_total_sanblas2=cal_cdeg_prom_total(sites)


# FEQ calculation by pair of archaeological sites
def cal_feq(cdeg_prom_total_sites, site_A, site_B):
    return cdeg_prom_total_sites[site_A] / cdeg_prom_total_sites[site_B]

# Call FEG SanBlas1/SanBlas2
cdeg_prom_total_sites = {'SanBlas1': cdeg_prom_total_sanblas1, 'SanBlas2': cdeg_prom_total_sanblas2}
feq_sanblas1_sanblas2 = cal_feq(cdeg_prom_total_sites, 'SanBlas1', 'SanBlas2')

# Call FEG SanBlas2/SanBlas1
cdeg_prom_total_sites = {'SanBlas2': cdeg_prom_total_sanblas2, 'SanBlas1': cdeg_prom_total_sanblas1}
feq_sanblas2_sanblas1= cal_feq(cdeg_prom_total_sites, 'SanBlas2','SanBlas1')



print(f"SanBlas1 - CDEGprom(*): {cdeg_prom_total_sanblas1:.4f}")
print(f"SanBlas2 - CDEGprom(*): {cdeg_prom_total_sanblas2:.4f}")


print(f"\nFEQ(SanBlas1, SanBlas2): {feq_sanblas1_sanblas2:.4f}")
print(f"\nFEQ(SanBlas2, SanBlas1): {feq_sanblas2_sanblas1:.4f}")