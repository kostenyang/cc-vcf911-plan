# -*- coding: utf-8 -*-
"""Shared content for the CTBC VCF 9.1.1 converge/import deck + per-step checklist.
Every item: cat (PRE/EXE/VER/RB), text, how (command / UI path), exp (expected), ref, own, d (deck short text or None)."""

def I(cat, t, how="", exp="", ref="", own="", d=None):
    return dict(cat=cat, t=t, how=how, exp=exp, ref=ref, own=own, d=d)

CAT_ZH = {"PRE": "前置檢查", "EXE": "執行", "VER": "完成驗證", "RB": "退版 / 截止點"}

PHASES = {
    "P0": ("準備", "Preparation"),
    "P1": ("管理網域", "Management Domain"),
    "P2": ("整合雲", "WLD 整合雲"),
    "P3": ("中信雲", "WLD 中信雲"),
    "P4": ("收尾", "Wrap-up"),
}

STEPS = []

def S(**kw):
    STEPS.append(kw)

# ---------------------------------------------------------------- S00
S(id="S00", orig="新增", phase="P0", gate="G0",
  en="Inventory, Blockers & Backups", zh="盤點、阻礙項排除與備份",
  own="ARC、ENG、SYS、NET、DR、AUTO", dur="", ponr=False,
  items=[
    I("PRE", "vRA 確切版本 ≥ 8.18.1（converge 情境頁要求 8.18.1 Patch 3，建議以 P3 為基準）", "vRA 主節點：vracli version", "≥ 8.18.1 P3", "TechDocs: Import an Existing VMware Aria Automation Instance；Converge … Aria Automation 情境頁", "AUTO", "vRA ≥ 8.18.1（建議 P3+）"),
    I("PRE", "vRO 實際版本（「8.18.7」在 Broadcom 查無此 Orchestrator 版號，需現場確認）且 ≥ 8.18.1", "vRO：vracli version", "≥ 8.18.1", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "AUTO", "vRO 實際版本（8.18.7 查無）"),
    I("PRE", "vIDM / Aria Suite Lifecycle 的版本與所在叢集（vIDM 升級後仍是 VCFA 9.1 驗證來源，不可刪）", "vSphere Client inventory", "已記錄", "TechDocs: Upgrading to VCF Automation 9.1", "AUTO", "vIDM / ASL 版本與位置"),
    I("PRE", "整合雲 / 中信雲 vCenter、ESXi 8.0.3 確切 build：8.0U3j 不可升 9.1.0、可升 9.1.1；8.0U3k 須另查 Interop Matrix（back-in-time）", "VAMI Summary；esxcli system version get", "目標 9.1.1 可行", "KB 450972；TechDocs: Upgrading to VCF 9.1.x", "SYS", "8.0.3 確切 build（back-in-time，KB 450972）"),
    I("PRE", "三套 vCenter 皆無 Enhanced Linked Mode（客戶 2026-10-07 已確認）；另確認無 vCenter HA（converge 與 import 都不支援）", "vSphere Client > vCenter > Configure > vCenter HA", "無 ELM ✔、無 VCHA", "TechDocs: Supported and Not Supported Configurations；Import an Existing vCenter", "SYS", "無 ELM ✔（10/7 已確認）；確認無 VCHA"),
    I("PRE", "叢集條件：vLCM image-based、DRS Fully Automated、VDS ≥ 8.0、vmk 靜態 IP、單一 vMotion vmk、ESXi 以 FQDN 加入 inventory", "Cluster > Updates / DRS；Host > VMkernel adapters", "全部符合", "TechDocs: Supported and Not Supported Configurations；KB 425102", "SYS", "vLCM image、DRS FA、VDS 8+、靜態 vmk、ESXi FQDN"),
    I("PRE", "DNS 正反解（A/PTR）一致、所有 FQDN 全小寫（大寫 FQDN 會讓 converge 憑證鏈失敗）", "nslookup <fqdn> / nslookup <ip>", "正反解一致、小寫", "KB 453612", "NET", "DNS A/PTR、FQDN 全小寫"),
    I("PRE", "IP / DNS 規劃完成（見『IP & DNS 規劃』頁）：VCF Mgmt Services IP pool ≥ 12（198.18.0.0/15 不可與內網重疊）、License Server A+PTR、VCFA 5 IP + runtime FQDN、RDU 暫時 IP ×2", "", "規劃表簽核", "KB 440630；TechDocs: Upgrading to VCF Automation 9.1", "NET", "IP pool ≥ 12、VCFA 5 IP、RDU 暫時 IP"),
    I("PRE", "管理叢集容量：單台主機邏輯 CPU ≥ 最大 VM vCPU（Installer 只驗叢集總量）；VCFA 藍綠升級期間資源約平時 2 倍", "", "容量足夠", "CXS Lab 實測", "ARC", "容量：單台 CPU ≥ 最大 VM；VCFA 期間 ×2"),
    I("PRE", "SRM 拓樸：兩朵雲是否互為配對、各 Protection Group 方向（protected / recovery）、replication 方式；solution account 密碼不過期設定", "SRM UI > Site Pair；Protection Groups", "已記錄", "TechDocs: Order of Upgrading vSphere and Protection and Recovery Components；KB 367383", "DR", "SRM 配對方向、replication 方式"),
    I("PRE", "Interop Matrix：VCFA 9.1.1 ↔ vCenter 8.0.3（過渡期）、SRM 9.1.1 ↔ vCenter 8.0.3 / 9.1.1、備份軟體與第三方 plugin ↔ vSphere 9.1.1", "interopmatrix.broadcom.com", "全部 Compatible 或已有對策", "Broadcom Interop Matrix", "ARC", "Interop：VCFA↔vC 8.0.3、備份軟體、plugin"),
    I("PRE", "備份：三套 vCenter file-based backup 並抽測還原；SRM 設定匯出；SFTP 備份伺服器就緒", "VAMI > Backup", "備份成功、還原驗證通過", "TechDocs: VCF 9.1 Backup and Restore", "SYS", "三套 vCenter file backup + 抽測還原"),
    I("EXE", "填寫 Planning & Preparation Workbook；開立變更單（每一步的窗口、退版時間、負責人）", "", "變更單核准", "", "PM、CHG", "Planning Workbook、變更單"),
    I("VER", "G0 簽核：阻礙項清零、備份可還原、IP/DNS 驗證完成", "", "G0 Go", "", "PM", "G0 簽核：阻礙項清零、備份可還原"),
    I("RB", "無變更（只做盤點與準備）", "", "", "", "", "無變更"),
  ])

# ---------------------------------------------------------------- S01
S(id="S01", orig="#1", phase="P1", gate="",
  en="Cold-migrate vRA / vRO into the Management Cluster", zh="vRA / vRO 冷遷移至 Management Cluster",
  own="ENG、SYS、AUTO、NET", dur="Lab：165 GB 冷遷移約 97 分 / VM（nested）", ponr=False,
  items=[
    I("PRE", "Management Cluster 提供與 vRA / vRO 現行『同一 L2 網段』的 port group（IP / FQDN 不變；VCFA 9.1 新節點也必須部署在同網段）", "VDS > Port groups", "VLAN / subnet 相同", "TechDocs: Upgrading to VCF Automation 9.1（same network）；Import an Existing VMware Aria Automation Instance", "NET", "目標 port group 與 vRA 同一 L2 網段"),
    I("PRE", "順序：CXS Lab 驗證的是管理網域建好後再搬（Converge → 搬 vRA → Import）；先搬再 Converge 亦可，但未經 Lab 驗證", "", "已決定", "CXS Lab 實測", "ARC", "Lab 驗證順序：Converge 後再搬"),
    I("PRE", "熱 vMotion 不採用：vDS 8.0.3 ↔ 9.1 不同版本間 vMotion 不支援；CXS Lab 熱遷移亦因 CPU feature 失敗 → 排停機窗口冷遷移", "", "已排窗口", "KB 318582；CXS Lab 實測", "ARC", "vDS 版本不同 → 冷遷移（KB 318582）"),
    I("PRE", "兩端 vCenter 443、ESXi 902（NFC）互通；目的 datastore 容量足夠", "Test-NetConnection / nc -zv", "可連通", "TechDocs: Import or Clone a VM with Advanced Cross vCenter vMotion", "NET", None),
    I("PRE", "記錄各節點 vApp properties / OVF 環境（vApp options 遺失會讓 vRA 服務起不來）", "VM > Configure > vApp Options（匯出截圖 / OVF）", "已備份", "KB 447218", "ENG", "備份 vApp properties（KB 447218）"),
    I("PRE", "健康基準：vracli status、pods 全 Running；凍結 vRA 請求與 vRO 排程工作流程", "kubectl get pods -n prelude", "全 Running", "CXS Lab 實測", "AUTO", "健康基準 + 凍結請求 / 排程"),
    I("EXE", "vRA 正常停止服務後關機", "主節點：/opt/scripts/deploy.sh --shutdown → Guest shutdown 各節點", "所有節點 Powered off", "TechDocs: Aria Automation 8.18 Start / Shut down", "ENG", "deploy.sh --shutdown → 關機"),
    I("EXE", "vRO 正常關機；確認各 VM CD/DVD 未掛 datastore ISO", "Guest shutdown；Edit Settings > CD/DVD", "Powered off、未掛 ISO", "CXS Lab 實測", "ENG", None),
    I("EXE", "Advanced Cross vCenter vMotion（關機狀態）：選 mgmt cluster / datastore / 同網段 port group；可選 Clone 方式保留來源（來源保持關機）作為退版點", "vSphere Client（目的 vCenter）> Import VMs；或 PowerCLI Move-VM", "遷移成功", "TechDocs: Import or Clone a VM with Advanced Cross vCenter vMotion", "ENG", "XVM 冷遷移（可 Clone 保留來源）"),
    I("EXE", "依相依性開機（vRO → vRA 全部節點），vRA 主節點啟動服務", "/opt/scripts/deploy.sh", "服務啟動", "TechDocs: Aria Automation 8.18 Start / Shut down", "ENG", "開機 → deploy.sh 啟動服務"),
    I("VER", "IP / FQDN / vApp properties 不變（ovfEnv 存在）", "cat /opt/vmware/etc/vami/ovfEnv.xml", "與遷移前一致", "KB 447218", "ENG", None),
    I("VER", "服務就緒：healthstatus 回 200、pods 全 Running（約 10–20 分）", "curl -k https://<vra-fqdn>/vco/api/healthstatus", "HTTP 200", "CXS Lab 實測", "ENG", "healthstatus 200、pods Running"),
    I("VER", "vIDM 登入、cloud account data collection、既有部署 Day-2（Power off/on）、新 catalog 請求、vRO workflow 測試", "Cloud Assembly / Service Broker / vRO Client", "全部成功", "CXS Lab 實測", "AUTO", "登入 / data collection / Day-2 / workflow"),
    I("RB", "反向冷遷移回中信雲；或刪除新 VM、開回 Clone 保留的來源", "", "回到遷移前狀態", "", "ENG", "反向冷遷移 / 開回保留來源"),
    I("RB", "截止點：S05 Import 之前", "", "", "", "", "截止：S05 Import 前"),
  ])

# ---------------------------------------------------------------- S02
S(id="S02", orig="#3", phase="P1", gate="",
  en="Deploy VCF Installer 9.1.1", zh="部署 VCF Installer 9.1.1",
  own="ENG", dur="", ponr=False,
  items=[
    I("PRE", "Installer 版本 ≥ 9.1.1（converge 文件要求），與 vCenter / ESXi 同為 9.1.1 BOM（Installer build 25713928）", "", "版本正確", "TechDocs: Deploy Components by Using VCF Installer…；VCF 9.1.1 BOM", "ENG", "Installer ≥ 9.1.1（同 9.1.1 BOM）"),
    I("PRE", "Installer IP / FQDN（A/PTR）、NTP、DNS 就緒", "nslookup", "正反解正確", "", "NET", "IP / FQDN、NTP、DNS"),
    I("PRE", "使用全新 Installer（做過 bring-up / converge 的 Installer 會記得舊 domain）", "GET https://<installer>/v1/sddcs", "回 []", "CXS Lab 實測", "ENG", "全新 Installer（/v1/sddcs = []）"),
    I("EXE", "部署 OVA（可放在 Management Cluster）；admin@local 密碼由密碼保管工具管理，不寫入文件", "vSphere Client > Deploy OVF Template", "Powered on", "", "ENG", "部署 OVA；密碼交保管工具"),
    I("VER", "UI 可登入、版本正確", "https://<installer-fqdn>", "9.1.1", "", "ENG", "UI 登入、版本 9.1.1"),
    I("RB", "刪除 Installer VM（不影響既有環境）", "", "", "", "ENG", "刪除 VM 即可（無影響）"),
  ])

# ---------------------------------------------------------------- S03
S(id="S03", orig="#4", phase="P1", gate="",
  en="Software Depot & Binaries", zh="Depot 與 Binaries（回答「Offline Depot???」）",
  own="ENG、NET", dur="", ponr=False,
  items=[
    I("PRE", "三種模式擇一：Online（activation code + proxy）／Offline Depot（自建 web server + VCF Download Tool）／Manual Transfer（下載後上傳 Installer）", "", "已決策", "TechDocs: Downloading Binaries to VCF Installer", "ARC", "三選一：Online / Offline Depot / Manual"),
    I("PRE", "建議 Offline Depot：Installer 內下載的 binaries 不會轉給部署後的 Software Depot；VCFA 與 WLD 升級還要再用", "", "", "TechDocs: Connect VCF Installer to Broadcom or an Offline Depot（not transferred）", "ARC", "建議 Offline Depot（binaries 不會轉移）"),
    I("PRE", "無 Internet 時，VCF Download Tool 是唯一支援的下載方式 → 準備可上網下載機 + activation code", "", "", "TechDocs: Manual Transfer", "ENG", None),
    I("PRE", "Depot server：HTTPS、憑證 SAN 含 FQDN + IP；Installer / SDDC Manager / VCF Ops 匯入 depot CA", "openssl s_client -connect <depot>:443", "SAN 含 FQDN 與 IP", "CXS Lab 實測", "ENG", "HTTPS 憑證（SAN 含 FQDN+IP）、匯入 CA"),
    I("EXE", "下載 converge INSTALL binaries：SDDC Manager、NSX、VCF Operations、Cloud proxy、License server、Fleet / SDDC lifecycle、Salt master / RaaS、Software depot、Telemetry、Identity broker、VCF services runtime、Migration service engine、VCF Automation", "vcf-download-tool binaries download …", "下載完成", "TechDocs: Downloading Binaries to VCF Installer", "ENG", "Converge 全套 INSTALL binaries"),
    I("EXE", "下載 vRA 升級用：VCF Automation 9.1.1 + Migration service engine 9.1.1", "vcf-download-tool binaries download …", "下載完成", "TechDocs: Upgrading to VCF Automation 9.1", "ENG", "VCFA 9.1.1 + Migration service engine"),
    I("EXE", "下載 WLD 升級用：vCenter / ESX 9.1.1（--type UPGRADE、esx download）；若走方案 A，另需與 vCenter 版本對應的 NSX install bundle", "vcf-download-tool …", "下載完成", "TechDocs: Import an Existing vCenter；Upgrading Workload Domains", "ENG", "WLD：vCenter / ESX 9.1.1（方案 A 加 NSX）"),
    I("EXE", "WLD ESXi 升級要 ESX 9.1.1 vLCM depot zip（catalog 只列 ISO；depot zip 下載需把 token 放在 URL path）", "https://dl.broadcom.com/<TOKEN>/PROD/COMP/ESX_HOST/<檔名>", "depot zip 已入 depot", "CXS Lab 實測", "ENG", "ESX 9.1.1 depot zip（不是 ISO）"),
    I("EXE", "另行準備 vRO 9.1.1 升級 ISO（S15 使用）", "", "已取得", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "AUTO", None),
    I("EXE", "Installer 連線 Offline Depot（CXS Lab：URL 用 FQDN 曾報 VMWARE_DEPOT_OFFLINE_INVALID_URL，改用 IP）", "Installer > Depot Settings", "Connected", "CXS Lab 實測", "ENG", "Installer 連 depot（Lab：URL 用 IP）"),
    I("VER", "Installer Binary Management 所需項目全部 Downloaded、無缺項；檔案 SHA256 / 大小核對", "Installer > Binary Management", "全部 Downloaded", "", "ENG", "Binary Management 全部 Downloaded"),
    I("RB", "無變更（不影響既有環境）", "", "", "", "", "無變更"),
  ])

# ---------------------------------------------------------------- S04
S(id="S04", orig="#5", phase="P1", gate="G1",
  en="Converge Management Cluster to VCF 9.1.1", zh="Management Cluster Converge 成 VCF 9.1.1 管理網域",
  own="ARC、ENG、SYS、NET", dur="Lab：約 5–5.5 h（nested）", ponr=True,
  items=[
    I("PRE", "支援組態全過：vLCM image、DRS Fully Automated、VDS ≥ 8.0、靜態 vmk、無 ELM / vCenter HA、≥ 3 台（vSAN）", "", "全部符合", "TechDocs: Supported and Not Supported Configurations to Converge to VCF", "SYS", "支援組態全過（vLCM / DRS / VDS / ELM）"),
    I("PRE", "mgmt vCenter VM 必須跑在它自己管理的叢集內；該 vCenter 下所有叢集會一起 converge（無法略過）", "", "符合", "TechDocs: Supported and Not Supported Configurations；CXS Lab 實測", "SYS", "vCenter VM 在自管叢集；全部 cluster 一起進"),
    I("PRE", "mgmt vCenter / ESXi build 與 VCF 9.1.1 BOM 一致（vCenter 25712839、ESX 25714478）；converge 會把 vLCM desired image 設為 BOM 版本", "VAMI；esxcli system version get", "與 BOM 相同", "VCF 9.1.1 BOM；CXS Lab 實測", "SYS", "vCenter / ESXi build = 9.1.1 BOM"),
    I("PRE", "vCenter 無殘留 com.vmware.sddcManager / com.vmware.vcf.client extension，無同名 SDDC Manager VM", "govc extension.info | grep -iE 'sddcmanager|vcf.client'", "無輸出", "CXS Lab 實測", "ENG", None),
    I("PRE", "vLCM remediation policy evacuate_offline_vms = true（CXS Lab 驗證會擋）", "PUT /api/esx/settings/clusters/{id}/policies/apply", "true", "CXS Lab 實測", "ENG", "vLCM evacuate_offline_vms = true"),
    I("PRE", "NSX overlay 設計：不給 TEP，或 overlay over management（mgmt VLAN 端到端 MTU ≥ 1600）；不含 NSX Edge cluster", "", "已決策", "TechDocs: Supported and Not Supported Configurations；CXS Lab 實測", "ARC", "Overlay：無 TEP 或 over mgmt（MTU ≥ 1600）"),
    I("PRE", "VCF Operations：9.1.1 起必須在第一個 Instance 的管理網域；決定新部署或沿用既有 9.1 實例", "", "已決策", "TechDocs: Deploy Components by Using VCF Installer…", "ARC", None),
    I("PRE", "VCF Automation 選『稍後部署』（vRA 走 S05 import）；mgmt vCenter file-based backup", "", "", "CXS Lab 實測", "ENG", "VCFA 選「稍後」，留給 vRA import"),
    I("EXE", "Installer > Deployment Wizard > VMware Cloud Foundation > Plan Step 1『Existing Component』勾既有 vCenter（跳過 Plan 會變 greenfield）", "Installer UI", "", "CXS Lab 實測", "ENG", "Plan 勾 Existing Component（不可跳過）"),
    I("EXE", "Prepare（VCF Mgmt Services IP pool 等）→ Validate（Warning 逐條確認）→ Deploy；下載 JSON spec 存檔", "Installer UI > Review > Download JSON spec", "Validation 無 Error", "", "ENG", "Validate → Deploy；JSON spec 存檔"),
    I("EXE", "監看里程碑：Convert vCenter → NSX → VCF Management Platform → VCF Operations → Management Services", "Installer UI / GET /v1/sddcs/{id}", "", "CXS Lab 實測", "ENG", None),
    I("VER", "全部 subtask COMPLETED_WITH_SUCCESS；SDDC Manager 管理網域 ACTIVE", "SDDC Manager UI / GET /v1/domains", "ACTIVE", "", "ENG", "全部 subtask 成功、Domain ACTIVE"),
    I("VER", "NSX：hosts Prepared / Up；VCF Operations > Lifecycle 看得到 Instance 與各元件", "NSX UI > Fabric > Hosts；VCF Ops > Build > Lifecycle", "全部正常", "", "ENG", "NSX hosts Up、VCF Ops 看得到 fleet"),
    I("VER", "授權（License Server / VCF Ops）完成；SDDC Manager / NSX SFTP 備份設定並完成第一次備份", "", "授權有效、備份成功", "", "SYS", "授權 + 第一次 SFTP 備份"),
    I("RB", "完成前失敗：刪除已部署元件 VM 與 Installer，修正後依 JSON 重做", "", "", "KB 448258", "ENG", "失敗：KB 448258 清除後重做"),
    I("RB", "成功後無官方反向程序 → G1 PONR，需客戶簽核後才進下一步", "", "", "", "PM", "⚠ 成功後不可逆（PONR）"),
  ])

# ---------------------------------------------------------------- S05
S(id="S05", orig="#6", phase="P1", gate="",
  en="Import vRA into VCF Operations", zh="vRA 匯入 VCF Operations（Fleet Lifecycle）",
  own="ENG、AUTO", dur="Lab 9.1.1：約 5 分", ponr=False,
  items=[
    I("PRE", "vRA 主節點已位於此 VCF Instance 的管理網域（S01 完成），否則升級 precheck 會在 import_vcfa 失敗", "", "符合", "TechDocs: Import an Existing VMware Aria Automation Instance；KB 425169", "ENG", "vRA 已在管理網域（KB 425169）"),
    I("PRE", "vRA ≥ 8.18.1、服務健康；root 密碼由保管工具提供", "vracli status", "健康", "", "AUTO", "vRA ≥ 8.18.1、服務健康"),
    I("PRE", "每個 fleet 只支援一個 VCF Automation 實例 → 確認 fleet 內尚無 VCFA", "VCF Ops > Lifecycle > Components", "無 VCFA", "TechDocs: Import an Existing VMware Aria Automation Instance", "ENG", "Fleet 內尚無 VCFA"),
    I("EXE", "Add Component > VCF Automation > Import 8.x appliance → VCF Instance、Primary node FQDN、root 密碼 → Trust 憑證 → Finish", "VCF Ops > Build > Lifecycle > VCF Management > Components", "Task 建立", "TechDocs: Import an Existing VMware Aria Automation Instance", "ENG", "Lifecycle > Add Component > Import 8.x"),
    I("EXE", "完成後按 Sync", "VCF Ops > Lifecycle > Sync", "", "CXS Lab 實測", "ENG", None),
    I("VER", "Task『Install components: VCF Automation』Completed；Components 出現 VCF Automation 8.18.x", "VCF Ops > Lifecycle > Tasks / Components", "Completed", "CXS Lab 實測", "ENG", "Task Completed、Components 有 VCFA 8.18.x"),
    I("VER", "來源 vRA 不受影響（服務、藍圖、部署正常，無快照）", "", "正常", "CXS Lab 實測", "AUTO", "來源 vRA 不受影響"),
    I("RB", "Import 只是註冊、來源不變；需撤除時依 KB 441333 cleanup（CXS Lab 9.1.1 實測移除後可再匯入）", "", "", "KB 441333；CXS Lab 實測", "ENG", "只是註冊；撤除走 KB 441333"),
  ])

# ---------------------------------------------------------------- S06
S(id="S06", orig="#7", phase="P1", gate="G2",
  en="Upgrade vRA 8.18 to VCF Automation 9.1.1", zh="vRA 8.18 → VCF Automation 9.1.1（藍綠升級）",
  own="ENG、AUTO、ARC", dur="Lab 9.1.1（10/7）：precheck 36 分、升級 4 h 47 m、vRA 中斷約 44 分", ponr=False,
  items=[
    I("PRE", "Depot 已有 VCFA 9.1.1 + Migration service engine 9.1.1；Sync 後 Upgrade 頁出現 VCFA 列", "VCF Ops > Lifecycle > Upgrade", "出現 VCFA 列", "TechDocs: Upgrading to VCF Automation 9.1；CXS Lab 實測", "ENG", "Depot 有 VCFA + MSE；Upgrade 頁有 VCFA 列"),
    I("PRE", "Fleet 元件 / VCF services runtime 已是 9.1.1（VCFA 9.1.1 需 runtime 9.1.1，precheck 會驗）", "VCF Ops > Lifecycle > Components", "9.1.1", "CXS Lab 實測", "ENG", "Fleet / services runtime 已 9.1.1"),
    I("PRE", "IP：5 個 IP（可不連續或 /29）與 vRA 同網段 + 1 個 runtime FQDN（IP 在 pool 外）；原 vRA IP 自動轉 VIP、FQDN 沿用", "", "DNS 就緒、IP 未使用", "TechDocs: Upgrading to VCF Automation 9.1", "NET", "5 IP 同網段 + runtime FQDN（pool 外）"),
    I("PRE", "端點憑證：cloud account 的 vCenter / NSX 憑證須已存入 DB（UI 驗證並 Accept 過者會持久化，CXS Lab 10/7 precheck 一次過）；若 precheck 報 endpoint certificates → 先 snapshot 再跑 KB 425489 腳本。另查 KB 389563 不支援 endpoints、KB 447667 FIPS、KB 450345", "Precheck details；vRA 主節點 SSH", "precheck Passed", "KB 425489；KB 389563；KB 447667；KB 450345；CXS Lab 實測", "ENG", "端點憑證已入 DB（否則 KB 425489）"),
    I("PRE", "排定 vRA 服務中斷窗口：來源關機 → 新 gateway 接管（CXS Lab 10/7 約 44 分）", "", "窗口核准", "CXS Lab 實測", "PM", "排中斷窗口（Lab 約 44 分）"),
    I("PRE", "資源：藍綠期間新舊並存約 2 倍；新 runtime 節點 24 vCPU / 96 GB（Lab Simple）", "", "容量足夠", "CXS Lab 實測", "ARC", "資源 ×2（新節點 24 vCPU / 96 GB）"),
    I("PRE", "9.1.1 起 public cloud endpoints 已 deprecated、升級後預設關閉 → 確認未使用", "Cloud Assembly > Cloud Accounts", "已確認", "VCFA 升級精靈 / VCF Automation 9.1.1 Release Notes", "AUTO", None),
    I("PRE", "保留 vIDM（仍是 VCFA 9.1 驗證來源）與 Aria Suite Lifecycle 8.x（vIDM Day-N）", "", "", "TechDocs: Upgrading to VCF Automation 9.1", "AUTO", "保留 vIDM 與 ASL 8.x"),
    I("PRE", "升級精靈密碼欄位：清掉自動產生值，改用保管工具內的標準密碼（自動產生值部署後看不到）", "", "", "CXS Lab 實測", "ENG", None),
    I("EXE", "Sync 後重新整理頁面，Upgrade 頁才會出現 VCFA 列（8.18.1 → 9.1.1）", "VCF Ops > Lifecycle > Upgrade", "Pending configuration", "CXS Lab 實測", "ENG", "Sync 後要 reload 才有 VCFA 列"),
    I("EXE", "VCFA 列 > Configure（IP pool / FQDN / 密碼）→ Run Prechecks（全部 SUCCEEDED）→ Upgrade（無確認框，按下即開始）", "VCF Ops > Lifecycle > Upgrade", "Precheck 全過", "TechDocs: Perform the Upgrade to VCF Automation 9.1", "ENG", "Configure → Prechecks 全過 → Upgrade"),
    I("EXE", "監看階段：部署新 runtime（約 2 h）→ import → prechecks → upgrade；完成後來源節點自動關機", "VCF Ops > Lifecycle > Tasks", "", "CXS Lab 實測", "ENG", None),
    I("VER", "Tenant /automation/（vIDM）與 Provider /provider 可登入；版本 9.1.1", "https://<vra-fqdn>/automation/ ; /provider", "9.1.1", "", "AUTO", "Tenant / Provider 登入、版本 9.1.1"),
    I("VER", "Projects / Cloud Accounts / Blueprints / Deployments 完整；既有部署 Day-2 與新 catalog 請求成功", "", "全部成功", "", "AUTO", "資料完整、Day-2 與新請求成功"),
    I("VER", "若 Fleet 顯示 Upgrade failed：先驗四項證據（vcfa-bundle Successful、pods Running、來源 VM 已關機、FQDN 回 9.1.1）再決定是否退版，並開 SR（9.1.0.0400 時 Lab 曾發生；9.1.1 Lab 未發生）", "kubectl get pd -n prelude；kubectl get pods -A", "", "CXS Lab 實測", "ENG", "Fleet 報 failed → 先驗 4 項證據"),
    I("RB", "Cutover 前：取消，來源 8.18 節點保持原狀", "", "", "", "ENG", "Cutover 前：來源 8.18 原封不動"),
    I("RB", "升級流程會先自動對來源 vRA 建 snapshot（automated_vcf_backup_*）再關機 → 這就是退版點，勿刪", "vCenter > vRA VM > Snapshots", "snapshot 存在", "CXS Lab 實測", "ENG", "退版點：自動 snapshot automated_vcf_backup_*"),
    I("RB", "Cutover 後：關閉新 runtime、revert 來源 vRA 的自動 snapshot 後開機；升級失敗的清理官方不支援 → 開 SR", "", "", "KB 441333", "ENG", "Cutover 後：revert 自動 snapshot＋SR"),
    I("RB", "截止點：刪除 8.18 來源 VM 與 snapshot（觀察期後）", "", "", "", "PM", "⚠ 截止：刪除 8.18 來源"),
  ])

# ---------------------------------------------------------------- S07
def wld_vc(sid, orig, phase, site):
    S(id=sid, orig=orig, phase=phase, gate="",
      en=f"{site} vCenter 8.0.3 to 9.1.1 (RDU)", zh=f"{site} vCenter 8.0.3 → 9.1.1（RDU，import 前）",
      own="ENG、SYS、DR", dur="Lab：RDU 約 33 分（停機約 5 分）；CLI migration 約 50 分", ponr=False,
      items=[
        I("PRE", "SRM 已是 9.1.1（官方建議先升 SRM 再升 vCenter ✓）；兩站互為配對時先升 protected site", "", "順序確認", "TechDocs: Order of Upgrading vSphere and Protection and Recovery Components", "DR", "SRM 9.1.1 ✓；先升 protected site"),
        I("PRE", "VAMI file-based backup 成功並記錄位置；SRM 設定匯出", "VAMI > Backup", "成功", "", "SYS", "VAMI file backup + SRM 設定匯出"),
        I("PRE", "8.0.3 build 確認可升 9.1.1（8.0U3j 可；8.0U3k 查 Interop Matrix）；9.1.1 ISO 備妥", "", "", "KB 450972；TechDocs: Upgrading to VCF 9.1.x；VCF 9.1.1 BOM", "SYS", None),
        I("PRE", "確認此 vCenter 未註冊 NSX（com.vmware.nsx.management.nsxt）：有 NSX < 9.1 註冊時 RDU switchover 會無聲卡住（precheck 只列 Warning）", "govc extension.info | grep -i nsx", "無 NSX extension", "CXS Lab 實測", "SYS", "vCenter 未註冊 NSX < 9.1（否則 RDU 卡住）"),
        I("PRE", "注意：RDU 的 --precheck-only 會先就地升級來源 vCenter 的 vLCM 服務（非唯讀），排在窗口內執行", "", "", "CXS Lab 實測", "ENG", None),
        I("PRE", "RDU 暫時 IP（不可有既存 PTR）、新 appliance 可達 NTP；/var/cache/svcaccounts/vsphere-ui/.vsphere-ui 存在", "ls /var/cache/svcaccounts/vsphere-ui/.vsphere-ui", "存在", "KB 396777；CXS Lab 實測", "ENG", "暫時 IP、NTP、KB 396777"),
        I("PRE", "第三方 plugin / 備份 agent 相容 vCenter 9.1.1；vSAN health 綠", "", "", "Broadcom Interop Matrix", "SYS", None),
        I("EXE", "vSphere Client > vCenter > Updates > vCenter Server > Upgrade（Reduced Downtime Upgrade）：掛 9.1.1 ISO → 部署目標 appliance → 資料複寫 → Switchover（排在窗口內）", "vSphere Client", "100% completed", "CXS Lab 實測", "ENG", "RDU：部署 → 複寫 → Switchover"),
        I("EXE", "不採兩階段 GUI 升級中途關機 / 重開（CXS Lab RCA：Stage 2 firstboot 失敗）", "", "", "CXS Lab 實測", "ENG", None),
        I("VER", "版本 9.1.1、服務全部 Started、SSO 登入；主機 Connected；vSAN health、VDS 正常；ESXi 仍為 8.0.3、VM 不受影響", "VAMI；vSphere Client", "全部正常", "", "SYS", "版本 / 服務 / 主機 / vSAN 正常"),
        I("RB", "Switchover 前失敗：RDU 自動回復", "", "", "TechDocs: Optimized / Sequential Update of vCenter and NSX", "ENG", "Switchover 前：RDU 自動回復"),
        I("RB", "Switchover 後：來源 VM 已退役（暫時 IP、服務停用），正式退版 = file-based restore（須事先演練）", "", "", "CXS Lab 實測", "SYS", "Switchover 後：file-based restore"),
      ])

def wld_srm(sid, orig, phase, site):
    S(id=sid, orig=orig, phase=phase, gate="",
      en=f"SRM Reconfigure & Site Pair Reconnect ({site})", zh=f"{site} vCenter 升級後 SRM 重新註冊",
      own="DR、ENG", dur="", ponr=False,
      items=[
        I("PRE", "該站 vCenter 升級完成；兩站 SRM VAMI 與 SSO 管理帳號備妥（保管工具）", "", "", "", "DR", None),
        I("PRE", "SRM-remote-* solution account 密碼未過期", "dir-cli", "未過期", "KB 448322；KB 367383", "DR", "solution account 未過期（KB 448322）"),
        I("EXE", "兩站 SRM VAMI（:5480）> Reconfigure（protected 與 recovery 兩站都要做）", "https://<srm>:5480 > Summary > Reconfigure", "成功", "KB 446701", "DR", "兩站 VAMI Reconfigure（KB 446701）"),
        I("EXE", "SRM UI > Site Pair > Summary > Reconnect", "SRM UI", "Connected", "TechDocs: Reconfigure the Connection Between Sites", "DR", "Site Pair → Reconnect"),
        I("EXE", "若 vSphere Replication 為獨立 appliance，一併確認註冊與連線（推定，Lab 驗證）", "VR VAMI", "", "推定", "DR", None),
        I("VER", "Site Pair Connected；Protection Groups OK；Replication 狀態與 RPO 正常", "SRM UI", "全部正常", "", "DR", "Site pair / PG / RPO 正常"),
        I("VER", "Recovery Plan 執行 Test（不中斷）→ Cleanup 成功", "SRM UI > Recovery Plans > Test", "Success", "", "DR", "Test Recovery + Cleanup 成功"),
        I("RB", "Reconfigure 不破壞設定；失敗依 KB 448322 修正後重做；必要時以 SRM 設定匯出還原", "", "", "KB 448322", "DR", "失敗：KB 448322 修正後重做"),
      ])

def wld_import(sid, orig, phase, site, gate):
    S(id=sid, orig=orig, phase=phase, gate=gate,
      en=f"Import {site} as a VI Workload Domain", zh=f"{site} 匯入為 VI Workload Domain（共用管理網域 NSX 9.1.1）",
      own="ARC、ENG、SYS、NET", dur="Lab：約 15 分（57 subtasks）", ponr=True,
      items=[
        I("PRE", "vCenter 已 9.1.1（共用 NSX 9.1 的前提：NSX 9.1 不支援 vCenter 8.0U3a 以後的 8.x）", "", "9.1.1", "TechDocs: Import an Existing vCenter to Create a Workload Domain", "ARC", "vCenter 已 9.1.1（共用 NSX 前提）"),
        I("PRE", "vCenter 開 SSH；ESXi 以 FQDN 加入；vLCM image（Image Setup「沿用現行映像」，之後不能回 baseline）；DRS FA；VDS 8+；無 ELM / VCHA", "", "全部符合", "TechDocs: Import an Existing vCenter；CXS Lab 實測", "SYS", "SSH、FQDN、vLCM image、DRS FA"),
        I("PRE", "在管理網域 NSX 先把此 vCenter 註冊為 Compute Manager（CXS Lab precheck Error）", "NSX UI > System > Fabric > Compute Managers", "Registered / Up", "CXS Lab 實測", "ENG", "mgmt NSX 先加 Compute Manager"),
        I("PRE", "SDDC Manager → NSX 443 可通；NSX 憑證 SAN 含所有節點 FQDN 與 VIP；授權容量足夠", "", "", "TechDocs: Import an Existing vCenter", "NET", None),
        I("EXE", "VCF Ops > Operate > Inventory > Detailed View > VCF Instances > Add Workload Domain > Import a vCenter → Prechecks → Review → Finish", "VCF Operations UI", "Prechecks 0 Error", "TechDocs: Import an Existing vCenter", "ENG", "VCF Ops > Add WLD > Import a vCenter"),
        I("EXE", "9.1.1 預設 VLAN-backed VPC、不在 DVPG 上啟用 NSX（既有 VM 網路不變）", "", "", "TechDocs: Import an Existing vCenter（9.1.1 changes）", "ARC", None),
        I("VER", "Domain ACTIVE；主機全部 ASSIGNED（ESXi 仍 8.0.3）；與管理網域共用同一套 NSX", "SDDC Manager UI；GET /v1/hosts；GET /v1/nsxt-clusters", "ACTIVE", "CXS Lab 實測", "ENG", "Domain ACTIVE、hosts ASSIGNED"),
        I("VER", "VM 網路不中斷；SRM Site Pair 仍 Connected", "", "正常", "", "DR", None),
        I("RB", "無 UI 反向程序；僅 KB 436924（API 移除匯入的 domain，troubleshooting 用）+ KB 430524（移除 NSX / compute manager）→ PONR，需簽核", "", "", "KB 436924；KB 430524", "PM", "⚠ 無 UI 反向（KB 436924）→ PONR"),
      ])

def wld_esx(sid, orig, phase, site):
    S(id=sid, orig=orig, phase=phase, gate="",
      en=f"{site} ESXi 8.0.3 to 9.1.1 via VCF Lifecycle", zh=f"{site} ESXi 8.0.3 → 9.1.1（VCF LCM / vLCM image）",
      own="ENG、SYS、DR、APP", dur="", ponr=False,
      items=[
        I("PRE", "ESXi 9.1.1 映像 / bundle 已在 Software Depot；HCL（CPU / NIC / HBA / 韌體）確認", "", "", "TechDocs: Upgrading Workload Domains to 9.1.x", "SYS", "Depot 有 ESX 9.1.1；HCL / 韌體"),
        I("PRE", "vSAN health 綠、resync = 0；N-1 容量與 HA admission 足夠；DRS FA；affinity 規則與 SRM placeholder VM 確認", "esxcli vsan debug resync summary get", "resync 0", "", "SYS", "vSAN 綠、resync 0、N-1 容量"),
        I("PRE", "vSAN on-disk format 本步不升（留到觀察期後，S16）", "", "", "TechDocs: About the vSAN Disk Format", "ARC", None),
        I("EXE", "Workload Domain > Updates：Precheck → 更新 vLCM image → ESX 升級（叢集 rolling）", "VCF Ops / SDDC Manager > Workload Domain > Updates", "", "TechDocs: Upgrading Workload Domains to 9.1.x", "ENG", "Precheck → vLCM image → ESX rolling"),
        I("VER", "6 台 build 9.1.1、全部退出 MM；vSAN 綠；cluster image compliant", "", "全部正常", "", "SYS", "6 台 9.1.1、vSAN 綠、compliant"),
        I("VER", "SRM Test Recovery 再驗一次；應用抽測", "", "成功", "", "DR、APP", "SRM Test Recovery、應用抽測"),
        I("RB", "單台 Shift+R 回 altbootbank（vLCM image 一致性影響屬推定，需 Lab 驗證）；vSAN format 升級後不可退", "", "", "KB 316592", "SYS", "單台 Shift+R（KB 316592）"),
      ])

wld_vc("S07", "#10（vCenter）", "P2", "整合雲")
wld_srm("S08", "#11", "P2", "整合雲")
wld_import("S09", "#8", "P2", "整合雲", "G3")
wld_esx("S10", "#10（ESXi）", "P2", "整合雲")
wld_vc("S11", "#12（vCenter）", "P3", "中信雲")
wld_srm("S12", "#13", "P3", "中信雲")
wld_import("S13", "#9", "P3", "中信雲", "G4")
wld_esx("S14", "#12（ESXi）", "P3", "中信雲")

# ---------------------------------------------------------------- S15
S(id="S15", orig="#2（移到最後）", phase="P4", gate="",
  en="Upgrade vRO to VCF Operations orchestrator 9.1.1", zh="vRO → VCF Operations orchestrator 9.1.1（VCFA 之後）",
  own="AUTO、ENG", dur="", ponr=False,
  items=[
    I("PRE", "順序：VCFA 9.1.1 完成後才升 external vRO（官方明文）；並建議在兩朵雲 vCenter 都 9.1.1 之後（Interop：vRO 9.1.1 對 vCenter 8.0U3 標示 Not Supported）", "", "順序確認", "TechDocs: Configure VCF Operations Orchestrator for VCF Automation VM Apps Organizations；Interop Matrix", "ARC", "VCFA 之後、兩朵雲 vCenter 9.1.1 之後"),
    I("PRE", "來源 ≥ 8.18.1；9.1.1 ISO 備妥", "vracli version", "", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "AUTO", None),
    I("PRE", "匯出自訂 packages / workflows / configurations；記錄 plugin 與 endpoints", "vRO Client > Packages > Export", "已匯出", "", "AUTO", "匯出 packages / 記錄 endpoints"),
    I("PRE", "關機 snapshot（不支援含 memory 的 snapshot）", "", "", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "ENG", "Snapshot 不含 memory"),
    I("PRE", "vSphere authentication：需當初註冊 SSO 的帳號憑證（以環境變數 / 保管工具提供，不落地明文）", "", "", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "AUTO", None),
    I("EXE", "掛載 9.1.1 ISO → 執行升級", "vracli upgrade exec -y --repo cdrom://", "Upgrade completed", "TechDocs: Upgrade to VCF Operations Orchestrator 9.1", "ENG", "vracli upgrade exec -y --repo cdrom://"),
    I("EXE", "需整合 VCFA VM Apps organization 時，驗證改指向 VCFA", "vracli vro authentication set -p tm … --tenant <org>", "", "TechDocs: Configure VCF Operations Orchestrator for VCF Automation VM Apps Organizations", "AUTO", "驗證改指向 VCFA（-p tm）"),
    I("VER", "版本 9.1.1；Control Center 正常；關鍵 workflow 執行成功；VCFA 呼叫 vRO 正常", "", "全部正常", "", "AUTO", "版本 / workflow / VCFA 整合正常"),
    I("RB", "Revert 升級前 snapshot", "", "", "", "ENG", "Revert snapshot"),
  ])

# ---------------------------------------------------------------- S16
S(id="S16", orig="新增", phase="P4", gate="G5",
  en="Observation, vSAN Format & Close-out", zh="觀察期、vSAN on-disk format 與收尾",
  own="PM、ARC、ENG、SYS", dur="", ponr=True,
  items=[
    I("PRE", "觀察期無重大事件；客戶簽核 G5", "", "簽核", "", "PM", "觀察期 OK + G5 簽核"),
    I("EXE", "vSAN on-disk format 升級（三個叢集；之後主機軟體無法退版）", "Cluster > vSAN > Disk Management > Upgrade", "完成", "TechDocs: About the vSAN Disk Format", "SYS", "vSAN on-disk format（PONR）"),
    I("EXE", "VDS 升級（選擇性）；刪除各階段 snapshot；移除已退役的 vCenter 來源 VM", "", "", "", "SYS", "VDS（選擇性）、清 snapshot / 舊 VM"),
    I("EXE", "vIDM → VCF Identity Broker 遷移另案規劃；完成前保留 vIDM 與 Aria Suite Lifecycle 8.x", "", "", "TechDocs: Migrate VCF Automation SSO from vIDM to VCF Identity Broker", "ARC", "vIDM → Identity Broker 另案"),
    I("VER", "授權、密碼 / 憑證到期監控、SFTP 備份排程正常；As-Built 與升級 / 退版測試報告", "", "交付", "", "ARC", "授權、備份排程、As-Built"),
    I("RB", "vSAN format 升級後無退版手段 → PONR", "", "", "TechDocs: About the vSAN Disk Format", "PM", "⚠ vSAN format 後不可退（PONR）"),
  ])

STEP_BY_ID = {s["id"]: s for s in STEPS}

# ---------------------------------------------------------------- original plan review
ORIG_REVIEW = [
    ("1", "vMotion vRO、vRA to Management Cluster", "調整", "改為冷遷移；目標 port group 與 vRA 同一 L2 網段（IP / FQDN 不變）", "KB 318582；Import Aria Automation 前置", "S01"),
    ("2", "Upgrade vRO to 9.1.1", "移到最後", "external vRO 必須在 vRA → VCFA 之後升；vRO 9.1.1 不支援 vRA 8.18 與 vCenter 8.0U3", "Configure VCF Ops Orchestrator…；Interop Matrix", "S15"),
    ("3", "Deploy VCF Installer 9.1.1", "照做", "全新 Installer、版本 ≥ 9.1.1", "Converge 部署頁", "S02"),
    ("4", "Offline Depot???", "建議架", "非必要（可 Manual Transfer），但 Installer 內 binaries 不會轉移，後續 VCFA / WLD 升級還要用", "Downloading Binaries to VCF Installer", "S03"),
    ("5", "Converge Management Cluster to VCF 9.1.1", "照做", "先過支援組態檢查；成功後不可逆（PONR）", "Supported / Not Supported Configurations", "S04"),
    ("6", "Import vRA to VCF", "照做", "前提：vRA 已在管理網域（Step 1）", "Import Aria Automation in VCF Ops", "S05"),
    ("7", "Upgrade vRA to 9.1.1", "照做", "KB 425489 腳本；5 IP + runtime FQDN 同網段", "Upgrading to VCF Automation 9.1", "S06"),
    ("8", "Import 整合雲", "調整", "import 8.0.3 會自建 3-node NSX 4.2；建議先升 vCenter 再 import、共用管理網域 NSX", "Import an Existing vCenter", "S09"),
    ("9", "Import 中信雲", "調整", "同上", "Import an Existing vCenter", "S13"),
    ("10", "Upgrade 整合雲 to 9.1.1", "拆兩段", "vCenter 在 import 前以 RDU 升；ESXi 在 import 後走 VCF LCM", "Import 頁；WLD 升級頁", "S07 + S10"),
    ("11", "SRM 重新註冊（整合雲）", "照做", "兩站 VAMI Reconfigure + Site Pair Reconnect", "KB 446701", "S08"),
    ("12", "Upgrade 中信雲 to 9.1.1", "拆兩段", "同 10", "Import 頁；WLD 升級頁", "S11 + S14"),
    ("13", "SRM 重新註冊（中信雲）", "照做", "同 11；每次 vCenter 升級後兩站都要做", "KB 446701", "S12"),
]

GATES = [
    ("G0", "S00 後", "盤點與備份", "阻礙項清零、三套 vCenter 備份可還原、IP/DNS 驗證完成", "PM、ARC", False),
    ("G1", "S04 後", "Converge 完成", "管理網域 ACTIVE、NSX / VCF Ops 正常、第一次 SFTP 備份成功", "PM、ARC", True),
    ("G2", "S06 後", "VCFA 9.1.1 cutover", "Tenant / Provider 登入、資料完整、Day-2 成功；8.18 來源保留至觀察期後", "PM、AUTO", False),
    ("G3", "S09", "整合雲 import", "vCenter 9.1.1 正常、SRM Test Recovery 成功、Compute Manager 已註冊", "PM、ARC、DR", True),
    ("G4", "S13", "中信雲 import", "同 G3", "PM、ARC、DR", True),
    ("G5", "S16", "vSAN on-disk format", "觀察期無重大事件、客戶簽核", "PM", True),
]

OPEN_ITEMS = [
    ("vRA 確切版本 / patch", "converge 情境頁要求 8.18.1 P3；import 頁為 8.18.1+", "vracli version", "AUTO"),
    ("vRO 實際版本", "「8.18.7」查無此 Orchestrator 版號；升級來源需 ≥ 8.18.1", "vracli version", "AUTO"),
    ("vIDM / Aria Suite Lifecycle 位置與版本", "vIDM 升級後仍是 VCFA 驗證來源；是否隨 vRA 一起搬", "vSphere inventory", "AUTO"),
    ("vCenter HA", "converge 與 import 都不支援 VCHA（ELM 已於 10/7 確認沒有）", "vSphere Client", "SYS"),
    ("兩朵雲 8.0.3 確切 build", "8.0U3j → 9.1.0 不支援、→ 9.1.1 支援；8.0U3k 需查 Interop（KB 450972 back-in-time）", "VAMI / esxcli", "SYS"),
    ("SRM 配對拓樸", "兩朵雲是否互為配對、PG 方向、replication 方式 → 決定先升哪一站", "SRM UI", "DR"),
    ("WLD import 方案 A / B", "A：import 8.0.3（自建 3-node NSX 4.2）／B：先升 vCenter 再 import 共用 NSX（建議）", "設計會議", "ARC、PM"),
    ("Management Cluster 網段與容量", "需提供 vRA 同 L2 網段；VCFA 藍綠期間資源約 2 倍", "網路 / 容量盤點", "NET、ARC"),
    ("VCF Operations 新部署或沿用", "9.1.1 起須在第一個 Instance 管理網域；是否已有 Aria Operations 8.18", "盤點", "ARC"),
    ("過渡期 interop", "Interop 對 Aria Automation 8.18 ↔ vCenter / ESX 9.x 標 Not Supported（推定指 endpoint）；過渡期盡量縮短、必要時開 SR 確認", "Interop Matrix / SR", "ARC"),
    ("vLCM image 叢集 Shift+R 退版", "KB 316592 未說明對 vLCM image 一致性的影響", "Lab 驗證 + SR", "ENG"),
]

DOCS = [
    ("Converge", "Supported and Not Supported Configurations to Converge to VCF", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/converging-your-existing-vsphere-infrastructure-to-a-vcf-or-vvf-platform-/supported-and-not-supported-configurations.html"),
    ("Converge", "Deploy Components by Using VCF Installer to Complete the Converging to VCF Process", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/converging-your-existing-vsphere-infrastructure-to-a-vcf-or-vvf-platform-/use-existing-vsphere-infrastructure-to-create-a-new-vcf-fleet-or-a-new-vcf-instance-using-the-deployment-wizard.html"),
    ("Converge", "Converge vCenter, ESX Hosts, Aria Suite Lifecycle and Aria Automation", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/converging-your-existing-vsphere-infrastructure-to-a-vcf-or-vvf-platform-/supported-scenarios-to-converge-to-vcf/converge-your-existing-vcenter-instance-esx-hosts-vrealize-suite-lifecycle-manager-and-vmware-aria-automation.html"),
    ("Depot", "Downloading Binaries to VCF Installer", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/deploying-a-new-vmware-cloud-foundation-or-vmware-vsphere-foundation-private-cloud-/preparing-your-environment/downloading-binaries-to-the-vcf-installer-appliance.html"),
    ("Depot", "Connect VCF Installer to Broadcom or an Offline Depot", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/deploying-a-new-vmware-cloud-foundation-or-vmware-vsphere-foundation-private-cloud-/preparing-your-environment/downloading-binaries-to-the-vcf-installer-appliance/connect-to-an-online-depot-to-download-binaries.html"),
    ("Depot", "Connect SDDC Manager to a Software Depot", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/binary-management-for-vmware-cloud-foundation/connect-sddc-manager-to-a-software-depot-for-downloading-bundles.html"),
    ("Automation", "Import an Existing VMware Aria Automation Instance in VCF Operations", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/phase-3-import-and-upgrade-aria-automation-8-to-vcf-automation-9/import-an-existing-vmware-aria-automation-instance-in-vcf-operations.html"),
    ("Automation", "Upgrading to VCF Automation 9.1", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/phase-3-import-and-upgrade-aria-automation-8-to-vcf-automation-9.html"),
    ("Automation", "Perform the Upgrade to VCF Automation 9.1", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/phase-3-import-and-upgrade-aria-automation-8-to-vcf-automation-9/upgrade-to-vcf-automation.html"),
    ("Automation", "Migrate VCF Automation SSO from vIDM to VCF Identity Broker", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/phase-3-import-and-upgrade-aria-automation-8-to-vcf-automation-9/migrate-vcf-automation-single-sign-on-configuration-from-vmware-identity-manager-to-vcf-identity-broker.html"),
    ("Orchestrator", "Upgrade to VCF Operations Orchestrator 9.1", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation/upgrade-a-standalone-or-clustered-vrealize-orchestrator-8-0-1-deployment-with-iso-image.html"),
    ("Orchestrator", "Configure VCF Operations Orchestrator for VCF Automation VM Apps Organizations", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/deploying-a-new-vmware-cloud-foundation-or-vmware-vsphere-foundation-private-cloud-/manual-deployment-of-components-to-complete-your-vcf-platform/download-and-deploy-the-vco-va/integrate-vcf-operations-orchestrator-with-vcf-automation-for-vm-apps.html"),
    ("Upgrade", "Upgrading to VCF 9.1.x（元件升級順序）", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/deployment/upgrading-cloud-foundation.html"),
    ("Import WLD", "Import an Existing vCenter to Create a Workload Domain", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/building-your-private-cloud-infrastructure/working-with-workload-domains/import-an-existing-vcenter-to-create-a-workload-domain.html"),
    ("Import WLD", "Upgrading VCF Workload Domains to 9.1.x", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/lifecycle-management/upgrade-workload-domains-to-vcf-5-2.html"),
    ("vMotion", "Import or Clone a VM with Advanced Cross vCenter vMotion (vSphere 9.1)", "https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vcenter-and-host-management/migrating-virtual-machines/vmotion-across-vcenter-server-systems/migrate-a-virtual-machine-from-an-external-vcenter-server-instance.html"),
    ("SRM", "Protection and Recovery 9.1.1.0 Release Notes", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/protection-and-recovery/9-1/release-notes/protection-and-recovery-9110-release-notes.html"),
    ("SRM", "Order of Upgrading vSphere and Protection and Recovery Components", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/protection-and-recovery/9-1/protection-and-recovery-installation/setting-up-vmware-live-site-recovery-overview/convergence-and-upgrade/upgrading-srm/order-of-upgrading-vsphere-and-srm-components.html"),
    ("SRM", "Reconfigure the Connection Between Sites", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/protection-and-recovery/9-1/protection-and-recovery-installation/setting-up-vmware-live-site-recovery-overview/reconfiguring-the-site-recovery-manager-virtual-appliance/reconfigure-the-connection-between-sites.html"),
    ("Release", "VMware Cloud Foundation 9.1.1.0 Release Notes", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/vmware-cloud-foundation-9-1-1-0-release-notes.html"),
    ("Release", "VMware Cloud Foundation 9.1.1.0 Bill of Materials", "https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/release-notes/vmware-cloud-foundation-9-1-1-0-release-notes/vmware-cloud-foundation-9-1-1-0-bill-of-material.html"),
    ("Interop", "Broadcom Product Interoperability Matrix", "https://interopmatrix.broadcom.com/Interoperability"),
]

KBS = [
    ("440630", "Upgrade sequence and related issues for VCF and vSphere Foundation 9.1"),
    ("450972", "vSphere / VCF 9.1 Back-in-Time 支援表（8.0U3j/k → 9.1.0 不支援升級 / converge）"),
    ("448258", "Converge 失敗：刪除已部署元件與 Installer 後重做"),
    ("453612", "vCenter FQDN 含大寫導致 converge 憑證鏈失敗"),
    ("425102", "ESX 主機須以 FQDN 加入 inventory"),
    ("436924", "How to remove an imported Domain from VCF 9.x"),
    ("430524", "移除主機上的 NSX 與 Compute Manager"),
    ("429205", "Import 時 NSX 版本控制（方案 A 用）"),
    ("425169", "Importing Aria Automation 8.x — 不在管理網域時網路選項不可用"),
    ("425489", "8.x endpoint certificates upgrade pre-check fails"),
    ("389563", "Essential prechecks for a successful VCF Automation upgrade（不支援的 endpoints）"),
    ("447667", "VCF Automation upgrade to 9.x fails — FIPS"),
    ("450345", "Aria Automation 8.18.1 upgrade precheck — 來源 IP / 網段"),
    ("441333", "VCF Automation 元件 cleanup（升級失敗清理不支援 → SR）"),
    ("318582", "不同版本 vDS 之間的 vMotion"),
    ("447218", "Aria Automation services fail to start — vApp options 遺失"),
    ("446701", "vCenter 升級後於兩站執行 SRM VAMI Reconfigure"),
    ("448322", "SRM Reconfigure 失敗 — SRM-remote solution account 密碼過期"),
    ("367383", "Solution account 密碼不過期設定"),
    ("396777", "RDU 切換時 vsphere-ui 服務帳號缺失"),
    ("316592", "ESXi Shift+R 回復前一版（altbootbank）"),
]

IPDNS = [
    ("VCF Installer", "1", "1", "Mgmt", "可放在 Management Cluster"),
    ("SDDC Manager", "1", "1", "Mgmt", ""),
    ("NSX Manager（管理網域）", "VIP 1 + 節點 1 或 3", "VIP + 每節點", "Mgmt", "無 NSX Edge cluster；NSX 憑證 SAN 含所有節點 FQDN 與 VIP"),
    ("VCF Operations", "1（Simple）或 3（HA）", "每節點", "Mgmt", "9.1.1 起須在第一個 Instance 的管理網域"),
    ("VCF Operations Cloud Proxy", "1", "1", "Mgmt", ""),
    ("License Server", "1", "1（A + PTR 必要）", "Mgmt", "KB 440630"),
    ("VCF Identity Broker", "1", "1", "Mgmt", ""),
    ("VCF Management Services（services runtime）", "IP pool ≥ 12（最多 30）", "Fleet / Instance FQDN", "Mgmt", "內部網段 198.18.0.0/15 不可與內網重疊（KB 440630）"),
    ("VCF Automation 9.1.1（升級用）", "5（可不連續或 /29）", "runtime FQDN 1（IP 在 pool 外）", "vRA 現行網段", "原 vRA IP 自動轉 VIP、FQDN 沿用"),
    ("RDU 暫時 IP — 整合雲 vCenter", "1", "—（不可有既存 PTR）", "整合雲 Mgmt", "Switchover 後釋放"),
    ("RDU 暫時 IP — 中信雲 vCenter", "1", "—（不可有既存 PTR）", "中信雲 Mgmt", "Switchover 後釋放"),
    ("Offline Depot Server", "1", "1", "Mgmt", "HTTPS；憑證 SAN 含 FQDN + IP"),
]

GIT_REFS = [
    ("S01", "vra-lifecycle（private）", "runbooks/vcf911-vra8-import-upgrade-worklog.md › Phase ④", "vRA appliance 跨 vCenter 搬進管理網域：熱遷移因 CPU feature 失敗、165 GB 冷遷移約 97 分；/vco/api/healthstatus 作為就緒判斷"),
    ("S01", "vra-lifecycle（private）", "runbooks/scripts/vcf911-vra8-upgrade/coldmove-vra9.ps1、xvmotion-vra9.ps1", "PowerCLI 冷 / 熱遷移腳本（PowerCLI 模組需釘同一版 13.5）"),
    ("S01", "vra-lifecycle（private）", "runbooks/vra8-cross-vcenter-migration-day2-power.md", "vRA 管的 workload VM 跨 vCenter 搬遷後 Day-2 可用；_ovfenv ISO 擋熱 vMotion → 冷搬（對象是 workload VM，不是 appliance）"),
    ("S02 / S04", "vcf9.1-lab-private（private）", "installer-deploy/（Invoke-Vcf9InstallerDeploy_v1.ps1、spec/management-domain.template_v1.json）", "Installer 部署腳本與 spec 範本"),
    ("S03", "vcf9offlinescript", "README.md、CUSTOMER-DEPLOY-GUIDE.md、create_vcf9_depot_server_v5.sh、import_vcf9depot_ca.sh", "Offline depot 一鍵建置（nginx / apache、HTTPS、basic auth）、CA 匯入 Installer / SDDC Manager / VCF Ops、客戶交付指南"),
    ("S03", "vcf9offlinescript", "INSTALLER_CONNECT_TROUBLESHOOTING.md、DEPOT-WAY-A/B/C、DOWNLOAD-INTO-DEPOT.md", "Installer 連 depot 除錯；三種灌 binaries 的方式"),
    ("S03", "vcf-download-tool", "README / CLI-REFERENCE / GOTCHAS / PROXY / WINDOWS", "VCF Download Tool 用法、proxy、Windows、activation code 判讀"),
    ("S03", "vcf9.1-lab-private（private）/ vcf9offlinescript", "FLEET-DEPOT-CA-TRUST.md", "Fleet Depot Service 信任自簽 depot CA（KB 442978；private 版含腳本）"),
    ("S04", "v8tov9", "converge/README.md（範本 1–3）", "Converge 9.1.1 JSON 範本：不給 TEP / 沿用既有 NSX / 多 cluster；逐 cluster 驗證項；evacuate_offline_vms；vSS 是硬擋點"),
    ("S04", "v8tov9", "converge/no-overlay/（README + VCF911-Converge-NoOverlay.docx）", "完全不部署 overlay 的 converge：23 頁手冊、5 個里程碑耗時、14 個踩坑速查"),
    ("S04", "v8tov9", "converge-existing-ops/README.md", "沿用既有 VCF Ops / License Server；Plan › Existing Component；容量驗證只看叢集總量；depot URL 用 IP"),
    ("S04", "debug-vcf9.1", "08-ops-loss-and-mgmt-rebuild.md §4、04-bringup-failures.md", "Converge 精靈踩雷：IP Pool ≥ 12、DRS fully automated、certificate chain"),
    ("S05 / S06", "vra-lifecycle（private）", "runbooks/vcf911-vra8-import-upgrade-worklog.md", "Import 精靈、precheck 擋點（管理網域、KB 425489）、藍綠升級階段、fleet 誤報 failed 的 4 項證據"),
    ("S05 / S06", "debug-vcf9.1", "deliverables/kb441333-vcfa-removal/（含 m03-test-notes-20261007.md）", "VCFA 正常移除三步；9.1.1 移除後再匯入 vRA 8 並升級成功（import 5 分、升級 4 h 47 m）"),
    ("S06", "vra-lifecycle（private）", "runbooks/vcfa-reset-provider-password.md", "Provider 密碼遺失時的重設程序"),
    ("S06", "vra-lifecycle（private）", "runbooks/vcf911-vcfa-fleet-record-manual-fix-optionB.md", "⚠ 非官方：fleet 帳面補正（僅限 lab；客戶環境請開 SR）"),
    ("S06", "debug-vcf9.1", "06-vcfa.md", "VCFA 應用層除錯（gateway / pods / region quota）"),
    ("S07 / S11", "v8tov9", "vc-8.0.3-to-9.1.1-firstboot-failure/README.md", "vCenter 8.0.3 → 9.1.1 GUI 兩階段失敗 RCA；建議 RDU（33 分、停機約 5 分）；KB 396777"),
    ("S07 / S11", "v8tov9", "doc/vcenter-8.0-to-9.1/vc8-0-3-to-9-1-migration-upgrade.docx", "vCenter 8.0.3 → 9.1 升級 walkthrough"),
    ("S09 / S13", "v8tov9", "import-wld/（README、PHASE4-import-runbook.md、VCF911-CoverageLab-ImportWLD.docx）", "既有 vSphere 匯入 VI WLD 並共用管理網域 NSX；precheck 3 個 Error 修法；50 頁手冊"),
    ("S09 / S13", "debug-vcf9.1", "deliverables/kb452458-principal-datastore/", "匯入叢集的 principal datastore 變更（KB 452458）"),
    ("S10 / S14", "v8tov9", "esxi-standalone-upgrade/", "vLCM image 升主機；VCF 納管規則（build 必須等於 BOM）"),
    ("S10 / S14", "vcf-skills", "vcf-9-ppt/runbooks/vcf9-host-maintenance-rotation.md；vcf-upgrade-ppt/runbooks/upgrade-precheck-runbook.md", "主機維護輪替、升級 precheck"),
    ("S08 / S12", "—", "（Git 上沒有）", "SRM / Live Recovery 重新註冊無既有文件 → 依 KB 446701 與 TechDocs"),
    ("S15", "—", "（Git 上沒有）", "vRO standalone 升級無既有文件 → 依 TechDocs《Upgrade to VCF Operations Orchestrator 9.1》"),
    ("全程", "debug-vcf9.1", "README.md（症狀路由表）、reference/commands.md", "除錯索引與常用指令"),
    ("全程", "lab-info", "runbooks/backup-sftp.md、runbooks/depot-server.md", "SFTP 備份、depot server 紀錄"),
]

# ---- 中信雲-specific additions (also shown on the S11–S14 deck slide)
STEP_BY_ID["S11"]["items"].insert(1, I("PRE", "若中信雲為 recovery site（依 PG 方向判定），排在 protected site 升級之後", "", "順序確認", "TechDocs: Order of Upgrading vSphere and Protection and Recovery Components", "DR", "若為 recovery site → 排在 protected site 之後"))
STEP_BY_ID["S11"]["items"].insert(2, I("PRE", "vRA / vRO 已移出中信雲；確認 vIDM / Aria Suite Lifecycle 所在位置不受此 RDU 停機影響", "", "已確認", "", "AUTO", "確認 vIDM / ASL 不受 RDU 停機影響"))
STEP_BY_ID["S12"]["items"].insert(6, I("VER", "Test Recovery 兩個方向都驗（若兩朵雲互為配對）", "SRM UI > Recovery Plans > Test", "Success", "", "DR", "Test Recovery 兩個方向都驗"))


# ---- CXS Lab coverage (github.com/kostenyang)
LAB_COVERAGE = [
    ("S01", "vRA 冷遷移進管理網域", "已驗證", "2026-09-09（m02）", "熱遷移因 CPU feature 失敗 → 冷遷移 165 GB 約 97 分；搬入後 import precheck 通過", "Lab 是管理網域已建好後才搬；先搬再 Converge 未驗證", "vra-lifecycle worklog Phase ④"),
    ("S02 / S03", "VCF Installer、Offline Depot", "已驗證", "多次（9 月）", "v5 depot 腳本、CA 匯入、客戶交付包；depot URL 用 IP", "—", "vcf9offlinescript、vcf-download-tool"),
    ("S04", "Converge vCenter 9.1.1 + ESXi 9.1.1", "已驗證", "2026-09-19 / 09-30 / 10-05", "多 cluster、無 overlay、overlay over mgmt、沿用既有 VCF Ops 皆 COMPLETED_WITH_SUCCESS；約 5–5.5 h", "Lab 是 nested 4 台；CTBC 為 6 台實體", "v8tov9 converge/、converge-existing-ops/"),
    ("S05", "Import vRA 8.18.1", "已驗證", "2026-09-06 / 10-07（m03）", "import 約 5 分，來源不受影響", "—", "vra-lifecycle（branch vra8-import-upgrade-m03）"),
    ("S06", "vRA → VCF Automation 9.1.1", "已驗證", "2026-10-07（m03）", "precheck 一次過 36 分、升級 4 h 47 m 一次成功、中斷約 44 分、資料 ID 全相同；來源自動 snapshot", "9/9 m02（fleet 9.1.0.0400）曾 7 h 55 m + 假失敗", "vra-lifecycle（branch vra8-import-upgrade-m03）"),
    ("S07 / S11", "vCenter 8.0.3 → 9.1.1", "已驗證", "2026-08-19 / 09-21 / 10-02", "RDU 33 分；CLI migration 50 分；RDU 遇 NSX < 9.1 註冊會卡 switchover", "Lab 無 SRM extension", "v8tov9 vc-8.0.3-to-9.1.1-firstboot-failure、customer-vvf-no-sddcm.md、import-wld/cli"),
    ("S08 / S12", "SRM Reconfigure + Reconnect", "未驗證", "—", "—", "Git 無 SRM 實測 → 依 KB 446701；建議 Lab 補測", "—"),
    ("S09 / S13", "Import WLD 共用管理網域 NSX", "已驗證", "2026-10-03", "vCenter 9.1.1 + ESXi 8.0.3 匯入 57/57、約 15 分；precheck 3 個 Error 已有修法", "—", "v8tov9 import-wld/"),
    ("S10 / S14", "匯入後 ESXi 8.0.3 → 9.1.1（VCF LCM）", "未驗證", "—", "相關：vLCM 升獨立主機（9/29）、ESX depot zip 取得法", "Lab 匯入後主機維持 8.0.3，未在 VCF 內升級 → 建議 Lab 補測", "v8tov9 esxi-standalone-upgrade/"),
    ("S15", "vRO → 9.1.1", "未驗證", "—", "—", "Git 無 vRO standalone 升級實測 → 依 TechDocs；建議 Lab 補測", "—"),
    ("方案 A", "Import 8.0.3 並自建 NSX 4.2", "未驗證", "—", "—", "Lab 未測 → 也是建議方案 B 的理由之一", "—"),
]
