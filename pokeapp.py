import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

@st.cache_data
def pokedata():
    poke_df = pd.read_csv("/STAT 386/pokemon-blogpost-code/pokemondata.csv")
    return poke_df

poke_data = pokedata()

st.title("Visualizing Pokemon Data")

regions = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova']
selected_regions = st.sidebar.multiselect(
    "Select Regions", options=regions, default=regions)
regional_poke_data = poke_data[poke_data['region'].isin(selected_regions)]

regional_poke_data_exploded = regional_poke_data.explode('types')
type_counts = regional_poke_data_exploded['types'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']

type_colors = {
    'normal': '#A8A878',
    'fire': '#F08030',
    'water': '#6890F0',
    'electric': '#F8D030',
    'grass': '#78C850',
    'ice': '#98D8D8',
    'fighting': '#C03028',
    'poison': '#A040A0',
    'ground': '#E0C068',
    'flying': '#A890F0',
    'psychic': '#F85888',
    'bug': '#A8B820',
    'rock': '#B8A038',
    'ghost': '#705898',
    'dark': '#705848',
    'dragon': '#7038F8',
    'steel': '#B8B8D0',
    'fairy': '#EE99AC'
}

# Tabs

tab1, tab2, tab3, tab4 = st.tabs(['Type', 'Height', 'Weight', 'Height vs Weight'])

with tab1:
    st.header("Pokémon Type Counts by Region")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filter Pokémon Types")
        selected_types = st.multiselect(
            "Select types to display:", 
            options=type_counts['Type'].tolist(),
            default=type_counts['Type'].tolist()
        )
    
    with col2:
        filtered_counts = type_counts[type_counts['Type'].isin(selected_types)]

        fig, ax = plt.subplots(figsize=(12, 6))
        bar_colors = [type_colors[t] for t in filtered_counts['Type']]
        bars = ax.bar(filtered_counts['Type'], filtered_counts['Count'], color=bar_colors)
        ax.set_title('Type Counts', fontsize=16)
        ax.set_xlabel('Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3, f'{int(height)}', 
                    ha='center', va='bottom', fontsize=10, color='black')

        st.pyplot(fig)

        with st.expander("See explanation"):
            st.write("""
                I know the colors are a little crazy with this one, but I chose to make the hex values
                of each bar match the hex values of each type from the games! Thought it would be a nice
                detail to help the viewers more familiar with pokemon to be able to quickly tell which
                bar is which type.
                    """)
        

with tab2:
    st.header("Pokémon Heights")

    stat_select = st.selectbox(
        "Select height statistic", options=["Min", "Mean", "Max"], index=0)

    if stat_select == "Mean":
        height_stat_by_region = regional_poke_data.groupby('region')['height'].mean().reset_index()
    elif stat_select == "Min":
        height_stat_by_region = regional_poke_data.groupby('region')['height'].min().reset_index()
    else:
        height_stat_by_region = regional_poke_data.groupby('region')['height'].max().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(height_stat_by_region['region'], height_stat_by_region['height'], color='indigo')
    ax.set_title('Pokémon Height by Region', fontsize=16)
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Height (m)', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.005, f'{height:.3f}', 
                ha='center', va='bottom', fontsize=10, color='black')

    st.pyplot(fig)


with tab3:
    st.header("Pokémon Weights")

    stat_select = st.selectbox(
        "Select weight statistic", options=["Min", "Mean", "Max"], index=0)

    if stat_select == "Mean":
        weight_stat_by_region = regional_poke_data.groupby('region')['weight'].mean().reset_index()
    elif stat_select == "Min":
        weight_stat_by_region = regional_poke_data.groupby('region')['weight'].min().reset_index()
    else:
        weight_stat_by_region = regional_poke_data.groupby('region')['weight'].max().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(weight_stat_by_region['region'], weight_stat_by_region['weight'], color='indigo')
    ax.set_title('Pokémon Weight by Region', fontsize=16)
    ax.set_xlabel('Region', fontsize=12)
    ax.set_ylabel('Weight (kg)', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.005, f'{height:.3f}', 
                ha='center', va='bottom', fontsize=10, color='black')

    st.pyplot(fig)


with tab4:
    st.header("Height vs Weight Correlation")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=regional_poke_data, x='height', y='weight', scatter_kws={'color': 'skyblue'}, line_kws={'color': 'red'}, ax=ax)
    ax.set_title('Height vs Weight Correlation', fontsize=16)
    ax.set_xlabel('Height (m)', fontsize=12)
    ax.set_ylabel('Weight (kg)', fontsize=12)

    st.pyplot(fig)

    correlation_matrix = np.corrcoef(regional_poke_data['height'], regional_poke_data['weight'])
    correlation_coefficient = correlation_matrix[0, 1]

    st.subheader(f"Correlation Coefficient: {correlation_coefficient:.3f}")