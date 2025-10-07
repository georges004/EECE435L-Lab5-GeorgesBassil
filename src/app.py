from flask import Flask, request, jsonify
from flask_cors import CORS
from db import (
    create_db_table,
    get_users,
    get_user_by_id,
    insert_user,
    update_user,
    delete_user,
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure table exists on startup
with app.app_context():
    create_db_table()

@app.get("/api/users")
def api_get_users():
    return jsonify(get_users())

@app.get("/api/users/<int:user_id>")
def api_get_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.post("/api/users/add")
def api_add_user():
    payload = request.get_json(force=True)
    required = {"name", "email", "phone", "address", "country"}
    missing = [k for k in required if k not in payload or not str(payload[k]).strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    created = insert_user(payload)
    return jsonify(created), 201

@app.put("/api/users/update")
def api_update_user():
    payload = request.get_json(force=True)
    required = {"user_id", "name", "email", "phone", "address", "country"}
    missing = [k for k in required if k not in payload or (k != "user_id" and not str(payload[k]).strip())]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    existing = get_user_by_id(int(payload["user_id"]))
    if not existing:
        return jsonify({"error": "User not found"}), 404
    updated = update_user({
        "user_id": int(payload["user_id"]),
        "name": payload["name"],
        "email": payload["email"],
        "phone": payload["phone"],
        "address": payload["address"],
        "country": payload["country"],
    })
    return jsonify(updated)

@app.delete("/api/users/delete/<int:user_id>")
def api_delete_user_route(user_id: int):
    existing = get_user_by_id(user_id)
    if not existing:
        return jsonify({"error": "User not found"}), 404
    msg = delete_user(user_id)
    return jsonify(msg)

if __name__ == "__main__":
    # `flask run` also works (see below); this is fine for the lab.
    app.run(host="127.0.0.1", port=5000, debug=True)