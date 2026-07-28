# 重复 Device 删除清单（需后台手动）

## API 限制

RepairDesk Public API **不支持删除 Model/Device**（已验证 `DELETE/POST deletemodel` 等均无效）。
删除只能在后台操作：

`Settings → Module Configurations → Items Management → Models Management` → 找到型号 → Delete

## 一、优先删除：表格中的 Samsung 重复项（15 个）

| id | 名称 | 说明 |
|---|---|---|
| `1258269` | Samsung Galaxy S21 | 重复槽，缺失型号已另建 |
| `1258278` | Samsung Galaxy S21 Plus | 重复槽，缺失型号已另建 |
| `1258276` | Samsung Galaxy S21 Ultra | 重复槽，缺失型号已另建 |
| `1258306` | Samsung Galaxy S22 | 重复槽，缺失型号已另建 |
| `1258291` | Samsung Galaxy S22 Plus | 重复槽，缺失型号已另建 |
| `1258285` | Samsung Galaxy S22 Ultra | 重复槽，缺失型号已另建 |
| `1258296` | Samsung Galaxy A12 | 重复槽，缺失型号已另建 |
| `1258158` | Samsung Galaxy A21s | 重复槽，缺失型号已另建 |
| `1258282` | Samsung Galaxy A22 5G | 重复槽，缺失型号已另建 |
| `1258227` | Samsung Galaxy A31 | 重复槽，缺失型号已另建 |
| `1258321` | Samsung Galaxy A53  | 重复槽，缺失型号已另建 |
| `1258277` | Samsung Galaxy M51 | 重复槽，缺失型号已另建 |
| `1257919` | Samsung Phone A30 | 重复槽，缺失型号已另建 |
| `1258293` | Samsung Galaxy Note 20 Ultra | 重复槽，缺失型号已另建 |
| `1258251` | Samsung galaxy S23 Ultra (Don't Use) | 重复槽，缺失型号已另建 |

## 二、建议一并删除：Apple 重复 / Don’t use / 占位（9 个）

| id | 名称 |
|---|---|
| `1258270` | Apple IPhone 12 Mini |
| `1258316` | Apple IPhone 13 Mini  |
| `1258297` | Apple IPhone 13 Pro |
| `1258338` | iPhone 13/14 |
| `1258339` | iPhone 13 / 14 |
| `1258175` | Apple iPhone 14 (Don't use) |
| `1258176` | Apple iPhone 14 Plus (Don't use) |
| `1258177` | Apple iPhone 14 Pro (Don't use) |
| `1258315` | Apple iPhone 14 Pro Max (Don't use) |

## 三、必须删除：API 探测残留（2 个）

| id | 名称 |
|---|---|
| `1258443` | __probe_should_409_or_fail__ |
| `1258465` | __deleted__ |

## 四、完整 MERGE_OR_DELETE 列表（含跨品牌）

共 59 条，见 `data/duplicate-devices.csv` 中 `action=MERGE_OR_DELETE`。

### 快速复制（优先 15+9+2）

```
1258269	Samsung Galaxy S21
1258278	Samsung Galaxy S21 Plus
1258276	Samsung Galaxy S21 Ultra
1258306	Samsung Galaxy S22
1258291	Samsung Galaxy S22 Plus
1258285	Samsung Galaxy S22 Ultra
1258296	Samsung Galaxy A12
1258158	Samsung Galaxy A21s
1258282	Samsung Galaxy A22 5G
1258227	Samsung Galaxy A31
1258321	Samsung Galaxy A53 
1258277	Samsung Galaxy M51
1257919	Samsung Phone A30
1258293	Samsung Galaxy Note 20 Ultra
1258251	Samsung galaxy S23 Ultra (Don't Use)
1258270	Apple IPhone 12 Mini
1258316	Apple IPhone 13 Mini 
1258297	Apple IPhone 13 Pro
1258338	iPhone 13/14
1258339	iPhone 13 / 14
1258175	Apple iPhone 14 (Don't use)
1258176	Apple iPhone 14 Plus (Don't use)
1258177	Apple iPhone 14 Pro (Don't use)
1258315	Apple iPhone 14 Pro Max (Don't use)
1258443	__probe_should_409_or_fail__
1258465	__deleted__
```

