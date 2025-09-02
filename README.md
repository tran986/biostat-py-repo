#    Patient Data Analysis and Visualization

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![Pandas](https://img.shields.io/badge/Library-Pandas-yellow.svg)
![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-green.svg)
![SciPy](https://img.shields.io/badge/Library-SciPy-orange.svg)
![Seaborn](https://img.shields.io/badge/Visualization-Seaborn-teal.svg)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple.svg)
![NumPy](https://img.shields.io/badge/Library-NumPy-orange.svg)

##    Description:
A biostatistics project analyzing patient data with Skin and soft tissue infection (SSI) using Python, with the overall aim to understand how SSI is related to factors, such as genders, surgical approaches, or c-reative proteins, etc... (specific questions can be found below).
The project demonstrates data preprocessing, statistical analysis, and visualization methods for biomedical research. 
Raw data for data reproducibility can be found in the project directory

##    Research Questions:
 1. Descriptive statistics
 2. Is the presence of SSI independent (or dependent) from surgical approach?
 3. Is the presence of SSI independent (or dependent) from gender?
 4. Is there a significant difference in the rise of CRP (before and after surgery) b/w patients with and without SSI
 5. Is there a significant difference in pre-operative albumin level (PreOpAlbumin) b/w patients with and without SSI
 6. Is there a significant difference in pre-operative white cell counts b/w patients with and without SSI

##    Figures:
A. Surgical approach:

<img width="995" height="496" alt="Screenshot 2025-09-01 at 7 52 38 PM" src="https://github.com/user-attachments/assets/f7e3ed02-a459-4cfd-a801-e024ad9dcfd3" />

B. Gender:

<img width="989" height="494" alt="Screenshot 2025-09-01 at 7 52 51 PM" src="https://github.com/user-attachments/assets/5033a9c6-542f-4cfb-a0c4-d0c35d5aedcd" />

C. CPR level:

<img width="1373" height="774" alt="Screenshot 2025-09-01 at 7 53 39 PM" src="https://github.com/user-attachments/assets/968c6964-2ff6-4df6-a08b-62d8d6c921b2" />
<img width="588" height="491" alt="Screenshot 2025-09-01 at 7 53 00 PM" src="https://github.com/user-attachments/assets/7926be1c-cb7d-4fac-a4fe-8c6594f93e01" />

D. Pre-op albumin level:

<img width="591" height="491" alt="Screenshot 2025-09-01 at 7 54 00 PM" src="https://github.com/user-attachments/assets/aed4cb44-48c6-4521-b459-7d6d1243ec74" />
<img width="1386" height="778" alt="Screenshot 2025-09-01 at 7 53 19 PM" src="https://github.com/user-attachments/assets/46d3865b-d512-44f6-884b-70003c46a2c4" />

E. White blood cell count:

<img width="1376" height="773" alt="Screenshot 2025-09-01 at 7 54 20 PM" src="https://github.com/user-attachments/assets/b10690d9-d325-44f1-8e92-f72b6a8201e0" />

##  Summarized results:

| Variables Tested with SSI | Test(s) Done | Significant (Yes/No) | pvalue | Graph |
|---|---|---|---|---|
| Surgical Approach | Chi-Square | Yes | 7.751498e-03 | Bar |
| Gender | Chi-Square | No | 4.178870e-01 | Bar |
| DeltaCRP | Shapiro/Mann Whitney U | Yes | 7.976901e-07 | Violin/Boxplot |
| Pre-Op Albumin | Shapiro/Barlett/Man Whitney U | Yes | 3.099776e-01 | Violin/Boxplot |
| PreOpWCC | Shapiro/Barlett/ttest | No | 4.815974e-01 | Boxplot |

*P-values for "Pre-op Albumin" and "Pre-op White cell count" (PreOpWCC) are determined from Mann Whitney U test. All significance tests use alpha level of 0.05.

##  Contribution/Citation:
Raw Data provided by Dr. Juan Klopper (Department of Biostatistics and Bioinformatics) from Milken Institute School of Public Health, The George Washington University Washington D.C.

