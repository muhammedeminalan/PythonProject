from flask import Flask, jsonify, request
from cities_data import cities

app = Flask(__name__)

# Tüm şehirleri listele
@app.route("/cities", methods=["GET"])
def list_cities():
    city_names = [city["il_adi"] for city in cities]
    return jsonify({
        "status": "success",
        "cities": city_names
    })


# Belirli bir şehrin ilçelerini döndür
@app.route("/districts", methods=["GET"])
def get_districts():
    city_name = request.args.get("city")
    if not city_name:
        return jsonify({"status": "error", "message": "city parametre zorunlu"}), 400

    city_data = next((c for c in cities if c["il_adi"].lower() == city_name.lower()), None)
    if not city_data:
        return jsonify({"status": "error", "message": "Şehir bulunamadı"}), 404

    return jsonify({
        "status": "success",
        "city": city_data["il_adi"],
        "districts": city_data["ilceler"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)