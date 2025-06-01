import json
import matplotlib.pyplot as plt
import statistics
import os
from matplotlib.patches import Patch

# Define color mapping for different opinions
OPINION_COLORS = {
    'good': 'green',
    'bad': 'red',
    'skeptical': 'orange',
    'neutral': 'blue'  # default color for proposals without an opinion
}

def create_bar_plot(proposals, title, filename, figsize=(20, 12)):
    plt.figure(figsize=figsize)
    
    # Calculate median length of proposal strings
    proposal_lengths = [len(proposal['proposal']) for proposal in proposals]
    median_length = int(statistics.median(proposal_lengths))
    
    # Extract data for plotting and truncate long labels
    amounts = [proposal['amount'] for proposal in proposals]
    names = []
    colors = []
    for proposal in proposals:
        name = proposal['proposal']
        if len(name) > median_length:
            name = name[:median_length-3] + "..."
        names.append(name)
        # Get color from mapping, default to neutral if no opinion
        opinion = proposal.get('opinion', 'neutral')

        # assert that the opinion exists in the keys of OPINION_COLORS
        assert opinion in OPINION_COLORS.keys(), f"Opinion {opinion} not found in OPINION_COLORS"

        colors.append(OPINION_COLORS.get(opinion, OPINION_COLORS['neutral']))
    
    # Create bar plot with custom colors
    plt.bar(range(len(amounts)), amounts, color=colors)
    
    # Create legend
    legend_elements = [Patch(facecolor=color, label=opinion.capitalize()) 
                      for opinion, color in OPINION_COLORS.items()]
    plt.legend(handles=legend_elements, title='Opinion', loc='upper right')
    
    # Customize the plot
    plt.title(title)
    plt.xlabel('Proposals')
    plt.ylabel('Amount (ADA)')
    
    # Rotate x-axis labels for better readability
    plt.xticks(range(len(names)), names, rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for i, amount in enumerate(amounts):
        plt.text(i, amount, f'{amount:,}', ha='center', va='bottom', rotation=90)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Bar graph has been saved as '{filename}'")

def create_opinion_pie_chart(proposals, filename_base, figsize=(10, 10)):
    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Count proposals by opinion
    opinion_counts = {}
    opinion_amounts = {}
    for proposal in proposals:
        opinion = proposal.get('opinion', 'neutral')
        opinion_counts[opinion] = opinion_counts.get(opinion, 0) + 1
        opinion_amounts[opinion] = opinion_amounts.get(opinion, 0) + proposal['amount']

    # assert that the sum of all values in opinion counts is equal to the total number of proposals
    assert sum(opinion_counts.values()) == len(proposals), "Sum of opinion counts should be equal to the total number of proposals"
    # assert that the sum of all values in opinion amounts is equal to the total amount requested
    assert sum(opinion_amounts.values()) == sum(proposal['amount'] for proposal in proposals), "Sum of opinion amounts should be equal to the total amount requested"

    # Create pie chart for counts
    labels = [opinion.capitalize() for opinion in opinion_counts.keys()]
    sizes = list(opinion_counts.values())
    colors = [OPINION_COLORS[opinion] for opinion in opinion_counts.keys()]
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Distribution of Opinions by Number of Proposals')
    
    # Create pie chart for amounts
    amount_sizes = list(opinion_amounts.values())
    ax2.pie(amount_sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Distribution of Opinions by Total Amount Requested (ADA)')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plots
    plt.savefig(filename_base, dpi=300, bbox_inches='tight')
    print(f"Pie charts have been saved as '{filename_base}'")

def main():
    # Create charts directory if it doesn't exist
    charts_dir = 'charts'
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Read the JSON file
    with open('data.json', 'r') as file:
        proposals = json.load(file)
    
    # Calculate total number of proposals
    total_proposals = len(proposals)
    assert total_proposals == 39, f"Total proposals should be 39, but is {total_proposals}"
    
    # Calculate total amount requested
    total_amount = sum(proposal['amount'] for proposal in proposals)
    
    # Print results
    print(f"Total number of proposals: {total_proposals}")
    print(f"Total amount requested: {total_amount:,} ADA")

    # Sort proposals by amount in descending order
    sorted_proposals = sorted(proposals, key=lambda x: x['amount'], reverse=True)
    
    # Split into top and bottom halves
    mid_point = len(sorted_proposals) // 2
    top_half = sorted_proposals[:mid_point]
    bottom_half = sorted_proposals[mid_point:]
    
    # add asserts to ensure this makes sense
    assert len(top_half) + len(bottom_half) == len(proposals), "Top half and bottom half should add up to the total number of proposals"
    # all elements of proposals is either in top or bottom (not using sets) using lambda
    assert all(lambda x: x in top_half or x in bottom_half for x in proposals), "Each proposal should be in either top or bottom"
    
    # Create three separate plots
    create_bar_plot(sorted_proposals, 'All Proposals by Amount Requested', os.path.join(charts_dir, 'all_proposals.png'))
    create_bar_plot(top_half, 'Top Half - Most Expensive Proposals', os.path.join(charts_dir, 'top_half_proposals.png'))
    create_bar_plot(bottom_half, 'Bottom Half - Least Expensive Proposals', os.path.join(charts_dir, 'bottom_half_proposals.png'))
    
    # Create opinion distribution pie charts
    create_opinion_pie_chart(proposals, os.path.join(charts_dir, 'opinion_distribution.png'))

if __name__ == "__main__":
    main()