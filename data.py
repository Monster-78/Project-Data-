from random import choice
from tkinter import NO, YES
from altair import to_csv
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Data Cleaning App", layout="wide")
choice = st.sidebar.selectbox("Navigation", ["Home", "Practice","Data","About"])
save_folder = "Data"
os.makedirs(save_folder, exist_ok=True)
if choice == "About":
    st.title("About")
    st.write("This app is designed to help users clean and visualize their datasets easily. Upload your data, handle missing values, and explore visualizations all in one place!")
    st.write("Developed by [Your Name].")
    st.write("Connect with me on [LinkedIn](https://www.linkedin.com) or visit my [GitHub](https://github.com).")
elif choice=="Home":
    st.title("🧹 Data Cleaning and Visualization App")
    st.write("Upload your dataset, handle missing values, and explore visualizations all in one place!")
# Upload file
    uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx", "txt"])

    if uploaded_file is not None:
        # Read file
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        st.subheader("📌 Original Data")
        st.write(df.head(5))
        st.write("📊 Summary Statistics")
        st.write(df.describe(include='all'))
        st.write("📐 Shape of Data:", df.shape)
        st.write("📄 Data Types:", df.dtypes)

        # Check for missing values
        st.write("🔍 Missing Values Count:")
        st.write(df.isna().sum())

        # User Choice
        Choice = st.radio("Do you want to clean all columns automatically?", ["Yes", "No"])

        st.subheader("🧹 Data Cleaning")
        if Choice == "Yes":
            for col in df.columns:
                if df[col].dtype in ["int64", "float64"]:   # Numeric columns
                    df[col] = df[col].fillna(df[col].mean())
                else:  # Object / Categorical columns
                    df[col] = df[col].fillna(df[col].mode()[0])
            st.success("✅ All missing values handled automatically.")

        else:
            user_col = st.selectbox("Select column to clean", df.columns)
            if df[user_col].dtype in ['int64', 'float64']:
                df[user_col] = df[user_col].fillna(df[user_col].mean())
                st.success(f"✅ Missing values in '{user_col}' filled with Mean.")
            else:
                df[user_col] = df[user_col].fillna(df[user_col].mode()[0])
                st.success(f"✅ Missing values in '{user_col}' filled with Mode.")

        # Show NaN count after cleaning
        st.subheader("📊 NaN Count after Cleaning")
        st.write(df.isna().sum())
        st.write("All missing values have been handled.")

        # Download Cleaned Data
        df_to_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Cleaned Data", df_to_csv, "cleaned_data.csv", "text/csv")

        # ---------------- VISUALIZATION PART ----------------
        # st.subheader("📈 Data Visualization")
        # st.write("🔗 Correlation Heatmap")
        # fig, ax = plt.subplots(figsize=(8,6))
        # sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        # st.pyplot(fig)


        # 1. Heatmap for missing values
        st.write("🔍 Heatmap of Missing Values (before cleaning)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(df.isna(), cbar=False, cmap="viridis", ax=ax)
        st.pyplot(fig)

        # 2. Distribution of numeric columns
        st.write("📊 Distribution of Numeric Columns")
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            col_choice = st.selectbox("Select numeric column", numeric_cols)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[col_choice], bins=20, kde=True, ax=ax, color="skyblue")
            st.pyplot(fig)

        # 3. Countplot for categorical columns
        st.write("📌 Countplot for Categorical Columns")
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            cat_choice = st.selectbox("Select categorical column", cat_cols)
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x=cat_choice, ax=ax, palette="Set2")
            plt.xticks(rotation=30)
            st.pyplot(fig)
        st.write("📈 Pairplot (sampled)")
        sampled_df = df.sample(min(200, len(df)))  # lagging avoid karega
        sns.pairplot(sampled_df[numeric_cols])
        st.pyplot()

        st.write("📦 Boxplot (Outliers)")
        num_col = st.selectbox("Select numeric column for Boxplot", numeric_cols)
        fig, ax = plt.subplots()
        sns.boxplot(x=df[num_col], ax=ax)
        st.pyplot(fig)

elif choice == "Practice":
    
    st.title("📊 Random Data Generator")

    # Session state to store data
    if "columns" not in st.session_state:
        st.session_state.columns = []
    if "data_list" not in st.session_state:
        st.session_state.data_list = []

    # Sidebar Inputs
    st.sidebar.header("Add a Column")
    col_type = st.sidebar.selectbox("Select column type", ["number", "string", "date", "boolean"])
    col_name = st.sidebar.text_input("Enter column name")
    rows = st.sidebar.number_input("Number of rows", min_value=1, value=10, step=1)

    if st.sidebar.button("Add Column"):
        if col_name == "":
            st.sidebar.warning("Please enter a column name!")
        else:
            # Generate random data
            if col_type == "number":
                data = np.random.randint(50, 501, size=rows)
            elif col_type == "date":
                start_date = np.datetime64('2020-01-01')
                end_date = np.datetime64('2023-12-31')
                data = np.random.choice(np.arange(start_date, end_date), size=rows)
            elif col_type == "boolean":
                data = np.random.choice([YES, NO], size=rows)
            else:
                data = np.random.choice(['A', 'B', 'C', 'D', 'E'], size=rows)
            
            # Store in session state
            st.session_state.columns.append(col_name)
            st.session_state.data_list.append(data)
            st.sidebar.success(f"Column '{col_name}' added!")

    # Show current DataFrame
    if st.session_state.columns:
        df = pd.DataFrame({st.session_state.columns[i]: st.session_state.data_list[i] 
                        for i in range(len(st.session_state.columns))})
        st.subheader("📄 Generated DataFrame")
        st.dataframe(df)
        # Save to CSV
   
        file_path = os.path.join(save_folder, "random_data.csv")
        df.to_csv(file_path, index=False)
        st.success(f"✅ File automatically saved at '{file_path}'")
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='random_data.csv',
            mime='text/csv'
        )

    # Reset button
    if st.sidebar.button("Reset All"):
        st.session_state.columns = []
        st.session_state.data_list = []
        st.sidebar.success("All data cleared!")
