import os
import sys
from PIL import Image
import io

def fix_card(file_path):
    print(f"正在處理: {file_path}")
    
    try:
        # 1. 讀取原始檔案為二進位數據
        with open(file_path, 'rb') as f:
            data = f.read()

        # 定義要替換的字串 (轉換為 bytes)
        # Madevil 環境 (壞掉的/存檔裡的) -> HF Patch 環境 (能讀取的/XML裡的)
        target_bytes = b'HarvexARC/XRay'
        replacement_bytes = b'HarvexARC-XRay'

        # 2. 檢查是否存在目標字串
        if target_bytes not in data:
            print("  -> 未發現 'HarvexARC/XRay'，此卡片不需要修復或不包含該 Shader。")
            return False

        # 3. 執行替換
        # count=0 表示替換所有出現的地方
        new_data = data.replace(target_bytes, replacement_bytes)
        
        # 4. 計算替換數量
        count = data.count(target_bytes)
        
        # 5. 備份原始檔案
        backup_path = file_path + ".bak"
        with open(backup_path, 'wb') as f:
            f.write(data)
        print(f"  -> 已備份原始檔案至: {backup_path}")

        # 6. 寫入新檔案
        with open(file_path, 'wb') as f:
            f.write(new_data)
            
        print(f"  -> 修復成功！已替換 {count} 處 Shader 名稱。")
        return True

    except Exception as e:
        print(f"  -> 發生錯誤: {e}")
        return False

def main():
    # 設定要掃描的資料夾 (預設為腳本所在目錄)
    # 你可以修改這裡，或者直接把腳本放在 UserData/chara/female 資料夾下執行
    target_dir = os.getcwd()
    
    print(f"開始掃描資料夾: {target_dir}")
    print("這將把所有 'HarvexARC/XRay' 替換為 'HarvexARC-XRay'")
    print("-" * 50)

    fixed_count = 0
    png_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.png')]

    if not png_files:
        print("未找到任何 .png 檔案。請將此腳本放在角色卡資料夾中執行。")
        input("按 Enter 鍵退出...")
        return

    for filename in png_files:
        full_path = os.path.join(target_dir, filename)
        # 簡單過濾：只處理檔案大小大於 100KB 的 (避免處理到非角色卡的縮圖)
        if os.path.getsize(full_path) > 102400:
            if fix_card(full_path):
                fixed_count += 1
    
    print("-" * 50)
    print(f"掃描完成。共修復了 {fixed_count} 張卡片。")
    input("按 Enter 鍵退出...")

if __name__ == "__main__":
    main()
