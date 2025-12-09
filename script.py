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

        # 定義要替換的字串組 (轉換為 bytes)
        # 格式: (壞掉的名稱/Madevil環境/原始名稱, 正確的名稱/HF Patch環境/XML名稱)
        replacements = [
            # HarvexARC XRay & Gem (斜線 -> 連字符)
            (b'HarvexARC/XRay', b'HarvexARC-XRay'),
            (b'HarvexARC/Gem', b'HarvexARC-Gem'),

            # MatCap Shaders (斜線/空格 -> 底線)
            # 這是根據您提供的 XML 反推的常見錯誤命名
            (b'MatCap/Vertex/Textured Lit', b'MatCap_Vertex_Textured_Lit'),
            (b'MatCap/Vertex/Plain', b'MatCap_Vertex_Plain'),
            (b'MatCap/Vertex/Plain Additive', b'MatCap_Vertex_Plain_Additive'),
            (b'MatCap/Vertex/Plain Additive Z', b'MatCap_Vertex_Plain_Additive_Z'),
            (b'MatCap/Vertex/Textured Add', b'MatCap_Vertex_Textured_Add'),
            (b'MatCap/Vertex/Textured Multiply', b'MatCap_Vertex_Textured_Multiply'),
            (b'MatCap/Bumped/Plain', b'MatCap_Bumped_Plain'),
            (b'MatCap/Bumped/Texture Add', b'MatCap_Bumped_Texture_Add'),
            (b'MatCap/Bumped/Texture Multiply', b'MatCap_Bumped_Texture_Multiply')
        ]

        new_data = data
        total_fixed_count = 0
        is_modified = False

        # 2. 遍歷所有替換規則
        for target, replacement in replacements:
            if target in new_data:
                count = new_data.count(target)
                new_data = new_data.replace(target, replacement)
                total_fixed_count += count
                is_modified = True
                print(f"  -> 發現 '{target.decode('utf-8')}'，已替換為 '{replacement.decode('utf-8')}' ({count} 處)")

        # 3. 如果沒有任何變更，直接結束
        if not is_modified:
            print("  -> 未發現需要修復的 Shader 名稱。")
            return False
        
        # 4. 備份原始檔案
        backup_path = file_path + ".bak"
        with open(backup_path, 'wb') as f:
            f.write(data)
        print(f"  -> 已備份原始檔案至: {backup_path}")

        # 5. 寫入新檔案
        with open(file_path, 'wb') as f:
            f.write(new_data)
            
        print(f"  -> 修復成功！共計替換 {total_fixed_count} 處。")
        return True

    except Exception as e:
        print(f"  -> 發生錯誤: {e}")
        return False

def main():
    # 設定要掃描的資料夾 (預設為腳本所在目錄)
    target_dir = os.getcwd()
    
    print(f"開始掃描資料夾: {target_dir}")
    print("支援修復的 Shader 系列:")
    print("1. HarvexARC (XRay, Gem)")
    print("2. HarvexARC MatCap (Lit, Plain, Bumped, etc.)")
    print("-" * 50)

    fixed_files_count = 0
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
                fixed_files_count += 1
    
    print("-" * 50)
    print(f"掃描完成。共修復了 {fixed_files_count} 張卡片。")
    input("按 Enter 鍵退出...")

if __name__ == "__main__":
    main()
