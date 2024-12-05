import streamlit as st
import os
import pandas as pd
from AdvancedVisulizationMethods import displaySample, convertIntoDF, plotChart, generate_bar_chart, generate_histogram, generate_pie_chart



# Global Flags 
isFileUploaded = False
sampled_data = None




# Functions -----------------------------------------------------------------

# Helper function to generate the plot based on the type of chart
def generate_plot(df, chart_type, **kwargs):
    """
    This function generates the plot based on the type of chart passed.
    """
    if chart_type == "scatter":
        return plotChart(df, **kwargs, chartType="scatter")
    elif chart_type == "line":
        return plotChart(df, **kwargs, chartType="line")
    elif chart_type == "bar":
        return generate_bar_chart(df, category_col=kwargs.get("category_col"))
    elif chart_type == "histogram":
        return generate_histogram(df, column=kwargs.get("column"))
    elif chart_type == "pie":
        return generate_pie_chart(df, category_col=kwargs.get("category_col"))
    return None


# Functions -----------------------------------------------------------------






# Create a folder to save the uploaded file
upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)



st.title("Task 1 - Advanced Data Visualization with Matplotlib")
st.markdown("""
- Upload any csv, xlx, or xlsx
- Click on button to visulize 
- Visulize different kind of Charts and Plots
- Option to enable data points for scatter and line
- Option to enable statistical Overlays 
""")

st.divider()


# Step 1 - Take File
uploaded_dataset = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xls', 'xlsx'])

if uploaded_dataset is not None:
    st.write(f'File uploaded: {uploaded_dataset.name}')

    # Step 1.1 Save file in upload folder
    file_path = os.path.join(upload_folder, uploaded_dataset.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_dataset.getbuffer())



    # Step 1.2 -> Convert file in DF
    df = convertIntoDF(file=file_path)


    if df is not None:
        # Create two columns: one for the input and one for the button
        inputCol, buttonCol = st.columns([2,1])

        with inputCol:
            rows = st.number_input("Enter number of sample rows", min_value=1, max_value=40, step=1)

        with buttonCol:
            # Step 1.2 Button to Display Dataframe
            if st.button("Sample") and rows:
                sampled_data = displaySample(df=df, rows=rows)
                

        if sampled_data is not None: 
            st.dataframe(sampled_data)


        st.divider()

        st.write("## Advanced Data Visualizations")
        st.write("### Scatter | Line | Bar | Hostogram | Pie")

        # Dropdowns for selecting columns
        # To Filter int and flot columns 
        int_columns = df.select_dtypes(include=['int64', 'float64']).columns
        categorial_columns = df.select_dtypes(include=['object', 'category']).columns

        col_1, col_2, col_3 = st.columns([1,1,1])
        
        with col_1:
            x_col_user = st.selectbox("Select X-Axis Column (Only Numerical)", int_columns)
        
        with col_2:
            y_col_user = st.selectbox("Select Y-Axis Column (Only Numerical)", int_columns)
        
        with col_3:
            group_col = st.selectbox("Select grouping column (optional):", ["None"] + list(categorial_columns))



        # Marker size and color options
        marker_col, color_col, data_point_col = st.columns([4, 1, 1])

        with marker_col:
            # Pick a marker size
            marker_size = st.slider("Select Marker Size", min_value=5, max_value=100, value=10)

        
        with color_col:
            color = st.color_picker("Pick a color", "#1f77b4")

        with data_point_col:
            isDataPointOne = st.checkbox("Data Point:", False)
            isStatisticalOverlays = st.checkbox("Statistical Overlays:", False)






    # Streamlit UI layout
    scatter_col, line_col, bar_col, histogram_col, pie_col = st.columns([1, 1, 1, 1, 1])

    plot = None  # Variable to store the plot object

    # Generate scatter plot
    with scatter_col:
        if st.button("Generate Scatter Plot"):
            plot = generate_plot(df, chart_type="scatter", x=x_col_user, y=y_col_user, group=group_col, color=color, marker=marker_size, isDataPointOne=isDataPointOne, isStatisticalOverlays=isStatisticalOverlays)

    # Generate line plot
    with line_col:
        if st.button("Generate Line Plot"):
            plot = generate_plot(df, chart_type="line", x=x_col_user, y=y_col_user, group=group_col, color=color, marker=marker_size, isDataPointOne=isDataPointOne, isStatisticalOverlays=isStatisticalOverlays)

    # Generate bar chart
    with bar_col:
        if st.button("Generate Bar Chart"):
            plot = generate_plot(df, chart_type="bar", category_col=group_col,isDataPointOne=isDataPointOne)

    # Generate histogram
    with histogram_col:
        if st.button("Generate Histogram"):
            plot = generate_plot(df, chart_type="histogram", column=group_col, bins=10, isDataPointOne=isDataPointOne)

    # Generate pie chart
    with pie_col:
        if st.button("Generate Pie Chart"):
            plot = generate_plot(df, chart_type="pie", category_col=group_col, isDataPointOne=isDataPointOne)

    # Display the generated plot
    if plot:
        try:
            st.pyplot(plot)  # Only call st.pyplot once with the correct plot object
        except Exception as e:
            st.error(f"Error displaying plot: {e}")
            

    st.divider()


    




