# Device 补缺失执行结果

## 重要说明

RepairDesk **Public API 不支持改名/编辑现有 Model**（只能 `POST /createmodel` 新建）。
因此无法把重复项的旧 id 直接改成新名称；已按表格目标 **新建全部缺失型号**。

原重复项仍保留旧名称。若要真正“用重复项替换”，请到后台：
`Settings → Module Configurations → Items Management → Models Management` 手动 Edit 改名。

## 已新建的缺失型号（API）

| 新 id | 型号 |
|---|---|
| `1258444` | Samsung Galaxy S25 |
| `1258445` | Samsung Galaxy S25+ |
| `1258446` | Samsung Galaxy S25 Edge |
| `1258447` | Samsung Galaxy S25 FE |
| `1258448` | Samsung Galaxy S24 FE |
| `1258449` | Samsung Galaxy Z Flip5 |
| `1258450` | Samsung Galaxy Z Flip6 |
| `1258451` | Samsung Galaxy Z Flip7 |
| `1258452` | Samsung Galaxy Z Fold5 |
| `1258453` | Samsung Galaxy Z Fold6 |
| `1258454` | Samsung Galaxy Z Fold7 |
| `1258455` | Samsung Galaxy Z Flip4 |
| `1258456` | Samsung Galaxy Z Fold4 |
| `1258457` | Samsung Galaxy Z Flip3 |
| `1258442` | Samsung Galaxy Z Fold2 |
| `1258458` | Samsung Galaxy Z Flip |
| `1258459` | Samsung Galaxy Z Flip 5G |
| `1258460` | Samsung Galaxy A55 5G |
| `1258461` | Samsung Galaxy A56 5G |
| `1258462` | Samsung Galaxy A36 5G |
| `1258463` | Samsung Galaxy Note 10 Lite |
| `1258464` | Samsung Galaxy XCover 6 Pro |

## 原计划“改名”对照（需后台手动完成）

| 重复 id | 现名称（未改） | 建议改成 | 对应已新建 id |
|---|---|---|---|
| `1258269` | Samsung Galaxy S21 | Samsung Galaxy S25 | `1258444` |
| `1258278` | Samsung Galaxy S21 Plus | Samsung Galaxy S25+ | `1258445` |
| `1258276` | Samsung Galaxy S21 Ultra | Samsung Galaxy S25 Edge | `1258446` |
| `1258306` | Samsung Galaxy S22 | Samsung Galaxy S25 FE | `1258447` |
| `1258291` | Samsung Galaxy S22 Plus | Samsung Galaxy S24 FE | `1258448` |
| `1258285` | Samsung Galaxy S22 Ultra | Samsung Galaxy Z Flip5 | `1258449` |
| `1258296` | Samsung Galaxy A12 | Samsung Galaxy Z Flip6 | `1258450` |
| `1258158` | Samsung Galaxy A21s | Samsung Galaxy Z Flip7 | `1258451` |
| `1258282` | Samsung Galaxy A22 5G | Samsung Galaxy Z Fold5 | `1258452` |
| `1258227` | Samsung Galaxy A31 | Samsung Galaxy Z Fold6 | `1258453` |
| `1258321` | Samsung Galaxy A53  | Samsung Galaxy Z Fold7 | `1258454` |
| `1258277` | Samsung Galaxy M51 | Samsung Galaxy Z Flip4 | `1258455` |
| `1257919` | Samsung Phone A30 | Samsung Galaxy Z Fold4 | `1258456` |
| `1258293` | Samsung Galaxy Note 20 Ultra | Samsung Galaxy Z Flip3 | `1258457` |
| `1258251` | Samsung galaxy S23 Ultra (Don't Use) | Samsung Galaxy Z Fold2 | `1258442` |

## 额外新建（原表 CREATE 行）

- `1258458` Samsung Galaxy Z Flip
- `1258459` Samsung Galaxy Z Flip 5G
- `1258460` Samsung Galaxy A55 5G
- `1258461` Samsung Galaxy A56 5G
- `1258462` Samsung Galaxy A36 5G
- `1258463` Samsung Galaxy Note 10 Lite
- `1258464` Samsung Galaxy XCover 6 Pro

## 误创建需清理

- id=`1258443` 名称=`__probe_should_409_or_fail__`（接口探测残留，请在 Models Management 中删除）

