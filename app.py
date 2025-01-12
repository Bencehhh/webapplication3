from flask import Flask, request, jsonify
import requests
import csv
import io

app = Flask(__name__)

# Your Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1312174281500655736/_DK4BgupYh0UZ0MN7XTe0WFMxGTGRulsb_USUoAmHPADARyU1m1Xnn6E7gOIHljloyQx"

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
        group_link = f"https://www.roblox.com/communities/{group_id}/{group_name}/about"

        # Construct the Discord embed
        embed = {
            "title": "New Game Uploaded to Roblox!",
            "description": f"A new game has been uploaded to Roblox by [Roblox User]({user_link}).",
            "color": 3066993,  # A nice green color
            "fields": [
                {
                    "name": "Uploaded By",
                    "value": f"[Roblox User]({user_link})",
                    "inline": True
                },
                {
                    "name": "Group",
                    "value": f"[Roblox Group]({group_link})",
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
            return jsonify({"error": "Failed to send notification to Discord."}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
