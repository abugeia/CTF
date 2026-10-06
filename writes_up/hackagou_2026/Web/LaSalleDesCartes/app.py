import os
import struct
import urllib.parse
from flask import Flask, request, Response, send_from_directory, jsonify

app = Flask(__name__, static_folder='public', static_url_path='')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILES_DIR = os.path.join(BASE_DIR, 'tiles')
FLAG_PATH = os.path.join(BASE_DIR, 'flag.txt')

FLAG = os.getenv("FLAG", "OPENNC{C4rt0gr4ph13_d35_pr0f0nd3ur5_dumb34_2026}")

with open(FLAG_PATH, 'w') as f:
    f.write(FLAG)

os.makedirs(TILES_DIR, exist_ok=True)

# Bathymetric tile payloads
sector_data_map = {
    "sector_alpha_1": "BATHYMETRY_V2 | SECTOR: Dumbéa Entrée | DEPTH: [12m, 45m, 89m, 120m] | REEF_SIG: 0x4131 | CONTOUR_SECTOR_A1",
    "sector_alpha_2": "BATHYMETRY_V2 | SECTOR: Récif Nord | DEPTH: [180m, 320m, 540m, 890m] | TRENCH_SIG: 0x4132 | CONTOUR_SECTOR_A2",
    "sector_beta_1": "BATHYMETRY_V2 | SECTOR: Fosse Képénéhé | DEPTH: [850m, 1200m, 1450m] | ANOMALY_SIG: 0x4231 | CONTOUR_SECTOR_B1",
    "sector_dumbea_pass": "BATHYMETRY_V2 | SECTOR: Archives Mégathalasse | DEPTH: [2100m, 2450m] | ABYSSAL_CORE_SIG: 0x4450 | CONTOUR_MEGATHALASSE_06"
}

for sec, data_str in sector_data_map.items():
    path = os.path.join(TILES_DIR, f"{sec}.bin")
    with open(path, 'wb') as f:
        f.write(data_str.encode('utf-8'))

def pack_bathymetric_tile(raw_bytes, status_code=0x0001):
    """
    Empaquète les réponses (succès comme erreurs) au format binaire NAUT :
    Header: 'NAUT' (4 bytes) | Payload Length uint32 (4 bytes) | Status uint16 (2 bytes) | Payload
    """
    magic = b'NAUT'
    length = len(raw_bytes)
    header = magic + struct.pack('>IH', length, status_code)
    return header + raw_bytes

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/sectors', methods=['GET'])
def list_sectors():
    return jsonify({
        "sectors": [
            {"id": "sector_alpha_1", "name": "Passe de Dumbéa — Entrée"},
            {"id": "sector_alpha_2", "name": "Récif Abyssal — Zone Nord"},
            {"id": "sector_beta_1", "name": "Fosse de Képénéhé"},
            {"id": "sector_dumbea_pass", "name": "Archives Cité Abysséa — Secteur Mégathalasse"}
        ],
        "system": "STÉGANOGRAPHE ANALOGIQUE DE DUMBÉA v3.4"
    })

@app.route('/api/sonar/tile', methods=['GET'])
def get_sonar_tile():
    sector = request.args.get('sector', '')
    
    if not sector:
        err_msg = b"NAUT_ERR: Missing sector parameter"
        return Response(pack_bathymetric_tile(err_msg, 0x0400), status=400, mimetype='application/octet-stream')

    if not sector.startswith('sector_'):
        err_msg = b"NAUT_ERR: Access Denied. Sector query must begin with 'sector_'"
        return Response(pack_bathymetric_tile(err_msg, 0x0403), status=403, mimetype='application/octet-stream')

    decoded_sector = urllib.parse.unquote(sector)
    
    if decoded_sector.endswith('.bin'):
        target_rel = decoded_sector
    else:
        target_rel = decoded_sector + '.bin'

    target_path = os.path.normpath(os.path.join(TILES_DIR, target_rel))

    if not os.path.exists(target_path):
        target_path_nobin = os.path.normpath(os.path.join(TILES_DIR, decoded_sector))
        if os.path.exists(target_path_nobin):
            target_path = target_path_nobin
        else:
            err_msg = f"NAUT_ERR: Tile file not found on disk at {target_path}".encode('utf-8')
            return Response(pack_bathymetric_tile(err_msg, 0x0404), status=404, mimetype='application/octet-stream')

    try:
        with open(target_path, 'rb') as f:
            content = f.read()
        
        packed = pack_bathymetric_tile(content, 0x0001)
        return Response(packed, mimetype='application/octet-stream')
    except Exception as e:
        err_msg = f"NAUT_ERR: Read error at {target_path}: {str(e)}".encode('utf-8')
        return Response(pack_bathymetric_tile(err_msg, 0x0500), status=500, mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
