


###################################################################################################################################################################################
#Instructions: The input data for replicating the experiment Illustration 3 of the article is configured in this space demarcated with #####.
#To replicate the experiment as it appears in the paper, with all its input values, simply run the script without altering anything.
#If you need to change the mu function values for another archaeological sites and/or to test other values for membership in the functionality and/or chronology categories:
#1. Remember that this script is designed to calculate the fuzzy metrics for the same archaeological site but in different temporal times, for instance in two different temporal excavations or interventions, and compare them with each other. 
# For each intervention, you must specify one mu membership function as explained in the paper: we focus here on one per functionality with the specified categories and a fuzzy value between 0 and 1 per category.
#2. Once you have defined  mu functions for each archaeological intervention (two interventions are required), you can run the script again, and it will give you the values for the framework metrics for your comparison of the sites in two different archaeological interventions.




import pandas as pd



mu_func_sanblas1 = {'A2': 1.00,'D1': 0.25, 'E': 0.50}
mu_func_sanblas2= {'A2': 0.75,'D1': 0.1, 'E': 0.25}


################################################################################################################################################################################


# DataFrame 
sites = pd.DataFrame({
    'site': ['SanBlas1', 'SanBlas1', 'SanBlas2', 'SanBlas2', 'SanBlas2', 'SanBlas2'],
    'func': ['A2', 'D1', 'E', 'A2', 'D1', 'E'],
})

# Function for obtaining mu values
def get_mu(set, mu_funcs):
    return mu_funcs.get(set, 0)

# Function for obtaining CDEG by variable
def cal_cdeg_var(site, var, df, mu_funcs):
    cdeg_vals = []
    for index, row in df.iterrows():
        if row['site'] == site:
            set = row[var]
            degree = get_mu(set, mu_funcs)
            cdeg_vals.append(degree)
    return max(cdeg_vals)

# Calls CDEG calculation by archaeological intervention
cdeg_func_sanblas1 = cal_cdeg_var('SanBlas1', 'func', sites, mu_func_sanblas1)
cdeg_func_sanblas2 = cal_cdeg_var('SanBlas2', 'func', sites, mu_func_sanblas2)

print("\nUncertainty in functionality to monitor changes in knowledge about a single site: San Blas")
print("\nILLUSTRATION 3 EXPERIMENT. RESULTS.")

#Call
print("\nCDEG by archaeological site interventions:")
print(f"SanBlas1 - CDEG(func): {cdeg_func_sanblas1:.4f}")
print(f"SanBlas2 - CDEG(func): {cdeg_func_sanblas2:.4f}")


# CDEGavg calculation by by archaeological intervention
def cal_cdeg_avg_var(site, var, df, mu_funcs):
    values = df[df['site'] == site][var]
    degrees = [get_mu(value, mu_funcs) for value in values]
    if degrees:
        return sum(degrees) / len(degrees)
    return 0

# Calls CDEGavg calculation by by archaeological intervention
cdeg_avg_func_sanblas1 = cal_cdeg_avg_var('SanBlas1', 'func', sites, mu_func_sanblas1)
cdeg_avg_func_sanblas2 = cal_cdeg_avg_var('SanBlas2', 'func', sites, mu_func_sanblas2)

print("\nPROPOSED METRICS & FUZZY FRAMEWORK FOR ARCHAEOLOGICAL LEGACY DATA")

# New metrics CDEGavg and FEQ results
print("\nCDEGavg by interventions:")
print(f"SanBlas1 - CDEGavg(functionality): {cdeg_avg_func_sanblas1:.4f}")
print(f"SanBlas2 - CDEGavg(functionality): {cdeg_avg_func_sanblas2:.4f}")



# CDEG avg (*) calculation by by archaeological intervention (It's the same as CDEGavg(functionality) because we are only evaluationg one variable (functionality))
def cal_cdeg_avg_total(df):
    cdeg_avg_total_sanblas1 = cdeg_avg_func_sanblas1
    cdeg_avg_total_sanblas2 = cdeg_avg_func_sanblas2
    # 
    cdeg_avg_total_sanblas1 = cdeg_avg_total_sanblas1/1
    cdeg_avg_total_sanblas2= cdeg_avg_total_sanblas2/1
    return cdeg_avg_total_sanblas1, cdeg_avg_total_sanblas2
    
    
    
# Call CDEG avg (*) calculation by archaeological site
cdeg_avg_total_sanblas1, cdeg_avg_total_sanblas2=cal_cdeg_avg_total(sites)


# FEQ calculation by pair of archaeological sites
def cal_feq(cdeg_avg_total_sites, site_A, site_B):
    return cdeg_avg_total_sites[site_A] / cdeg_avg_total_sites[site_B]

# Call FEG SanBlas1/SanBlas2
cdeg_avg_total_sites = {'SanBlas1': cdeg_avg_total_sanblas1, 'SanBlas2': cdeg_avg_total_sanblas2}
feq_sanblas1_sanblas2 = cal_feq(cdeg_avg_total_sites, 'SanBlas1', 'SanBlas2')

# Call FEG SanBlas2/SanBlas1
cdeg_avg_total_sites = {'SanBlas2': cdeg_avg_total_sanblas2, 'SanBlas1': cdeg_avg_total_sanblas1}
feq_sanblas2_sanblas1= cal_feq(cdeg_avg_total_sites, 'SanBlas2','SanBlas1')



print(f"SanBlas1 - CDEGavg(*): {cdeg_avg_total_sanblas1:.4f}")
print(f"SanBlas2 - CDEGavg(*): {cdeg_avg_total_sanblas2:.4f}")


print(f"\nFEQ(SanBlas1, SanBlas2): {feq_sanblas1_sanblas2:.4f}")
print(f"\nFEQ(SanBlas2, SanBlas1): {feq_sanblas2_sanblas1:.4f}")
