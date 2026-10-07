# 中信 VCF 9.1.1 Converge & Import 執行計畫

Management Cluster Converge 成 VCF 9.1.1 管理網域 → vRA 8.18 import / 升級 VCF Automation 9.1.1 → 整合雲 / 中信雲 Import 為 VI Workload Domain 並升級 → SRM 重新註冊；Aria Operations 8.18.7 → VCF Operations 9.1.1（客戶所稱 vRO 即 Aria Operations）。不含 NSX Edge cluster。

> 🔒 Private：內含客戶名稱與環境資訊。

## 成品（`out/`）

| 檔案 | 內容 |
|---|---|
| `CTBC_VCF911_Converge_Import_Plan.pptx` | 31 頁：原 13 步檢視、方案 A/B 決策、建議流程（17 步 / Gate / PONR）、Lab 驗證覆蓋、每步 Pre-check / Execute / Verify / Rollback、待確認、IP/DNS、官方依據 |
| `CTBC_VCF911_每步Checklist.xlsx` | 202 項逐步 checklist（狀態下拉、進度總覽自動統計）、原計畫對照、Gate 簽核、IP & DNS 規劃、待確認事項、官方文件、Lab 驗證覆蓋、Git 參考文件 |

## 怎麼改

所有步驟、檢查項、依據都在 **`scripts/content.py`**（單一來源）。改完重建：

```bash
pip install python-pptx openpyxl
# 底版：BroadcomPPT repo 的 TECH_TUESDAY_Whats_New_with_vSAN_in_VCF_9_1.pptx
export BASE_PPTX=/path/to/BroadcomPPT/TECH_TUESDAY_Whats_New_with_vSAN_in_VCF_9_1.pptx
python3 scripts/build_deck.py      # → out/CTBC_VCF911_Converge_Import_Plan.pptx
python3 scripts/build_xlsx.py      # → out/CTBC_VCF911_每步Checklist.xlsx
```

`build_xlsx.py` 寫出的公式沒有快取值；用 Excel 開啟即自動計算（或以 LibreOffice headless 重算）。

## 重點決策（2026-10-07）

- 「vRO」= Aria Operations 8.18.7：先冷遷移進管理叢集 → PAK 升 VCF Operations 9.1.1 → Converge 沿用既有 VCF Ops（9.1.1 起 VCF Ops 須在第一個 Instance 管理網域）
- WLD 採**方案 B**：vCenter 先 RDU 升 9.1.1 → SRM Reconfigure → Import 共用管理網域 NSX → ESXi 走 VCF LCM（import 8.0.3 vCenter 會自建 3-node NSX）
- vRA / Aria Operations 冷遷移（vDS 版本不同，KB 318582）；目標 port group 與 vRA 同 L2
- Offline Depot 建議架（Installer 內 binaries 不會轉給 Software Depot）
- 三套 vCenter 無 ELM（客戶 10/7 確認）

## Lab 驗證缺口（正式前補測）

S09 / S13 SRM Reconfigure、S11 / S15 匯入後 ESXi 8.0.3 → 9.1.1（VCF LCM）、方案 A。
其餘步驟的實測出處見 Excel「Lab 驗證覆蓋」頁（v8tov9、vra-lifecycle、vcf9offlinescript、debug-vcf9.1）。
