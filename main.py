import json
import streamlit as st
from pathlib import Path



json_file = Path('player_data.json', ).read_text(encoding='utf-8')
players = json.loads(json_file)
ALL_PLAYERS = tuple(player.get('player') for player in players)

# Load JSON data with error handling
try:
    with open('player_data.json', 'r', encoding='utf-8') as file:
        footballers = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    st.error(f"Error loading JSON file: {e}")
    footballers = []


# Function to find a footballer by name
def find_footballer(name):
    for player in footballers:
        if player['player'].lower() == name.lower():
            return player
    return None


# Function to format nationality
def format_nationalities(nationalities):
    if not nationalities:
        return "Unknown"
    return ', '.join(f"{nat.get('nationalty', 'Unknown')}" for nat in nationalities)


# Function to format nationality images
def format_nationality_images(nationalities):
    if not nationalities:
        return []
    return [nat.get('nationality_url', '') for nat in nationalities]


# Function to get player information
def get_player_info(player):
    if not player:  # Check if player is None
        return {
            "Player": "Not Found", "Position": "N/A", "Age": "N/A", "Nationality": "N/A",
            "Club": "N/A", "Market Value": "N/A", "Matches": "N/A", "Goals": "N/A",
            "Assists": "N/A", "Own Goals": "N/A", "Yellow Cards": "N/A", "Second Yellow Cards": "N/A",
            "Red Cards": "N/A", "Substitution On": "N/A", "Substitution Off": "N/A",
            "Gallery URL": "", "Nationality URLs": [], "Club Image URL": ""
        }

    # Retrieve player information with correct keys
    return {
        "Player": player.get('player', 'N/A'),
        "Position": player.get('position', 'N/A'),
        "Age": player.get('age', 'N/A'),
        "Nationality": format_nationalities(player.get('nationalities', [])),
        "Club": player.get('club', 'N/A'),
        "Market Value": player.get('market_value', 'N/A'),
        "Matches": player.get('matches', 'N/A'),
        "Goals": player.get('goals', 'N/A'),
        "Assists": player.get('assists', 'N/A'),
        "Own Goals": player.get('own_goals', 'N/A'),
        "Yellow Cards": player.get('yellow_cards', 'N/A'),
        "Second Yellow Cards": player.get('second_yellow_cards', 'N/A'),
        "Red Cards": player.get('red_cards', 'N/A'),
        "Substitution On": player.get('substitution_on', 'N/A'),
        "Substitution Off": player.get('substitution_off', 'N/A'),
        "Gallery URL": player.get('gallery_url', ''),
        "Nationality URLs": format_nationality_images(player.get('nationalities', [])),
        "Club Image URL": player.get('club_image_url', '')
    }


# Main interaction loop
st.title("Welcome to Player Comparison")

# Sidebar for choosing attributes to display
with st.sidebar:
    st.write("## Choose Categories to Display")
    display_attributes = {
        "Club": st.checkbox("Club", value=True, key="club"),
        "Position": st.checkbox("Position", value=True, key="position"),
        "Age": st.checkbox("Age", value=True, key="age"),
        "Market Value": st.checkbox("Market Value", value=True, key="market_value"),
        "Nationality": st.checkbox("Nationality", value=True, key="nationality"),
        "Matches": st.checkbox("Matches", value=True, key="matches"),
        "Goals": st.checkbox("Goals", value=True, key="goals"),
        "Assists": st.checkbox("Assists", value=True, key="assists"),
        "Own Goals": st.checkbox("Own Goals", value=False, key="own_goals"),
        "Yellow Cards": st.checkbox("Yellow Cards", value=False, key="yellow_cards"),
        "Second Yellow Cards": st.checkbox("Second Yellow Cards", value=False, key="second_yellow_cards"),
        "Red Cards": st.checkbox("Red Cards", value=False, key="red_cards"),
        "Substitution On": st.checkbox("Substitution On", value=False, key="substitution_on"),
        "Substitution Off": st.checkbox("Substitution Off", value=False, key="substitution_off"),
        "Nationality Flags": st.checkbox("Nationality Flags", value=True, key="nationality_flags"),
        "Club Image": st.checkbox("Club Image", value=True, key="club_image")
    }

pl1, pl2 = st.columns(2)

with pl1:
    player1_name =  st.selectbox(
        "PLayer 1",
        ALL_PLAYERS,
        index=0,
        placeholder="Select contact method...",
    )


with pl2:
    player2_name = st.selectbox(
        "PLayer 2",
        ALL_PLAYERS,
        index=1,
        placeholder="Select contact method...",
    )


tab1, tab2 = st.tabs(["Information's", "Charts"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        player1 = find_footballer(player1_name)  # Find player object
        player1_info = get_player_info(player1)  # Get player information

    with col2:
        player2 = find_footballer(player2_name)  # Find player object
        player2_info = get_player_info(player2)  # Get player information

    # Display player information side by side
    with col1:
        if player1_info["Gallery URL"]:
            st.image(player1_info["Gallery URL"], use_column_width=True)
        st.divider()  # Divider above attributes

        for attribute, value in player1_info.items():
            if attribute not in ["Gallery URL", "Nationality URLs", "Club Image URL"] and display_attributes.get(attribute,
                                                                                                                 False):
                st.write(f"**{attribute}:** {value}")
                if attribute == "Nationality" and display_attributes.get("Nationality Flags", False):
                    col1_nationality_columns = st.columns(len(player1_info["Nationality URLs"]))
                    for i, nat_url in enumerate(player1_info["Nationality URLs"]):
                        with col1_nationality_columns[i]:
                            st.image(nat_url, width=30)
                if attribute == "Club" and display_attributes.get("Club Image", False):
                    st.image(player1_info["Club Image URL"], width=40)
                st.divider()  # Divider between each attribute

    with col2:
        if player2_info["Gallery URL"]:
            st.image(player2_info["Gallery URL"], use_column_width=True)
        st.divider()  # Divider above attributes

        for attribute, value in player2_info.items():
            if attribute not in ["Gallery URL", "Nationality URLs", "Club Image URL"] and display_attributes.get(attribute,
                                                                                                                 False):
                st.write(f"**{attribute}:** {value}")
                if attribute == "Nationality" and display_attributes.get("Nationality Flags", False):
                    col2_nationality_columns = st.columns(len(player2_info["Nationality URLs"]))
                    for i, nat_url in enumerate(player2_info["Nationality URLs"]):
                        with col2_nationality_columns[i]:
                            st.image(nat_url, width=30)
                if attribute == "Club" and display_attributes.get("Club Image", False):
                    st.image(player2_info["Club Image URL"], width=40)
                st.divider()  # Divider between each attribute

#with tab2:
 #   st.write("## Player Comparison Bar Chart")
  #  st.bar_chart( x="market_value", y="market_value", color="site", stack=False)