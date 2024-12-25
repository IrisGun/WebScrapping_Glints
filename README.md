# WebScrapping_Glints
TL,DR: This project crawls info on Data Analyst jobs in Vietnam and does some EDA to understand the post-pandemic (2022) labor market for this role. 
It was first inspired by the reposistory of anhvi.

---

## **Background**
> **"Stability isn't about staying in one job for life, but rather being able to find a new one tomorrow if you quit today."**

The Covid-19 pandemic kinda messed with everyone's idea of work. Post-pandemic, the word I see quite often in the job market is 'layoff' – it's practically the new black. While I've thankfully never been on the receiving end of that particular party favor (touch wood!), I've always been a fan of proactive self-improvement and keeping my skills sharp.  
This project is my deep dive into the real-deal labor market demand, so I can transform myself into a shiny, top-shelf, highly desirable human resource. You know, the kind they most likely want to keep around or the kind who can walk away with their head held high!

---

## **Features**
- **Automated Data Crawling from Glints:** Automatically extracts data from Glints job postings related to data roles. 
- **Comprehensive Exploratory Data Analysis (EDA):** Provides in-depth exploratory analysis of the collected data, including visualizations and summary statistics. 
- **Association Rule Mining with Apriori:** Employs the Apriori algorithm to identify frequently associated skills within job descriptions.
  
---

## **How It Works**

1. **Data Crawling:** Job data is [extracted](https://github.com/IrisGun/WebScrapping_Glints/blob/main/utils/visualization.py) from Glints using Selenium and Beautiful Soup. This structured data is then stored in a DataFrame for further [processing](https://github.com/IrisGun/WebScrapping_Glints/blob/main/utils/preprocess.py).
2. **Exploratory Data Analysis (EDA):** [Interactive charts](https://github.com/IrisGun/WebScrapping_Glints/blob/main/eda.ipynb) are generated using Plotly to visualize and explore the data.[ Reusable functions](https://github.com/IrisGun/WebScrapping_Glints/blob/main/utils/visualization.py) are implemented to easily customize and generate various chart types.
3. **Skill Association Analysis:** Skills are treated as items in a market basket analysis. The Apriori algorithm is applied to discover associations between skills, providing recommendations for skill development.

---

## **How to Use Locally**
1. Clone the repository:  
   ```bash
   git clone https://github.com/IrisGun/WebScrapping_Glints.git
2. Navigate to the project directory:
   ```bash
   cd WebScrapping_Glints
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the notebook   

---

## **Technologies Used**

**Data Acquisition:**
- **Selenium:** Web browser automation.
- **Beautiful Soup:** HTML parsing.

**Data Processing and Analysis:**
- **Python:** Core programming language.
- **Pandas:** Data manipulation and analysis.
- **Apriori Algorithm (from `mlxtend` or similar library):** Association rule mining.

**Data Visualization:**
- **Plotly:** Interactive charting.
- **HTML (Optional):** Embedding charts in web pages.

---

## **Some takeaway insights**
### **1. Univariate charts**  
#### **1.1. Data job count by Category**  
Based on the job count chart from Glints in Vietnam, Data Science exhibits the highest demand, followed by Software Engineering. Other fields like Engineering, Marketing, and Finance have significantly fewer job postings compared to these two leading areas, indicating a strong focus on tech-related positions on the platform.  Notably, employers tend to categorize various data-related roles under the broad umbrella of _"Data Science"_ rather than posting and selecting for specific business domains.

<img src="charts\capture\jobcount_bycategory.png" alt="chart_job_bycategory">  


#### **1.2. Data job count by Location**  
Job opportunities are heavily concentrated in Ho Chi Minh City, which has a substantially larger volume of postings compared to Hanoi, while Ha Nam and Da Nang have minimal job postings represented in this data. This indicates a significant regional disparity in job availability. Therefore, candidates in major metropolitan areas can effectively utilize this platform, while those targeting more niche markets or seeking opportunities in other regions should consider alternative job search strategies.

<!-- <img src="charts\capture\jobdistribution_location.png" alt="chart_job_bylocation" width="60%">   -->
<img src="charts\capture\jobdistribution_location.png" alt="chart_job_bylocation">  


#### **1.3. Salary distribution**  
Software Engineering and Data Science offer the most competitive salaries among the specific categories, with Data Science showing potential for higher earnings due to some outliers. Engineering roles have a more modest and consistent pay range, while Marketing, Administrative, Finance, and Business Development/Sales generally offer lower salaries with less variability.  
The presence of high-end outliers in Data Science implies that achieving significant experience and expertise in this field can lead to substantial financial rewards, making it a promising career path for those seeking high earning potential.

<img src="charts\capture\salarydistribution_bycategory.png" alt="chart_salarydistribution">  


#### **1.4. Top required skills**  
Among the top 5 required skills among data analysis, data science, programming, database, there is a requirement for English proficiency, demonstrating that in addition to technical skills, candidates need communication skills, especially communication in an international environment.  
Python is still the star! Tableau and PowerBI are most popular tool for data visualization.  

<img src="charts\capture\toprequiredskills.png" alt="chart_topskills">  


#### **1.5. Experience requirement**  
Job opportunities are most abundant for candidates with 1-3 years of experience, indicating a strong demand for early-career professionals. While entry-level and mid-level roles are available, senior-level positions are comparatively scarce. Senior-level candidates should probably explore other resources to find data-related jobs rather than this mass channel.  

<img src="charts\capture\experiencerequirement.png" alt="chart_experience">  


### **2. Comparative charts**   
#### **2.1. Segment by location**  
<img src="charts\capture\seg_location.png" alt="chart_seglocation">  

- _Salary:_ 
   Ho Chi Minh generally has a higher median salary compared to Hanoi across all experience levels.  
   The range of salaries in Ho Chi Minh City also tends to be wider, suggesting geater potential higher earnings for potential candidates.  
- _Experience Requirements:_  
   Job postings in both cities show a strong preference for candidates with 1-3 years of experience.  
   Entry-level candidate are more well-accepted in Hanoi than Ho Chi Minh city.  
- _Skill requiremtns:_  
   Data Analysis, SQL, and Python are consistently among the most in-demand skills in both locations.
   The specific skill requirements might slightly between cities but the overall emphasis on tenchnical skills remain consistent.
   Besides Data Analysis, Data Science, and coding skills, Data jobs in Hanoi show the preference in BI tool while Ho Chi Minh city lean toward database a little bit.  

- **_Overall:_** Ho Chi Minh city presents a more competitive job market with higher earning potential. At this specific timeline (Nov 2022). Data Analysis and Data Science as core skills, Python and SQL as technical skills should be sharpen. Focus on Database for candidates who want to target Ho Chi Minh city and BI tool for counterpart in Hanoi.   

#### **2.2. Segment by experience**  


---
## **Suggestions for Improvement**  

This project provides a foundation for analyzing job market data from Glints. Due to my current limitations (mostly involving the space-time continuum and a distinct lack of superpowers), I haven't quite gotten around to these enhancements yet:

- **Data Source Expansion:** Conquer the data from other job boards or platforms to broaden the analysis.
- **Enhanced Data Cleaning and Preprocessing:** Implement more robust data cleaning and preprocessing techniques to handle inconsistencies and missing values.
- **Advanced Analysis Techniques:** Go beyond Apriori and unlock the secrets of the data universe with fancy models such as:
    - **Salary Prediction:** Develop a model to predict salaries based on job title, skills, experience, and location. This could use regression algorithms like Linear Regression, Random Forest Regressor, or Gradient Boosting Regressor.
    - **Job Clustering:** Group similar jobs together based on their descriptions, skills, and industry. This could use clustering algorithms like K-Means or DBSCAN.
    - **Job Categorization:** Classify jobs into predefined categories (e.g., Data Scientist, Data Engineer, Data Analyst). This could use classification algorithms like Naive Bayes, Support Vector Machines (SVM), or Random Forest Classifier.
    - **Recruitment Trend Analysis:** Analyze how job postings and required skills change over time to identify emerging trends in the job market. This could involve time series analysis or analyzing changes in word frequencies over time.
- **Web Application Development:** Develop a web application to host the analysis results and provide an interactive user interface.
- **Automated Updates:** Implement a scheduled task to automatically update the data, ensuring the analysis reflects the latest job market trends (Because who has time to manually update things? Not me, that's for sure!).

---

## **Contributing**
Contributions are welcome! Feel free to fork the repo, submit pull requests, or open issues for suggestions, bug reports, or connect with me via [LinkedIn](https://www.linkedin.com/in/trang-nguyen-45374b102/).
