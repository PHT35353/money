import streamlit as st
import pandas as pd
from collections import Counter

# Initialize the deck
def initialize_deck():
    return Counter({
        2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 16, 11: 4
    })

# Calculate probabilities
def calculate_probabilities(deck, dealer_card, desired_cards):
    total_cards = sum(deck.values())
    if total_cards == 0:
        return {}, {}

    dealer_outcome_probabilities = {}

    # Calculate dealer's possible outcomes
    for card, count in deck.items():
        if count > 0:
            dealer_total = dealer_card + card
            if dealer_total > 21 and dealer_card == 11:  # Convert Ace to 1 if bust
                dealer_total -= 10
            dealer_outcome_probabilities[dealer_total] = dealer_outcome_probabilities.get(dealer_total, 0) + count / total_cards

    # Normalize probabilities for dealer outcomes
    total_dealer_prob = sum(dealer_outcome_probabilities.values())
    for key in dealer_outcome_probabilities:
        dealer_outcome_probabilities[key] /= total_dealer_prob

    # Calculate probabilities for desired cards
    desired_card_probabilities = {
        card: (deck[card] / total_cards if deck[card] > 0 else 0) for card in desired_cards
    }

    return dealer_outcome_probabilities, desired_card_probabilities

# Streamlit App
st.title("Advanced Blackjack Strategy Tool")

# Inputs
st.header("Player's Inputs")
deck = initialize_deck()
player_hand_total = st.number_input("Your Hand Total", min_value=2, max_value=21, step=1)
dealer_card = st.number_input("Dealer's Shown Card", min_value=2, max_value=11, step=1)
desired_cards = st.multiselect("Cards You Want to Draw", options=list(deck.keys()))
cards_to_exclude = st.multiselect("Cards You Don't Want to Draw", options=list(deck.keys()))

# Adjust the deck based on user's choices
for card in cards_to_exclude:
    deck[card] = 0

# Calculate probabilities
if st.button("Calculate Probabilities"):
    dealer_probs, desired_probs = calculate_probabilities(deck, dealer_card, desired_cards)

    st.subheader("Dealer's Outcome Probabilities")
    dealer_probs_df = pd.DataFrame(dealer_probs.items(), columns=["Dealer Total", "Probability"])
    st.table(dealer_probs_df)

    st.subheader("Desired Card Probabilities")
    desired_probs_df = pd.DataFrame(desired_probs.items(), columns=["Card", "Probability"])
    st.table(desired_probs_df)

# Blackjack Rules
st.sidebar.header("Blackjack Rules")
st.sidebar.write(
    """This tool incorporates advanced blackjack strategy based on probabilities:
    - Probabilities of dealer outcomes based on remaining cards in the deck.
    - Probability of drawing specific cards you want.
    - Ability to exclude cards from the deck.
    """
)
