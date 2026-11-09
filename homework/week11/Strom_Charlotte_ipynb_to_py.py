# Refactor and generalize the cartography Jupyter Notebook you worked on last week, 
# then convert it into a Python script that accepts two arguments. 
# One argument is required and the other argument is not required, but it has a default value. 
# Submit a link to your .py file.

import argparse
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
# Replace these with your existing data-loading code
NC_county_boundaries = gpd.read_file("/Users/Charlotte/Desktop/SeniorYear/GEOG_592/geog592-stromc/geog592-stromc/homework/week11/county_boundaries.geojson")
Hog_CAFOs = gpd.read_file("/Users/Charlotte/Desktop/SeniorYear/GEOG_592/geog592-stromc/geog592-stromc/homework/week11/Hog_CAFOs.geojson")

# Generalized cartography function
def county_figure(county_name, counties, cafos):

    # Select the requested county
    county = counties[counties["County"] == county_name]

    if county.empty:
        raise ValueError("County not found: " + county_name)

    # Select CAFOs in the county
    county_cafos = gpd.sjoin(
        cafos,
        county,
        how="inner",
        predicate="within"
    )

    # Create map
    fig, ax = plt.subplots(figsize=(10, 8))
    
    county.plot(ax=ax, color="lightgreen", edgecolor="black", alpha=0.5)
    county_cafos.plot(ax=ax, color="darkred", markersize=20)
    
    # Add title
    ax.set_title(county_name + " County, North Carolina",
                 fontname="Times New Roman",
                 fontsize=16,
                 fontweight="bold")
    
    # Add statistic
    sentence = (
            "There are " + str(len(county_cafos)) +
            " hog CAFO(s) in " + county_name + " County."
        )
    
    ax.text(
            0.5, -0.05, sentence,
            transform=ax.transAxes,
            ha="center", fontname="Times New Roman", fontsize=12
        )
    
    ax.set_axis_off()
    
    return fig


# Command-line arguments
def main():

    parser = argparse.ArgumentParser(
        description="Create a county CAFO map."
    )

    parser.add_argument(
        "county",
        type=str,
        help="Name of the North Carolina county"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="county_map.png",
        help="Output filename (default: county_map.png)"
    )

    args = parser.parse_args()

    # Generate map
    fig = county_figure(
        args.county,
        NC_county_boundaries,
        Hog_CAFOs
    )

    # Save map
    fig.savefig(args.output, bbox_inches="tight")

    plt.close(fig)


if __name__ == "__main__":
    main()