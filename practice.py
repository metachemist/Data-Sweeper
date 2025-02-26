import pandas as pd
import streamlit as st
import os
from io import BytesIO
from openpyxl.workbook import Workbook


# Set up our App
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Advanced Data Sweeper")
st.write ("Transform your files between CSV and Excel formats with built-in data cleaning and visualization tools.")


# File uploader widget that accepts CSV and Excel files
# 'accept_multiple_files=True' allows batch uploading multiple files at once
uploaded_files = st.file_uploader("Upload Your Files (CSV or Excel): ", type=['csv', 'xlsx'], accept_multiple_files = True)

# Processing logic for uploaded files (if any files are uploaded)
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Invalid File Format. Please upload a CSV or Excel file.")
            continue

        # Display info about the file
        st.write(f"**📄 File Name**: {file.name}")
        st.write(f"**📏 File Size**: {file.size/1024}")

        # Preview the first 5 rows of the uploaded file
        st.write("**🔍 Preview the Head of the Dataframe**")
        st.write(df.head())

        # Options for the data cleaning 
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                # Button to remove duplicate rows from the DataFrame
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed Successfully")
            with col2:
                # Button to fill missing numeric values with column means
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled Successfully")

        # Choose Specific Columns to convert
        st.subheader("🎯 Select Columns Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Visualization Chart
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart        

        # Convert the file 
        st.subheader("🔄️ Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO() # Create in-memory buffer to store the converted file
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.split(".")[0] + ".csv"
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.split(".")[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download the file
            st.download_button(
                label=f"⬇️ Download {file.name} to {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )    
st.success("Thank you for using Data Sweeper!")
