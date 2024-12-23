import streamlit as st
import pandas as pd

# Blackjack Strategy Tool
def calculate_best_action(player_total, dealer_card, has_ace, can_split):
    """
    Calculate the best action based on player's total, dealer's card, 
    whether the player has an ace, and if splitting is an option.
    """
    if player_total >= 17:
        return "Stand"
    elif 13 <= player_total <= 16:
        if dealer_card >= 7:
            return "Hit"
        else:
            return "Stand"
    elif player_total == 12:
        if dealer_card in [4, 5, 6]:
            return "Stand"
        else:
            return "Hit"
    elif 9 <= player_total <= 11:
        if player_total == 11 or (player_total == 10 and dealer_card <= 9):
            return "Double Down"
        else:
            return "Hit"
    elif player_total <= 8:
        return "Hit"
    
    # Special cases
    if has_ace:
        if player_total + 10 <= 21:
            return "Hit" if dealer_card >= 7 else "Stand"

    if can_split:
        return "Split" if player_total in [16, 18] else "Hit"

    return "Stand"

# Streamlit App
st.title("Blackjack Strategy Tool")

# Inputs
st.header("Player's Hand")
player_total = st.number_input("Total Value of Your Hand", min_value=2, max_value=21, step=1)
has_ace = st.checkbox("Do you have an Ace?")
can_split = st.checkbox("Can you split?")

st.header("Dealer's Hand")
dealer_card = st.number_input("Dealer's Card Value", min_value=2, max_value=11, step=1)

# Calculate the best action
if st.button("Get Best Action"):
    best_action = calculate_best_action(player_total, dealer_card, has_ace, can_split)
    st.subheader(f"Recommended Action: {best_action}")

# Blackjack Rules
st.sidebar.header("Blackjack Rules")
st.sidebar.write(
    """This tool uses basic blackjack strategy based on the following rules:
    - Stand on 17 or higher.
    - Hit on 12-16 if dealer has 7 or higher.
    - Always hit on 8 or below.
    - Double down on 10 or 11 if possible.
    - Split pairs of 8 or aces.
    - Adjust based on whether you have an ace or can split.""")
