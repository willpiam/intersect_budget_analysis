import json
import matplotlib.pyplot as plt
import statistics

def create_bar_plot(proposals, title, filename, figsize=(20, 12)):
    plt.figure(figsize=figsize)
    
    # Calculate median length of proposal strings
    proposal_lengths = [len(proposal['proposal']) for proposal in proposals]
    median_length = int(statistics.median(proposal_lengths))
    
    # Extract data for plotting and truncate long labels
    amounts = [proposal['amount'] for proposal in proposals]
    names = []
    for proposal in proposals:
        name = proposal['proposal']
        if len(name) > median_length:
            name = name[:median_length-3] + "..."
        names.append(name)
    
    # Create bar plot
    plt.bar(range(len(amounts)), amounts)
    
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

def main():
    # Read the JSON file
    with open('data.json', 'r') as file:
        proposals = json.load(file)
    
    # Calculate total number of proposals
    total_proposals = len(proposals)
    
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
    assert len(top_half) + len(bottom_half) == len(proposals)
    # all elements of proposals is either in top or bottom (not using sets) using lambda
    assert all(lambda x: x in top_half or x in bottom_half for x in proposals)
    





    
    # Create three separate plots
    create_bar_plot(sorted_proposals, 'All Proposals by Amount Requested', 'all_proposals.png')
    create_bar_plot(top_half, 'Top Half - Most Expensive Proposals', 'top_half_proposals.png')
    create_bar_plot(bottom_half, 'Bottom Half - Least Expensive Proposals', 'bottom_half_proposals.png')

if __name__ == "__main__":
    main()