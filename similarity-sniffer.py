import openpyxl
import streamlit as st
import pandas as pd
from difflib import SequenceMatcher
global df

# Header
st.header("Similarity Sniffer V1.0")

# Markdown
st.markdown("by Emran Bahadur")

# Subheader
st.subheader("This app allows you to upload an excel file,iterate through each row comparing the PLP Copy and calculating a % similarity score.")

# get the upload file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    # read the excel file
    df = pd.read_excel(uploaded_file)
    
    st.write(df)

# Create a new dataframe to store the results
results_df = pd.DataFrame(columns=['URL', 'PLP Copy', 'Similarity'])

# Iterate through each row and compare the PLP Copy
for index, row in df.iterrows():
    url1 = row['URL']
    plp1 = row['PLP Copy']
    for index2, row2 in df.iterrows():
        url2 = row2['URL']
        plp2 = row2['PLP Copy']
        # Check that the URLs are not the same
        if url1 != url2:
            # Calculate the similarity between two PLP Copy
            ratio = SequenceMatcher(None, plp1, plp2).ratio()
            # Append the results to the results dataframe
            results_df = results_df.append({'URL 1': url1, 'URL 2': url2, 'Similarity': ratio*100}, ignore_index=True)

# Sort the results by Similarity in ascending order
results_df = results_df.sort_values('Similarity', ascending=True)

# Ask user to set a similarity score to filter against
st.title("Set a similarity score to filter against")
similarity_threshold = st.number_input("Please enter a similarity score to filter against:", min_value = 0, max_value = 100, value = 0)

#Filter the results to only include matches with a similarity above the user set threshold
filtered_results = results_df[results_df['Similarity'] >= similarity_threshold]

# Save the filtered results to a CSV file
file_data = filtered_results.to_csv(index=False)

# Create a download link for the CSV file
download_button = st.download_button(
    label="Download CSV File",
    data=file_data,
    file_name="Similarity_Sniffer.csv",
    mime="text/csv",
)

if download_button:
    st.success('File downloaded to local storage')
    st.balloons()
