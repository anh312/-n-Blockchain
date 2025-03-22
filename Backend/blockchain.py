import json
import os
from block import Block
from datetime import datetime

def save_blockchain_to_file(chain, filename="blockchain_data.json"):
    """
    Lưu toàn bộ blockchain (danh sách Block) thành file JSON.
    """
    chain_data = []
    for block in chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp.isoformat(),  # sử dụng ISO format cho timestamp
            "transactions": block.transactions,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chain_data, f, ensure_ascii=False, indent=4)
    print("Blockchain đã được lưu vào file:", filename)

def load_blockchain_from_file(filename="blockchain_data.json"):
    """
    Đọc dữ liệu blockchain từ file JSON.
    Nếu file không tồn tại, trả về None.
    """
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2
        self.balances = {}  # Lưu số dư từng địa chỉ

        # Thử load blockchain từ file JSON nếu có
        loaded_chain = load_blockchain_from_file("blockchain_data.json")
        if loaded_chain:
            print("Đang khôi phục blockchain từ file...")
            for block_data in loaded_chain:
                # Tạo lại đối tượng Block từ dữ liệu lưu trữ
                block_obj = Block(
                    index=block_data["index"],
                    transactions=block_data["transactions"],
                    timestamp=datetime.fromisoformat(block_data["timestamp"]),
                    previous_hash=block_data["previous_hash"]
                )
                block_obj.hash = block_data["hash"]
                self.chain.append(block_obj)
            print("Blockchain đã được khôi phục thành công từ file.")
        else:
            # Nếu không có file, tạo block khởi tạo (Genesis block)
            self.create_genesis_block()

    def create_genesis_block(self):
        print("Creating Genesis Block...")
        genesis_block = Block(1, ["Genesis block"], datetime.now(), "0")
        self.chain.append(genesis_block)
        print(f"Genesis Block created with hash: {genesis_block.hash}")

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("No pending transactions to mine!")
            return

        print("Mining pending transactions...")
        print("Transactions to be mined:", self.pending_transactions)
        
        # Tạo block mới
        new_block = Block(
            index=len(self.chain) + 1,
            transactions=self.pending_transactions,
            timestamp=datetime.now(),
            previous_hash=self.chain[-1].hash
        )
        print(f"New Block created with index: {new_block.index}. Starting proof of work...")

        self.proof_of_work(new_block)
        
        print(f"Block mined successfully! Hash: {new_block.hash}")
        
        # Cập nhật balances cho từng giao dịch trước khi thêm block vào chain
        for tx in self.pending_transactions:
            sender = tx['sender']
            receiver = tx['receiver']
            amount = tx['amount']

            # Giảm số dư của sender (trừ đi giao dịch, nếu sender không phải SYSTEM)
            if sender != "SYSTEM":
                if sender not in self.balances:
                    self.balances[sender] = 0
                self.balances[sender] -= amount

            # Tăng số dư của receiver
            if receiver not in self.balances:
                self.balances[receiver] = 0
            self.balances[receiver] += amount

        # Thêm block vào chain
        self.chain.append(new_block)
        print("New block appended to the blockchain.")

        # Lưu blockchain ra file JSON sau khi block được thêm
        save_blockchain_to_file(self.chain)

        # Xóa pending transactions sau khi đã đưa vào block
        self.pending_transactions = []
        print("Pending transactions cleared.")

    def proof_of_work(self, block):
        print(f"Starting proof of work for Block {block.index}...")
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Proof of work completed for Block {block.index} with nonce: {block.nonce}")

    def is_valid_chain(self, chain_data):
        # Kiểm tra chain lấy từ node khác có hợp lệ không
        # Tùy bạn triển khai
        return True

    def replace_chain(self, new_chain_data):
        # Thay thế chain hiện tại bằng chain khác (nếu hợp lệ)
        # Tùy bạn triển khai
        pass
