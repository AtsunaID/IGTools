from flask import Flask, render_template, request, jsonify
import instaloader

app = Flask(__name__)
loader = instaloader.Instaloader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_accounts', methods=['POST'])
def check_accounts():
    usernames = request.json.get('usernames', [])
    if not usernames:
        return jsonify({"error": "Usernames are required"}), 400

    live_accounts = []
    dead_accounts = []

    for username in usernames:
        try:
            loader.check_profile_id(username.strip())
            live_accounts.append(username)
        except instaloader.exceptions.ProfileNotExistsException:
            dead_accounts.append(username)
        except Exception as e:
            dead_accounts.append(username)  # Anggap error sebagai akun "dead"

    return jsonify({
        "live_count": len(live_accounts),
        "dead_count": len(dead_accounts),
        "live_accounts": live_accounts,
        "dead_accounts": dead_accounts
    })

if __name__ == '__main__':
    app.run(debug=True)
