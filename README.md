## 1. File Structures
```
├───assets
│   └───relations.png
├───data
│   ├───olist_all_data.csv
│   ├───olist_customers_dataset.csv
│   ├───olist_geolocation_dataset.csv
│   ├───olist_order_items_dataset.csv
│   ├───olist_order_payments_dataset.csv
│   ├───olist_order_reviews_dataset.csv
│   ├───olist_orders_dataset.csv
│   ├───olist_products_dataset.csv
│   ├───olist_sellers_dataset.csv
│   └───product_category_name_translation.csv
├───dashboard_util.py
├───dashboard.py
├───notebook.ipynb
├───Proyek_Analisis_Data.ipynb
├───README.md
├───requirements.txt
└───url.txt

```
## 2. Project Workflow  
1. **Library Preparation**  
   - Install and import necessary libraries for data analysis and visualization.  

2. **Data Wrangling**  
   - **Data Collection**: Gather raw data from various sources.  
   - **Data Assessment**: Evaluate data quality, detect missing values, and identify inconsistencies.  
   - **Data Cleaning**: Handle missing values, correct inconsistencies, and preprocess data for analysis.  

3. **Exploratory Data Analysis (EDA) & Clustering Analysis**  
   - Define key business questions to guide the analysis.  
   - Perform clustering to segment data based on relevant business characteristics.  

4. **Data Visualization**  
   - Develop visual representations to effectively communicate insights derived from the analysis.  

5. **Conclusion**  
   - Summarize findings and provide answers to the defined business questions.  

6. **Dashboard Development**  
   - Structure the DataFrame for dashboard integration.  
   - Implement filter components for better interactivity.  
   - Enhance the dashboard with various visual elements to present insights clearly.  

## 3. Getting Started  

### Running `notebook.ipynb`  
1. Download this project.  
2. Install required libraries using the command:  
   ```sh
   pip install -r requirements.txt
   ```
3. Open your preferred development environment, such as Jupyter Notebook or Google Colaboratory.  
   - **For Jupyter Lab:**  
     - Open a terminal and navigate to the project directory.  
     - Example: `cd D:/path/to/your/project`  
     - Run the command: `jupyter lab .`  
   - **For Google Colaboratory:**  
     - Create a new notebook.  
     - Upload and select the `.ipynb` file.  
     - Connect to a hosted runtime.  
     - Execute the code cells sequentially.  

### Running `dashboard.py`  
1. Download this project.  
2. Install Streamlit using the command:  
   ```sh
   pip install streamlit
    ```
3. Ensure that required libraries such as pandas, numpy, scipy, matplotlib, and seaborn are installed.
4. Keep the CSV files in the same directory as `dashboard.py`, as they serve as the data source.
5. Open VS Code, access the terminal, and run the dashboard with: 
   ```sh
   streamlit run dashboard.py
   ```

