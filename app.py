from flask import Flask, request, jsonify
import requests
import csv
import io
import os

app = Flask(__name__)

# Retrieve Discord webhook URL from Render secret
WEBHOOK_URL = os.getenv("DISCORDWEBHOOK")

@app.route("/game-upload", methods=["POST"])
def game_upload():
    try:
        # Parse incoming JSON request
        data = request.json

        if not data:
            return jsonify({"error": "Invalid request, JSON payload is missing."}), 400

        # Extract necessary information
        username = data.get("username")
        user_id = data.get("user_id")
        group_id = data.get("group_id")
        group_name = data.get("group_name")

        if not username or not user_id or not group_id or not group_name:
            return jsonify({"error": "Missing required fields: username, user_id, group_id, or group_name."}), 400

        # Create Roblox user and group links
        user_link = f"https://www.roblox.com/users/{user_id}/profile"
        group_link = f"https://www.roblox.com/groups/{group_id}/about"

        # Construct the Discord embed (matching your desired format)
        embed = {
            "title": "Moderation Log",
            "description": "Server Activity Report",
            "color": 3447003,  # Blue color
            "fields": [
                {
                    "name": "Uploader",
                    "value": f"[{username}]({user_link})",
                    "inline": True
                },
                {
                    "name": "User ID",
                    "value": f"`{user_id}`",
                    "inline": True
                },
                {
                    "name": "Group",
                    "value": f"[{group_name}]({group_link})",
                    "inline": True
                },
                {
                    "name": "Group ID",
                    "value": f"`{group_id}`",
                    "inline": True
                }
            ],
            "footer": {
                "text": "CondoWare has been activated",
                "icon_url": "https://example.com/footer-icon.png"  # Replace with a valid image URL if needed
            }
        }

        # Create a CSV file in memory
        csv_output = io.StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Username", "User ID", "Group ID", "Group Name"])
        csv_writer.writerow([username, user_id, group_id, group_name])
        csv_output.seek(0)

        # Send the embed and CSV to Discord webhook
        files = {
            "file": ("game_upload.csv", csv_output.read(), "text/csv")
        }
        payload = {
            "embeds": [embed]
        }

        response = requests.post(WEBHOOK_URL, json=payload, files=files)

        # Check if the webhook request was successful
        if response.status_code == 204:
            return jsonify({"message": "Notification sent successfully!"}), 200
        else:
            return jsonify({"error": "Failed to send notification to Discord.", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
