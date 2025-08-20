import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go


#test the setting up:
print("hello")
print("Skin and softt tissue infection (SSI) after open and minimally invasive surgery")

#import data + first glance:
df=pd.read_csv("~/Desktop/mini_project_1/RawData.csv")
print(df.head)
print(df.shape) #189 rows x 7 columns (189 patients x 7 vars)
print(df.columns) #Index(['SSI', 'Gender', 'Approach', 'PreOPCRP', 'PostOpCRP', 'PreOpAlbumin', 'PreOpWCC'], dtype='object')
print(df.dtypes)

#   Research Questions:
#1. Descriptive statistics
#2. Is the presence of SSI independent (or dependent) from surgical approach?
#3. Is the presence of SSI independent (or dependent) from gender?
#4. Is there a significant difference in the rise of CRP (before and after surgery) b/w patients with and without SSI
#5. Is there a significant difference in pre-operative albumin level (PreOpAlbumin) b/w patients with and without SSI
#6. Is there a significant difference in pre-operative white cell counts b/w patients with and without SSI


## 1. DESCRIPTIVE STATISTICS:
#case: SSI Yes
#ctrl: SSI No

if len(df[df.SSI == "No"]) == len(df[df.SSI != "No"]):
    print("Sample sizes between groups are equal")
else:
    print("Sample size between group are not equal")
    
print(df.Gender.value_counts(normalize = True) * 100) #Gender Female: 57.142857% | Male: 42.857143%

#--create a contingency table:
print(pd.crosstab(df["SSI"],
                  df["Gender"]))
#Gender  Female  Male
#SSI                 
#No          95    67
#Yes         13    14

#-- % by group:
print(df.groupby("SSI").Gender.value_counts(normalize = True) * 100)
#SSI  #Gender
#No   Female    58.641975
#     Male      41.358025
#Yes  Male      51.851852
#     Female    48.148148

# A) C-REACTIVE PROTEINS
#--Add a column showing change in C-reactive protein
df["CRPDelta"]=df["PostOpCRP"]-df["PreOPCRP"]
print(df.head(7))
print(df["CRPDelta"].describe())

 #count    189.000000
#mean       2.788360
#std        2.020552
#min        0.000000
#25%        1.000000
#50%        3.000000
#75%        4.000000
#max       10.000000
#Name: CRPDelta, dtype: float64

print(df.groupby("SSI").CRPDelta.describe())
#     count      mean       std  min  25%  50%  75%   max
#SSI                                                     
#No   162.0  2.388889  1.557391  0.0  1.0  2.0  4.0   5.0
#Yes   27.0  5.185185  2.746145  0.0  3.0  6.0  7.0  10.0

#--make a boxplot of control distribution:
trace0 = go.Box(y = df[df["SSI"] == "No"]["CRPDelta"],
                name = "No SSI",
                marker = {"color": "rgb(20, 52, 164)"},
                boxpoints = "outliers")

trace1= go.Box(y = df[df["SSI"] != "No"]["CRPDelta"],
               name = "SSI",
               marker = {"color": "rgb(136, 8, 8)"},
               boxpoints = "outliers")

data=[trace0, trace1]
layout={"title":"Difference in C-reactive Protein after Surgery",
       "xaxis": {"title":"SSI Status", "zeroline": False },
       "yaxis": {"title":"CRP Level (mg/dL)", "zeroline" : False}
       }
fig = go.Figure(data=data, layout=layout) 
fig.show()

# B) ALBUMIN
print(df.groupby("SSI")["PreOpAlbumin"].describe())
#SSI                                                       
#No   162.0  4.533951  1.055725  1.4  3.90  4.55  5.10  7.7
#Yes   27.0  4.192593  2.399187  0.2  2.45  4.30  5.85  9.9

trace2 = go.Box(y = df[df["SSI"] =="No"]["PreOpAlbumin"],
                name = "No SSI",
                marker = {"color": "rgb(20, 52, 164)"},
                boxpoints = "outliers")
trace3 = go.Box(y = df[df.SSI !="No"].PreOpAlbumin, 
                name= "SSI",
                marker = {"color":"rgb(136, 8, 8)"},
                boxpoints = "outliers")
data1=[trace2, trace3]
layout1={"title":"Pre-op Albumin Level Difference",
        "xaxis":{"title": "SSI Status", "zeroline":False},
        "yaxis":{"title": "Albumin (g/dL)", "zeroline":False}
        }
fig1=go.Figure(data=data1, layout=layout1)
fig1.show()

## 2. SSI vs SURGICAL APPROACH:
print(df.groupby("SSI")["Approach"].describe())
#   count unique   top freq
#SSI                        
#No    162      2  Open   84
#Yes    27      2  Open   22
print(df.groupby("SSI")["Approach"].value_counts(normalize=True))

#--Chi-sq test where H0 is SSI and Surgical approach is independent.
conting_tbl=(pd.crosstab(df["SSI"],
            df["Approach"]))
chisq_stat, pval, df, exp_fre = stats.chi2_contingency(conting_tbl)
print(f'chi-sq statistic between surgical approach & SSI : {chisq_stat}')
print(f'pvalue of chi-sq test between surgical approach & SSI: {pval}')

expected_df=pd.DataFrame(
    exp_fre,
    index=conting_tbl.index,
    columns=conting_tbl.columns
)
#--Plot observed vs expected
#creating plotting axes
fig, axes = plt.subplots(1, len(conting_tbl.columns), figsize=(10, 5), sharey=True) 

for i, col in enumerate(conting_tbl.columns):
    ax = axes[i]
    observed = conting_tbl[col]
    exp = expected_df[col]
    
    ax.bar(observed.index, observed.values, alpha=0.7, label="Observed")
    ax.bar(exp.index, exp.values, alpha=0.7, label="Expected", color="orange")
    
    ax.set_title(f"{col}")
    ax.set_xlabel("SSI")
    if i == 0:
        ax.set_ylabel("Count")
    ax.legend()

plt.suptitle(f"Chi-square test between surgical approach & SSI (Chi2={chisq_stat:.2f}, p={pval:.4g})", fontsize=14)
plt.tight_layout()
plt.show()

#Chi2ContingencyResult(
# statistic=np.float64(7.090006251420779), 
# pvalue=np.float64(0.007751497682624491), 
# dof=1, expected_freq=array([[71.14285714, 90.85714286],
# [11.85714286, 15.14285714]]))

## 3. SSI vs GENDER:
df=pd.read_csv("~/Desktop/mini_project_1/RawData.csv")
print(df.groupby("SSI")["Gender"].describe())
#count unique     top freq
#SSI                          
#No    162      2  Female   95
#Yes    27      2    Male   14

#--Chi-sq test where H0 is SSI and Gender approach is independent.
conting_tbl_s=pd.crosstab(
    df["SSI"],
    df["Gender"]
)
chisq_stat1, pval1, df1, exp_fre1 = stats.chi2_contingency(conting_tbl_s)
print(f'chi-sq statistic between gender & SSI: {chisq_stat1}')
print(f'pvalue of chi-sq test between gender & SSI: {pval1}')

expected_df_gend=pd.DataFrame(
    exp_fre1,
    index=conting_tbl_s.index,
    columns=conting_tbl_s.columns
)

fig_gen, axes_gen = plt.subplots(1, len(conting_tbl_s.columns), figsize=(10, 5), sharey=True) 

for i, col in enumerate(conting_tbl_s.columns):
    ax = axes_gen[i]
    observed = conting_tbl_s[col]
    exp = expected_df_gend[col]
    
    ax.bar(observed.index, observed.values, alpha=0.7, label="Observed")
    ax.bar(exp.index, exp.values, alpha=0.7, label="Expected", color="orange")
    
    ax.set_title(f"{col}")
    ax.set_xlabel("SSI")
    if i == 0:
        ax.set_ylabel("Count")
    ax.legend()

plt.suptitle(f"Chi-square test between gender & SSI (Chi2={chisq_stat1:.2f}, p={pval1:.4g})", fontsize=14)
plt.tight_layout()
plt.show()

## 3. CRP CHANGE POST vs PRE-OP CRP in SSI and NON-SSI PATIENTS: - SIGNIFICANT
#check for normality of SSI in ctrl group to use either t-test or Man-Whitney
#--Shapiro test Ho: CRP Changes in non-SSI data is NORMAL
print(df.head)
df["CRPDelta"]=df["PostOpCRP"]-df["PreOPCRP"]
shap_statistic, shap_pval = stats.shapiro(df[df["SSI"] == "No"]["CRPDelta"])
print(f'shapiro statistic (closer to 1 means more normality):{shap_statistic}')
print(f'pval of shapiro test (smaller is not normal): {shap_pval}') 
#pval is too small, data is not normal --> Man Whitney test

#--Man Whitney to compare means:
mwu_statistic, mwu_pval = stats.mannwhitneyu(df[df["SSI"]=="No"]["CRPDelta"],
                                             df[df["SSI"]!="No"]["CRPDelta"],
                                             alternative = "two-sided")

#--violin (distribution shape, max/min)
plt.figure(figsize=(6,5))
sns.violinplot(x="SSI", y="CRPDelta", data=df, inner="box", palette="Set3")
plt.title("CRP Change distribution by SSI (Mann-Whitney U test)")
plt.show()

## 4. PreOpAlbumin IN NON-SSI VS SSI PATIENTS: - SIGNIFICANT
#check for normality of SSI to use either t-test or Man-Whitney
#--Shapiro test Ho: PreOpAlbumin data in NON-SSI is NORMAL
stat_shapiro_al, pval_al = stats.shapiro(df[df["SSI"]=="No"]["PreOpAlbumin"])
print(f'shapiro statistic (closer to 1 means more normal): {stat_shapiro_al}')
print(f'shapiro pvalue (smaller more likely derived from normal): {pval_al}')

#check for homogenous variance in 2 comparing sample groups:
#--Barlett's test (usually done before ANOVA) H0: all groups have equal variance
stat_bar, pval_bar = stats.bartlett(df[df.SSI == "No"]["PreOpAlbumin"],
                                    df[df.SSI != "No"]["PreOpAlbumin"])
print(f"barlett's test pvalue (smaller, variance less likely to be equal): {pval_bar}") 
#not normal

#--man whitney u test:
stat_mw_al, pval_mw_al = stats.mannwhitneyu(df[df.SSI == "No"]["PreOpAlbumin"],
                   df[df["SSI"] != "No"]["PreOpAlbumin"]
)

#--Welch's ttest (just in case)):
ttest_stat, pval_tt = stats.ttest_ind(df[df.SSI == "No"]["PreOpAlbumin"],
                df[df.SSI != "No"]["PreOpAlbumin"],
                equal_var = False)

#--box plot visualizing ttest:
plt.figure(figsize=(6,5))
sns.violinplot(x="SSI", y="PreOpAlbumin", data=df, inner="box", palette="Set3")
plt.title(f"Pre-op Albumin Level Across SSI Status: T-test t={ttest_stat:.2f}, pval={pval_tt:.4g}")
plt.show()

#6. PRE-OP WHITE CELL COUNTS ACROSS SSI STATUS: --NOT SIGNIFICANT
#--Shapiro test Ho: Pre-op WCC data in NON-SSI is NORMAL
shapiro_wc, pval_wc = stats.shapiro(df[df["SSI"]=="No"]["PreOpWCC"])
print(f"shapiro statistic: {shapiro_wc}")
print(f"shapiro pvalue: {pval_wc}") #normal

#--Barlett's test, with H0: all groups have equal variance:
stat_bar_wc, pval_bar_wc = stats.bartlett(df[df.SSI == "No"]["PreOpWCC"],
                                          df[df.SSI != "No"]["PreOpWCC"])
print(f"barlett's test pvalue (smaller, variance less likely to be equal): {pval_bar_wc}") 
#not equal variance

#--t-test:
tt_wc_stat, tt_wc_pval = stats.ttest_ind(df[df["SSI"] == "No"]["PreOpWCC"],
                df[df["SSI"] != "No"]["PreOpWCC"],
                equal_var=False)

#--box plot:
trace4=go.Box(y=df[df["SSI"] == "No"]["PreOpWCC"],
              marker = {"color": "darkblue"},
              name = "No SSI",
              boxpoints = "outliers")

trace5=go.Box(y=df[df["SSI"]=="Yes"].PreOpWCC,
              marker = {"color":"red"},
              name = "SSI",
              boxpoints = "outliers")

data2=[trace4, trace5]

layout2={"title" : "Pre-Op White Blood Count Across SSI Status",
         "xaxis" : {"title": "SSI Status", "zeroline" : False},
         "yaxis" : {"title": "White Blood Count (cells/µL)", "zeroline" : False}}

fig2=go.Figure(data=data2,
               layout=layout2)
fig2.show()

#--violin plot:
plt.figure(figsize=(6,5))
sns.violinplot(x="SSI", y="PreOpWCC", data=df, inner="box", palette="Set3")
plt.title(f"Pre-op White Blood Count Across SSI Status: T-test t={tt_wc_stat:.2f}, pval={tt_wc_pval:.4g}")
plt.show()

#--SUMMARY OF ALL RESULTS:
sum_proj=pd.DataFrame(
    {"Variables Tested with SSI": ["Surgical Approach", "Gender", "DeltaCRP", "Pre-Op Albumin", "PreOpWCC"],
     "Test(s) Done" : ["Chi-Square", "Chi-Square", "Shapiro/Mann Whitney U", "Shapiro/Barlett/Man Whitney U", "Shapiro/Barlett/ttest"],
     "Significant (Yes/No)":["Yes", "No?", "Yes", "Yes", "No"],
     "pvalue":[pval, pval1, mwu_pval, pval_mw_al, tt_wc_pval],
     "Graph Plotted": ["Bar", "Bar", "Violin/Boxplot", "Violin/Boxplot", "Boxplot"]
    }
)
#--Generate HTML table string
html_table = sum_proj.to_html(index=False) # index=False to hide the DataFrame index

#--Save to an HTML file
with open("published_table.html", "w") as f:
    f.write(html_table)
