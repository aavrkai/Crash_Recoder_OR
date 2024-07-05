import streamlit as st
import pandas as pd
from io import StringIO

def concatenate_files(uploaded_files, format_file):
    if format_file == 'txt':
        content = ""
        for uploaded_file in uploaded_files:
            content += uploaded_file.getvalue().decode("utf-8").strip() + "\n"
        content = content.strip()
        lines = content.splitlines()
        data = [line.split(',') for line in lines]
        concatenated_df = pd.DataFrame(data)
    elif format_file == 'csv':
        dfs = []
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file)
            dfs.append(df)
        concatenated_df = pd.concat(dfs, ignore_index=True)
    else:
        raise ValueError("Unsupported file format. Please select either 'txt' or 'csv'.")
    return concatenated_df

def main():
    st.title("File Concatenator")

    format_file = st.selectbox("Select the file format", ['txt', 'csv'])
    uploaded_files = st.file_uploader(f"Upload {format_file} files", accept_multiple_files=True, type=[format_file])

    if uploaded_files:
        concatenated_df = concatenate_files(uploaded_files, format_file)
        
        # Remove completely empty rows
        concatenated_df.dropna(how='all', inplace=True)
        
        st.write("Concatenated Content:")
        st.write(concatenated_df)
        
        csv = concatenated_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download concatenated content as CSV",
            data=csv,
            file_name='concatenated_content.csv',
            mime='text/csv',
        )
    uploaded_files = st.file_uploader(f"Upload Dictionary file", type=['xlsx'])

    if uploaded_files:
        df_translation = pd.read_excel(uploaded_files)
        temp = df_translation.drop(columns='Values')  # droping the values column
        cols = temp.columns.tolist()

        concatenated_df.columns = cols    
        st.write(concatenated_df.columns)

if __name__ == "__main__":
    main()
