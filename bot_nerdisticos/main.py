import discord
import os
from pathlib import Path

# Check the bot's filesystem
def create_filesystem():
    if Path("profile").exists() is False:
        os.makedirs("profile")

# Function to create user's profile (If they exist at all)
def check_user(user_id):
    if Path(f"profile/{user_id}").exists() is False:
        os.makedirs(f"profile/{user_id}")
    if Path(f"profile/{user_id}/score").exists() is False:
        with open(f"profile/{user_id}/score", 'w') as f:
            f.write(0)
