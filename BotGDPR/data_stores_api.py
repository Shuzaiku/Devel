import requests
import bot_config
from collections import defaultdict

"""
Calls Data Stores Open Cloud API to delete all entries for a user_id configured in
STANDARD_DATA_STORE_ENTRIES. Returns a list of successful deletions and failures to delete.
"""
def delete_standard_data_stores(user_id, start_place_ids):
    successes = defaultdict(list)
    failures = defaultdict(list)
    for owned_start_place_id in bot_config.STANDARD_DATA_STORE_ENTRIES:
        if owned_start_place_id not in start_place_ids:
            continue
        universe_id, universe_entries = bot_config.STANDARD_DATA_STORE_ENTRIES[owned_start_place_id]
        for (data_store_name, scope, entry_key) in universe_entries:
            entry_key = entry_key.replace("{user_id}", user_id)
            response = requests.delete(
                f"https://apis.roblox.com/datastores/v1/universes/{universe_id}/standard-datastores/datastore/entries/entry",
                headers={"x-api-key": bot_config.OPEN_CLOUD_API_KEY},
                params={
                    "datastoreName": data_store_name,
                    "scope": scope,
                    "entryKey": entry_key
                }
            )
            if response.status_code in [200, 204]:
                successes[owned_start_place_id].append((data_store_name, scope, entry_key))
            else:
                failures[owned_start_place_id].append((data_store_name, scope, entry_key))
    return successes, failures

"""
Calls Ordered Data Stores Open Cloud API to delete all entries for a user_id configured in
ORDERED_DATA_STORE_ENTRIES. Returns a list of successful deletions and failures to delete.
"""
def delete_ordered_data_stores(user_id, start_place_ids):
    successes = defaultdict(list)
    failures = defaultdict(list)
    for owned_start_place_id in bot_config.ORDERED_DATA_STORE_ENTRIES:
        if owned_start_place_id not in start_place_ids:
            continue
        universe_id, universe_entries = bot_config.ORDERED_DATA_STORE_ENTRIES[owned_start_place_id]
        for (data_store_name, scope, entry_key) in universe_entries:
            entry_key = entry_key.replace("{user_id}", user_id)
            response = requests.delete(
                f"https://apis.roblox.com/ordered-data-stores/v1/universes/{universe_id}/orderedDatastores/{data_store_name}/scopes/{scope}/entries/{entry_key}",
                headers={"x-api-key": bot_config.OPEN_CLOUD_API_KEY}
            )
            if response.status_code in [200, 204, 404]:
                successes[owned_start_place_id].append((data_store_name, scope, entry_key))
            else:
                failures[owned_start_place_id].append((data_store_name, scope, entry_key))
    return successes, failures