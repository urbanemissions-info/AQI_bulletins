from scipy.stats import bootstrap
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd
import random 

bhubaneshwar = [112, 87]
chandigarh = [124, 130, 143]
nagpur = [92, 107, 103, 78]
lucknow = [96, 67, 88, 71, 80, 54]
hyd = [158, 100, 81, 75, 62, 82, 115, 97, 89 ]
bengaluru = [133, 131, 82, 84, 107, 70, 106, 141, 50]
mumbai = [107, 102, 179, 165, 87, 76, 74, 164, 99, 122, 122, 132, 144, 97, 115, 91, 250, 36, 72, 168, 101, 237, 99, 93, 95]

ci_lows = []
ci_highs = []
means = []
samplesizes = []
sems = []
ts = []
#for i in [3,4,7,10,13,17,20, 25]:
#    city = random.sample(mumbai, i)
  
for city in [bhubaneshwar, chandigarh, nagpur, lucknow, bengaluru, mumbai]:
    samplesizes.append(len(city))  
    #create 95% confidence interval for population mean weight
    #ci = st.t.interval(confidence=0.95, df=len(city)-1, loc=np.mean(city), scale=st.sem(city))
    city = (city,)
    bootstraped = bootstrap(city, np.mean, confidence_level=0.95,
                         random_state=111, method='percentile')
    ci = bootstraped.confidence_interval


    ci_lows.append(ci[0])
    ci_highs.append(ci[1])
    means.append(np.mean(city))
    
    #sems.append(st.sem(city))
    ts.append(st.t.ppf(q=1-.05/2,df=len(city)-1))


df = pd.DataFrame([ci_lows, ci_highs, means,sems, samplesizes, ts]).T
df.columns = ['ci_low', 'ci_high', 'mean', 'sem', 'samplesize', 't-stat']
print(df)

plt.figure(figsize=(10, 10))
plt.errorbar(df['samplesize'], df['mean'], yerr=[df['mean'] - df['ci_low'], df['ci_high'] - df['mean']],
             fmt='o', capsize=5, markersize=7, label='CI')
plt.xlabel('Number of monitors')
plt.ylabel('AQI')
plt.title('Confidence Interval for Each Sample Size')
plt.grid(True)
plt.axhline(y=50, color='#00b050', linestyle='--', 
            #label=f'Population mean: {column.mean()}'
            )
plt.axhline(y=100, color='#669900', linestyle='--')
plt.axhline(y=200, color='#f2f542', linestyle='--')
plt.axhline(y=300, color='#f59042', linestyle='--')
plt.axhline(y=400, color='#ff0000', linestyle='--')
plt.axhline(y=500, color='#753b3b', linestyle='--')

tick_labels = ['Bhubaneshwar(2)', 'Chandigarh(3)', 'Nagpur(4)', 'Lucknow(6)', 'Bengaluru(9)', 'Mumbai(25)']
plt.xticks(df['samplesize'],
 #          tick_labels, rotation=45
           )
plt.legend()
plt.show()

exit()
data = (data,)
#calculate 95% bootstrap for mean
bootstraped = bootstrap(data, np.mean, confidence_level=0.95,
                         random_state=111, method='percentile')

print(bootstraped.confidence_interval)