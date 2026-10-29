from flask import jsonify

def success(message="OK", data=None, status=200):
    return jsonify({"success": True, "message": message, "data": data}), status

def error(message="Terjadi kesalahan", status=400, data=None):
    return jsonify({"success": False, "message": message, "data": data}), status
