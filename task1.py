import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Global styling baseline for matplotlib
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10


# 1: load and clean data

print("Loading datasets...")
# Skip first 4 rows of the World Bank file
df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv', skiprows=4)
meta_df = pd.read_csv('Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv')

print("Merging and preprocessing demographics data...")

# Merge primary dataset with country metadata map
merged = pd.merge(df, meta_df, on='Country Code', how='left')
years = [str(y) for y in range(1960, 2025)]

# Clean and convert all historical year to float numeric values
for y in years:
    merged[y] = pd.to_numeric(merged[y], errors='coerce').fillna(0)

# Filter aggregate regions
countries_only = merged[merged['Region'].notnull()].copy()


# CHART 1: Global population distribution by region (Stacked)

print("Generating Chart 1: Regional Stacked Bar Chart...")
region_data = countries_only.groupby('Region')[years].sum().T

fig, ax = plt.subplots(figsize=(12, 7))
bottom = np.zeros(len(years))

for region in region_data.columns:
    ax.bar(years, region_data[region], bottom=bottom, label=region)
    bottom += region_data[region].values

ax.set_title('Global Population Distribution by Region (1960 - 2024)', fontsize=14, weight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Population', fontsize=12)
ax.set_xticks(years[::5])
ax.set_xticklabels(years[::5], rotation=45)
ax.legend(title='Regions', loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('region_population_trend.png', dpi=150)
plt.close()


# CHART 2: Top 10 most populous countries 2024 (Horizontal bar)

print("Generating Chart 2: Top 10 Countries Summary...")
top_10_2024 = countries_only.sort_values(by='2024', ascending=True).tail(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_10_2024['Country Name'], top_10_2024['2024'] / 1e6, color='#34d399')
ax.set_title('Top 10 Most Populous Countries in 2024', fontsize=14, weight='bold')
ax.set_xlabel('Population (Millions)', fontsize=12)
ax.set_ylabel('Country', fontsize=12)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('top_10_countries_2024.png', dpi=150)
plt.close()


# CHART 3: Trajectory of top 5 countries (Historical line graph)

print("Generating Chart 3: Top 5 Historical Growth Trajectories...")
top_5_2024 = countries_only.sort_values(by='2024', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(11, 6))
for idx, row in top_5_2024.iterrows():
    ax.plot(years, row[years] / 1e6, label=row['Country Name'], marker='o', markevery=5, linewidth=2)

ax.set_title('Population Growth Trajectory of Top 5 Countries (1960 - 2024)', fontsize=14, weight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Population (Millions)', fontsize=12)
ax.set_xticks(years[::5])
ax.set_xticklabels(years[::5], rotation=45)
ax.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('top_5_growth_trajectory.png', dpi=150)
plt.close()


# CHART 4: Population breakdown by income group 2024 (Pie Chart)

print("Generating Chart 4: Income Cohorts Allocation...")
income_data = countries_only.groupby('IncomeGroup')['2024'].sum()
income_data = income_data[income_data.index.notnull() & (income_data.index != '')]

fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#f87171', '#60a5fa', '#34d399', '#fbbf24']
ax.pie(income_data, labels=income_data.index, autopct='%1.1f%%', startangle=140, colors=colors)
ax.set_title('Global Population Breakdown by Income Group (2024)', fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig('income_group_population_2024.png', dpi=150)
plt.close()


# CHARTS 5 - 11: Country level breakdowns for each unique region

print("Extracting individual regional groups...")
regions = countries_only['Region'].unique()

for region in regions:
    print(f" -> Creating granular breakdown chart for: '{region}'")

    # Isolate mapping to single region and sort ascending
    region_df = countries_only[countries_only['Region'] == region].sort_values(by='2024', ascending=True)

    # Dynamic height sizing: Allocate 0.25 inches per country item so tall graphs are clean and legible.
    fig_height = max(6, len(region_df) * 0.25)
    fig, ax = plt.subplots(figsize=(11, fig_height))

    # Render customized regional horizontal bars
    bars = ax.barh(region_df['Country Name'], region_df['2024'] / 1e6, color='#38bdf8')

    ax.set_title(f'Population Breakdown: {region} (2024)', fontsize=13, weight='bold')
    ax.set_xlabel('Population (Millions)', fontsize=11)
    ax.set_ylabel('Country', fontsize=11)
    ax.margins(y=0.01)

    # Append localized numeric value labels to the tip of every valid bar
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(width, bar.get_y() + bar.get_height() / 2, f' {width:,.1f}M',
                    va='center', ha='left', fontsize=8.5, color='#1e293b')

    # Remove right and top aesthetic chart borders
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.grid(axis='x', linestyle='--', alpha=0.2)
    plt.tight_layout()

    # Clean up commas, spaces, and ampersands to build solid dashboard filenames
    safe_region_name = region.replace(' & ', '_').replace(' ', '_').replace(',', '')
    filename = f"region_breakdown_{safe_region_name}.png"

    plt.savefig(filename, dpi=150)
    plt.close()

print("\nProcessing complete! All 11 data visualization images have been exported successfully!.")