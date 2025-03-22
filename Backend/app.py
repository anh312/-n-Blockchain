from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests

from blockchain import Blockchain
from wallet import Wallet


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Hiển thị tiếng Việt không bị escape
CORS(app)

blockchain = Blockchain()

@app.route('/pending', methods=['GET'])
def get_pending_transactions():
    return jsonify(blockchain.pending_transactions), 200

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    required_fields = ['sender', 'receiver', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Thiếu thông tin giao dịch!"}), 400

    # Tạo chữ ký số
    wallet = Wallet()
    data['signature'] = wallet.sign_transaction(data)

    # Thêm giao dịch vào hàng đợi
    blockchain.pending_transactions.append({
        'sender': data['sender'],
        'receiver': data['receiver'],
        'amount': data['amount'],
        'timestamp': str(datetime.now()),
        'signature': data['signature']
    })

    return jsonify({"message": "Giao dịch đã ký và thêm vào block chờ!"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    if not blockchain.pending_transactions:
        return jsonify({"error": "Không có giao dịch để đào!"}), 400

    blockchain.mine_pending_transactions()
    return jsonify({"message": "Block mới đã được đào thành công!"}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        "index": block.index,
        "timestamp": str(block.timestamp),
        "transactions": block.transactions,
        "previous_hash": block.previous_hash,
        "hash": block.hash
    } for block in blockchain.chain]
    return jsonify(chain_data), 200

blockchain.nodes = set()

@app.route('/register_node', methods=['POST'])
def register_node():
    data = request.get_json()
    node_address = data.get('node_address')
    if not node_address:
        return jsonify({"error": "Thiếu địa chỉ node!"}), 400
    blockchain.nodes.add(node_address)
    return jsonify({"message": f"Node {node_address} đã được thêm!"}), 200

@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    longest_chain = None
    max_length = len(blockchain.chain)

    for node in blockchain.nodes:
        try:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                remote_chain = response.json()
                if len(remote_chain) > max_length and blockchain.is_valid_chain(remote_chain):
                    max_length = len(remote_chain)
                    longest_chain = remote_chain
        except requests.RequestException as e:
            print(f"Lỗi kết nối đến node {node}: {e}")

    if longest_chain:
        blockchain.replace_chain(longest_chain)
        return jsonify({"message": "Đã đồng bộ chain từ node dài nhất!"}), 200

    return jsonify({"message": "Chain hiện tại là dài nhất!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
