import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os

class FrictionTestPlotter:
    def __init__(self):
        self.data_frames = []
        self.file_names = []

    def load_txt_files(self, uploaded_files):
        
        for uploaded_file in uploaded_files:
            try:
                # Assuming the text file is tab-delimited; modify sep if necessary
                df = pd.read_csv(uploaded_file, sep=None, header=None, engine='python')
                if df.shape[1] != 2:
                    raise ValueError(f"File {uploaded_file.name} doesn't have exactly 2 columns.")
                df.columns = ['Encoder Position', 'Current']  # Assign column names
                self.data_frames.append(df)
                self.file_names.append(uploaded_file.name)  # Save the file name for legend
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")

    def normalize_encoder_position(self, df):
        
        max_value = df['Encoder Position'].max()
        df['Encoder Position'] = df['Encoder Position'] * (360 / max_value)
        return df

    def plot_data(self, width, height):
        
        if not self.data_frames:
            st.warning("No data available to plot. Please upload files.")
            return


        fig, ax = plt.subplots(figsize=(width, height))
        for df, file_name in zip(self.data_frames, self.file_names):
            df = self.normalize_encoder_position(df)
            ax.plot(df['Encoder Position'], df['Current'], label=file_name)

        # Calculate a scaling factor based on the plot's width and height
        scaling_factor = (width + height) / 2

        # dynamic sizing for the labels
        ax.set_title("Friction Test", fontsize=scaling_factor * 1.2)
    
        ax.set_xlabel("Encoder Position in Degrees", fontsize=scaling_factor * 1.2)
        ax.set_ylabel("Current ", fontsize=scaling_factor * 1.2)
        ax.tick_params(axis='both', labelsize=scaling_factor * 1.1)

        ax.set_xlabel("Encoder Position in Degrees")
        ax.set_ylabel("Current")
        plt.xticks(np.arange(0, 361, 20))  # x axis increments of 20 degrees
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=scaling_factor*1.2)
        ax.grid(True)
        st.pyplot(fig)
        

# Streamlit UI
def main():
    st.title("Friction Test Plotter")
    st.markdown("Upload file")

    uploaded_files = st.file_uploader(
        "Upload TXT Files", 
        type=["txt"], 
        accept_multiple_files=True
    )

    st.sidebar.header("Graph Settings")
    width = st.sidebar.slider("Graph Width", 5, 70, 5)
    height = st.sidebar.slider("Graph Height", 5, 30, 5)

    if st.button("Process and Plot Data") and uploaded_files:
        plotter = FrictionTestPlotter()
        plotter.load_txt_files(uploaded_files)
        plotter.plot_data(width, height)

if __name__ == "__main__":
    main()


