from flask import Flask, render_template, request, jsonify
from modules.steam_api import resolve_vanity
from urllib.parse import urlparse
from modules.calc import compute_smurf_probability


app = Flask(__name__)

def normalize_steamid(raw: str):
    raw = raw.strip()
    if raw.startswith(("http://", "https://")):
        parts = [p for p in urlparse(raw).path.split("/") if p]
        if parts and parts[0] in ("id", "profiles"):
            return parts[1], (parts[0] == "id")
    # if non-numeric, treat as vanity
    return raw, (not raw.isdigit())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/steam", methods=["GET"])
def api_steam():
    raw = request.args.get("steamid", "").strip()
    if not raw:
        return jsonify({"error": "Missing steamid parameter"}), 400

    steamid, is_vanity = normalize_steamid(raw)

    # If the provided identifier is a vanity URL / name, resolve it first
    if is_vanity:
        try:
            steamid = resolve_vanity(steamid)
        except Exception as e:
            # Early return on resolution failure so we don't hit subsequent look-ups
            return jsonify({"error": str(e)}), 400

    try:
        prob, data = compute_smurf_probability(steamid)
        data["Smurf Risk %"] = round(prob, 2)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
