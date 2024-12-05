import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Functions -----------------------------------------------------------------

def convertIntoDF(file):
    """
    Converts uploaded file into DataFrame based on file type (CSV, XLSX, or XLS).
    """
    try:
        if file.endswith('.csv'):
            return pd.read_csv(file)

        elif file.endswith(('xls', 'xlsx')):
            # Handle Excel files
            engine = 'openpyxl' if file.endswith('.xlsx') else 'xlrd'
            return pd.read_excel(file, engine=engine)

        else:
            st.error("Unsupported file type")
            return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


def displaySample(df, rows):
    """
    Display a random sample of 'rows' number of rows from the DataFrame.
    """
    return df.sample(rows)


# Scatter plot with Matplotlib

def plotChart(df, **kwargs):
    """
    General function for creating scatter and line plots based on input parameters.
    """
    x = kwargs.get("x")
    y = kwargs.get("y")
    group = kwargs.get("group")
    marker_size = kwargs.get("marker", 20)
    color = kwargs.get("color", "#1f77b4")
    chartType = kwargs.get('chartType')
    isDataPointOne = kwargs.get('isDataPointOne')
    isStatisticalOverlays = kwargs.get('isStatisticalOverlays')

    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axes object
    
    if group != "None":
        # Plot grouped data (scatter/line)
        for grp in df[group].unique():
            subset = df[df[group] == grp]

            # Annotate each point with its coordinates
            if isDataPointOne:
                for i in range(len(df)):
                    ax.annotate(f"({df[x][i]}, {df[y][i]})", 
                                (df[x][i], df[y][i]), 
                                textcoords="offset points",  # Adjusts label position
                                xytext=(0, 10),  # Position the text slightly above the point
                                ha='center',  # Horizontal alignment of the text
                                fontsize=8)
                        

            if isStatisticalOverlays:
                # Fit line using polyfit
                p = np.polyfit(df[x], df[y], 1)  # p is the slope and intercept of the line
                ax.plot(df[x], np.polyval(p, df[x]), color='red', label='Regression Line')
        

            if chartType == "scatter":                
                ax.scatter(subset[x], subset[y], label=grp, s=marker_size, marker='v')
                
            elif chartType == "line":
                ax.plot(subset[x], subset[y], marker='o', markersize=marker_size, label=grp)
        ax.legend()
    else:

        if isDataPointOne:
                # Annotate each point with its coordinates
                for i in range(len(df)):
                    ax.annotate(f"({df[x][i]}, {df[y][i]})", 
                                (df[x][i], df[y][i]), 
                                textcoords="offset points",  # Adjusts label position
                                xytext=(0, 10),  # Position the text slightly above the point
                                ha='center',  # Horizontal alignment of the text
                                fontsize=8)
                    

        if isStatisticalOverlays:
            # Fit line using polyfit
            p = np.polyfit(df[x], df[y], 1)  # p is the slope and intercept of the line
            ax.plot(df[x], np.polyval(p, df[x]), color='red', label='Regression Line')
    
        # Plot non-grouped data (scatter/line)
        if chartType == "scatter":
            ax.scatter(df[x], df[y], s=marker_size, color=color)
        elif chartType == "line":
            ax.plot(df[x], df[y], markersize=marker_size, color=color)

    ax.set_title(f"{x} vs {y}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    return fig


def generate_bar_chart(df, category_col):
    """
    Generate a bar chart of the 'category_col' column.
    """
    
    if category_col is None:
        st.error("Please select a grouping column")
        return None

    try:
        count_data = df[category_col].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(count_data.index, count_data.values)

        
        # Annotate each bar with its height (value)
        for i, value in enumerate(count_data.values):
            ax.text(i, value + 0.2, str(value), ha='center', fontsize=10, color='black')  # Add value on top of the bars

        
        ax.set_title(f'Bar Chart of {category_col}')
        ax.set_xlabel(category_col)
        ax.set_ylabel('Count')
        
        return fig
    except Exception as e:
        st.error("Please select a grouping column")
        st.error(f"Error: {e}")
        return None


def generate_histogram(df, column, bins=10):
    """
    Generate a histogram for the specified column.
    """

    if column is None:
        st.error("Please select a grouping column")
        return None
    
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        # Create histogram
        counts, edges, patches = ax.hist(df[column], bins=bins, color='skyblue', edgecolor='black')  
        
        # Annotate each bar (bin) with its count
        for i in range(len(counts)):
            # Get the position of the label (center of the bin)
            x_pos = (edges[i] + edges[i+1]) / 2
            # Annotate the count on top of the bar
            plt.text(x_pos, counts[i] + 0.2, str(int(counts[i])), ha='center', fontsize=10, color='black')
        

        ax.set_title(f'Distribution of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')

        return fig
    except Exception as e:
        st.error("Please select a grouping column")
        st.error(f"Error: {e}")

def generate_pie_chart(df, category_col):
    """
    Generate a pie chart based on the 'category_col'.
    """
    if category_col is None:
        st.error("Please select a grouping column")
        return None

    try:
        count_data = df[category_col].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(count_data.values, labels=count_data.index, autopct='%1.1f%%', startangle=90)

        ax.set_title(f'Distribution of {category_col}')
        
        return fig
    except Exception as e:
        st.error("Please select a grouping column")
        st.error(f"Error: {e}")
        return None
