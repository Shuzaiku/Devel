import time
import hmac
import hashlib
import re
import base64

import bot_config

"""
Parses received message for Roblox signature and timestamp, the footer is only set if you
configured webhook secret
"""
def parse_footer(message):
    if not message.embeds[0].footer or \
        not message.embeds[0].footer.text:
        return "", 0
    footer_match = re.match(
        r"Roblox-Signature: (.*), Timestamp: (.*)",
        message.embeds[0].footer.text
    )
    if not footer_match:
        return "", 0
    else:
        signature = footer_match.group(1)
        timestamp = int(footer_match.group(2))
        return signature, timestamp

"""
Verifies Roblox signature with configured secret to check for validity
"""
def validate_signature(message, signature, timestamp):
    if not message or not signature or not timestamp:
        return False

    # Prevents replay attack within 300 seconds window
    request_timestamp_ms = timestamp * 1000
    window_time_ms = 300 * 1000
    oldest_timestamp_allowed = round(time.time() * 1000) - window_time_ms
    if request_timestamp_ms < oldest_timestamp_allowed:
        return False

    # Validates signature
    timestamp_message = "{}.{}".format(timestamp, message.embeds[0].description)
    digest = hmac.new(
        bot_config.ROBLOX_WEBHOOK_SECRET.encode(),
        msg=timestamp_message.encode(),
        digestmod=hashlib.sha256
    ).digest()
    validated_signature = base64.b64encode(digest).decode()
    if signature != validated_signature:
        return False

    # Valid signature
    return True

"""
Parses a received webhook messaged on Discord or Guilded. Extracts user ID, prevents replay attack
based on timestamp received, and verifies Roblox signature with configured secret to check for
validity.
"""
def parse_message(message):
    # Parses received message for user ID and game ID
    if len(message.embeds) != 1 or \
        not message.embeds[0].description:
        return "", []
    description_match = re.match(
        r"You have received a new notification for Right to Erasure for the User Id: (.*) in " +
        r"the game\(s\) with Ids: (.*)",
        message.embeds[0].description
    )
    if not description_match:
        return "", []
    user_id = description_match.group(1)
    start_place_ids = set(int(item.strip()) for item in description_match.group(2).split(","))

    signature, timestamp = parse_footer(message)
    if validate_signature(message, signature, timestamp):
        return user_id, start_place_ids
    else:
        return "", []