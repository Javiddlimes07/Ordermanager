import json
from typing import List, Dict, Tuple, Optional

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> List[Dict]:
    """讀取order.json檔，如不存在則返還空列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(filename: str, orders: List[Dict]) -> None:
    """儲存order.json檔"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)

def calculate_order_total(order: Dict) -> int:
    """計算單筆訂單金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])

def print_order_report(data, title: str = "訂單報表", single: bool = False) -> None:
    """出示單筆或多筆訂單報表"""
    print(f"\n{'=' * 20} {title} {'=' * 20}")
    
    if single:
        order = data
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print(f"{'商品名稱':<8}\t{'單價':<4}\t{'數量':<4}\t{'小計'}")
        print("-" * 50)
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            print(f"{item['name']:<8}\t{item['price']:<4}\t{item['quantity']:<4}\t{subtotal:,}")
        print("-" * 50)
        total = calculate_order_total(order)
        print(f"訂單總額: {total:,}")
        print("=" * 50)
    else:
        for i, order in enumerate(data, 1):
            print(f"訂單 #{i}")
            print(f"訂單編號: {order['order_id']}")
            print(f"客戶姓名: {order['customer']}")
            print("-" * 50)
            print(f"{'商品名稱':<8}\t{'單價':<4}\t{'數量':<4}\t{'小計'}")
            print("-" * 50)
            for item in order["items"]:
                subtotal = item["price"] * item["quantity"]
                print(f"{item['name']:<8}\t{item['price']:<4}\t{item['quantity']:<4}\t{subtotal:,}")
            print("-" * 50)
            total = calculate_order_total(order)
            print(f"訂單總額: {total:,}")
            print("=" * 50)
            print()

def get_valid_price() -> int:
    """取得可用價格"""
    while True:
        try:
            price = int(input("請輸入價格："))
            if price < 0:
                print("=> 錯誤：價格不可以是負數，請重新輸入！")
                continue
            return price
        except ValueError:
            print("=> 錯誤：價格或數量必須是整數，請重新輸入！")

def get_valid_quantity() -> int:
    """取得可用數量"""
    while True:
        try:
            quantity = int(input("請輸入數量："))
            if quantity <= 0:
                print("=> 錯誤：數量必須是正整數，請重新輸入！")
                continue
            return quantity
        except ValueError:
            print("=> 錯誤：價格或數量必須是整數，請重新輸入！")

def add_order(orders: List[Dict]) -> str:
    """新增訂單"""
    order_id = input("請輸入訂單編號：").upper()
    
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"
    
    customer = input("請輸入顧客姓名：")
    items = []
    
    while True:
        item_name = input("請輸入訂單項目名稱（按空白鍵結束）：")
        if not item_name:
            break
        price = get_valid_price()
        quantity = get_valid_quantity()
        items.append({"name": item_name, "price": price, "quantity": quantity})
    
    if not items:
        return "=> 至少需要一個訂單項目"
    
    new_order = {"order_id": order_id, "customer": customer, "items": items}
    orders.append(new_order)
    save_orders(INPUT_FILE, orders)
    return f"=> 訂單 {order_id} 已新增！"

def process_order(orders: List[Dict]) -> Tuple[str, Optional[Dict]]:
    """完成訂單"""
    if not orders:
        return "=> 目前沒有待處理訂單！", None
    
    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders, 1):
        print(f"{i}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("=" * 32)
    
    while True:
        selection = input("請選擇要出餐的訂單編號 (輸入數字或按空白鍵 取消): ")
        if not selection:
            return "=> 已取消出餐", None
        try:
            index = int(selection) - 1
            if 0 <= index < len(orders):
                processed_order = orders.pop(index)
                output_orders = load_data(OUTPUT_FILE)
                output_orders.append(processed_order)
                save_orders(INPUT_FILE, orders)
                save_orders(OUTPUT_FILE, output_orders)
                return f"=> 訂單 {processed_order['order_id']} 已出餐完成", processed_order
            else:
                print("=> 錯誤：請輸入有效的數字！")
        except ValueError:
            print("=> 錯誤：請輸入有效的數字！")

def main():
    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(按空白鍵離開)：")  
        
        if not choice or choice == "4":
            break
        
        if choice == "1":
            orders = load_data(INPUT_FILE)
            result = add_order(orders)
            print(result)
        
        elif choice == "2":
            orders = load_data(INPUT_FILE)
            if not orders:
                print("=> 目前沒有訂單！")
            else:
                print_order_report(orders)
        
        elif choice == "3":
            orders = load_data(INPUT_FILE)
            result, processed_order = process_order(orders)
            print(result)
            if processed_order:
                print("出餐訂單詳細資料：")  
                print_order_report(processed_order, "出餐訂單", True)
        
        else:
            print("=> 請輸入有效的選項（1-4）")