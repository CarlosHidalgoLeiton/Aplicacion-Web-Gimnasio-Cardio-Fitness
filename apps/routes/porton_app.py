from flask import Blueprint, jsonify

porton_app = Blueprint("porton_remote_app", __name__)

# Variable global (puede ser cambiada luego a base de datos si lo preferís)
orden_apertura = {"estado": False}

@porton_app.route("/ordenar-apertura", methods=["POST"])
def ordenar_apertura():
    orden_apertura["estado"] = True
    return jsonify({"success": True, "message": "Orden enviada correctamente"})

@porton_app.route("/revisar-orden", methods=["GET"])
def revisar_orden():
    if orden_apertura["estado"]:
        orden_apertura["estado"] = False
        return jsonify({"abrir": True})
    return jsonify({"abrir": False})
