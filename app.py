from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

discord_webhook_url = "https://discord.com/api/webhooks/1312174281500655736/_DK4BgupYh0UZ0MN7XTe0WFMxGTGRulsb_USUoAmHPADARyU1m1Xnn6E7gOIHljloyQx"

def send_discord_webhook(username, group):
    embed = {
        "title": "CondoWare has been activated!",
        "description": "A new game upload to Roblox has been detected!",
        "color": 0xFF5733,  # Orange-red color
        "fields": [
            {"name": "Username", "value": username, "inline": True},
            {"name": "Group", "value": group if group else "N/A", "inline": True},
        ],
        "footer": {
            "text": "Roblox Game Upload Tracker",
            "icon_url": "https://www.roblox.com/favicon.ico"
        }
    }

    data = {
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)
    if response.status_code == 204:
        print("Webhook sent successfully.")
    else:
        print(f"Failed to send webhook. Status code: {response.status_code}, Response: {response.text}")

@app.route("/upload", methods=["POST"])
def detect_game_upload():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        username = data.get("username")
        group = data.get("group")

        if not username:
            return jsonify({"error": "Username is required."}), 400

        # Send data to Discord webhook
        send_discord_webhook(username, group)

        return jsonify({"status": "success", "message": "Webhook triggered."}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
