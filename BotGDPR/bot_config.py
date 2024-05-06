import os
from dotenv import load_dotenv

# Load environment variables
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILDED_BOT_TOKEN = os.getenv("GUILDED_BOT_TOKEN")
OPEN_CLOUD_API_KEY = os.getenv("OPEN_CLOUD_API_KEY")
ROBLOX_WEBHOOK_SECRET = os.getenv("ROBLOX_WEBHOOK_SECRET")

# Declare how many ranked seasons have passed.
# Each new ranked season creates a new OrderedDataStore, so it is very important
#   to update this variable with each passing season
ranked_seasons = 0

# Dictionary of the Start place ID to
# (universe ID, list of (data stores name, scope, and entry key)) for
# Standard Data Stores
# User data stored under these entries will be deleted

STANDARD_DATA_STORE_ENTRIES = {
    # Start Place ID
    15352179962: (
        # Universe ID
        5295223317,
        [
            ("PlayerData_v4", "global", "Player_{user_id}"),
            ("PurchaseHistory", "global", "PlayerPurchases_{user_id}")
        ]
    )
}

# Dictionary of the Start place ID to
# (universe ID, list of (data stores name, scope, and entry key)) for
# Ordered Data Stores
# User data stored under these entries will be deleted

ordered_data_store_list = [
    ("TotalKillsData_TEST_STORE", "global", "PlayerTotalKills_{user_id}"),
    ("TotalKillsData_RELEASE_STORE", "global", "PlayerTotalKills_{user_id}")
]

seasonal_leaderboard_names = [
    "Kills",
    "DuelPoints",
    "DuoPoints"
]

for season in range(ranked_seasons + 1):
    scope = "global"

    for leaderboard_name in seasonal_leaderboard_names:
        data_store_name = f"{leaderboard_name}Data_v{season}"
        data_store_key = f"Player{leaderboard_name}_" + "{user_id}"
        entry = (data_store_name, scope, data_store_key)
        ordered_data_store_list.append(entry)

# print("Ordered data store list:")
# print(ordered_data_store_list)

ORDERED_DATA_STORE_ENTRIES = {
    15352179962: (
        5295223317,
        ordered_data_store_list
    )
}