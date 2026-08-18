# RepairDesk 重复 Device 清单（单独列出）

- 总设备数：**702**
- 完全重复分组：**17**（涉及 34 条）
- 近似重复分组：**29**（涉及 61 条）
- 说明：API **不能删除/改名** device；请在 RepairDesk → Settings → Models Management 手动处理
- 建议：每组保留 **建议保留**，其余合并/删除（删除前确认工单未引用该 id）
- 完整列表：`data/devices-full.csv`

## 一、完全重复（优先清理）

同品牌 + 同名（忽略大小写/首尾空格）。

### Apple iPhone 12 Mini  （2 条｜品牌: Apple）
- **建议保留** id=`1258069` \| `Apple iPhone 12 Mini` \| `Apple` \| sort=`41`
- 建议合并/删除 id=`1258270` \| `Apple IPhone 12 Mini` \| `Apple` \| sort=`0`

### Apple iPhone 13 Mini  （2 条｜品牌: Apple）
- **建议保留** id=`1258110` \| `Apple iPhone 13 Mini` \| `Apple` \| sort=`45`
- 建议合并/删除 id=`1258316` \| `Apple IPhone 13 Mini ` \| `Apple` \| sort=`0`

### Apple iPhone 13 Pro  （2 条｜品牌: Apple）
- **建议保留** id=`1258109` \| `Apple iPhone 13 Pro` \| `Apple` \| sort=`46`
- 建议合并/删除 id=`1258297` \| `Apple IPhone 13 Pro` \| `Apple` \| sort=`0`

### Samsung  Chromebook  （2 条｜品牌: Samsung）
- **建议保留** id=`1258103` \| `Samsung  Chromebook` \| `Samsung` \| sort=`2`
- 建议合并/删除 id=`1258425` \| `Samsung Chromebook` \| `Samsung` \| sort=`0`

### Samsung Galaxy A12  （2 条｜品牌: Samsung）
- **建议保留** id=`1258087` \| `Samsung Galaxy A12` \| `Samsung` \| sort=`23`
- 建议合并/删除 id=`1258296` \| `Samsung Galaxy A12` \| `Samsung` \| sort=`0`

### Samsung Galaxy A21S  （2 条｜品牌: Samsung）
- **建议保留** id=`1258045` \| `Samsung Galaxy A21S` \| `Samsung` \| sort=`5`
- 建议合并/删除 id=`1258158` \| `Samsung Galaxy A21s` \| `Samsung` \| sort=`0`

### Samsung Galaxy A22 5G  （2 条｜品牌: Samsung）
- **建议保留** id=`1258142` \| `Samsung Galaxy A22 5G` \| `Samsung` \| sort=`26`
- 建议合并/删除 id=`1258282` \| `Samsung Galaxy A22 5G` \| `Samsung` \| sort=`0`

### Samsung Galaxy A31  （2 条｜品牌: Samsung）
- **建议保留** id=`1258212` \| `Samsung Galaxy A31` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258227` \| `Samsung Galaxy A31` \| `Samsung` \| sort=`0`

### Samsung Galaxy A53  （2 条｜品牌: Samsung）
- **建议保留** id=`1258173` \| `Samsung Galaxy A53` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258321` \| `Samsung Galaxy A53 ` \| `Samsung` \| sort=`0`

### Samsung Galaxy M51  （2 条｜品牌: Samsung）
- **建议保留** id=`1258161` \| `Samsung Galaxy M51` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258277` \| `Samsung Galaxy M51` \| `Samsung` \| sort=`0`

### Samsung Galaxy S21  （2 条｜品牌: Samsung）
- **建议保留** id=`1258083` \| `Samsung Galaxy S21` \| `Samsung` \| sort=`45`
- 建议合并/删除 id=`1258269` \| `Samsung Galaxy S21` \| `Samsung` \| sort=`0`

### Samsung Galaxy S21 Plus  （2 条｜品牌: Samsung）
- **建议保留** id=`1258085` \| `Samsung Galaxy S21 Plus` \| `Samsung` \| sort=`46`
- 建议合并/删除 id=`1258278` \| `Samsung Galaxy S21 Plus` \| `Samsung` \| sort=`0`

### Samsung Galaxy S21 Ultra  （2 条｜品牌: Samsung）
- **建议保留** id=`1258084` \| `Samsung Galaxy S21 Ultra` \| `Samsung` \| sort=`47`
- 建议合并/删除 id=`1258276` \| `Samsung Galaxy S21 Ultra` \| `Samsung` \| sort=`0`

### Samsung Galaxy S22  （2 条｜品牌: Samsung）
- **建议保留** id=`1258165` \| `Samsung Galaxy S22` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258306` \| `Samsung Galaxy S22` \| `Samsung` \| sort=`0`

### Samsung Galaxy S22 Plus  （2 条｜品牌: Samsung）
- **建议保留** id=`1258166` \| `Samsung Galaxy S22 Plus` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258291` \| `Samsung Galaxy S22 Plus` \| `Samsung` \| sort=`0`

### Samsung Galaxy S22 Ultra  （2 条｜品牌: Samsung）
- **建议保留** id=`1258162` \| `Samsung Galaxy S22 Ultra` \| `Samsung` \| sort=`0`
- 建议合并/删除 id=`1258285` \| `Samsung Galaxy S22 Ultra` \| `Samsung` \| sort=`0`

### Samsung Phone A30  （2 条｜品牌: Samsung）
- **建议保留** id=`1257953` \| `Samsung Phone A30` \| `Samsung` \| sort=`87`
- 建议合并/删除 id=`1257919` \| `Samsung Phone A30` \| `Samsung` \| sort=`86`

## 二、近似重复（命名风格不同，机型应相同）

例如 `Samsung A20` vs `Samsung Galaxy A20`，`iPad Mini 4` vs `Apple iPad Mini 4`。**4G/5G 不同版本不会并在一起。**

### iPad Mini 4  （2 条｜品牌: Apple）
- **建议保留** id=`1257990` \| `iPad Mini 4` \| `Apple` \| sort=`75`
- 建议核对后合并/删除 id=`1257992` \| `Apple iPad Mini 4` \| `Apple` \| sort=`29`

### Apple iPhone SE  （2 条｜品牌: Apple）
- **建议保留** id=`1251874` \| `Apple iPhone SE` \| `Apple` \| sort=`62`
- 建议核对后合并/删除 id=`1258242` \| `iphone SE` \| `Apple` \| sort=`0`

### laptop  （2 条｜品牌: Asus）
- **建议保留** id=`1257885` \| `laptop` \| `Asus` \| sort=`3`
- 建议核对后合并/删除 id=`1257900` \| `Asus Laptop` \| `Asus` \| sort=`2`

### Huawei Phone P10 Lite  （2 条｜品牌: Huawei）
- **建议保留** id=`1257951` \| `Huawei Phone P10 Lite` \| `Huawei` \| sort=`23`
- 建议核对后合并/删除 id=`1257950` \| `Huawei P10 Lite` \| `Huawei` \| sort=`6`

### Oppo A5  （2 条｜品牌: Oppo）
- **建议保留** id=`1258039` \| `Oppo A5 ` \| `Oppo` \| sort=`1`
- 建议核对后合并/删除 id=`1258412` \| `A5` \| `Oppo` \| sort=`0`

### Oppo Phone A52  （2 条｜品牌: Oppo）
- **建议保留** id=`1258172` \| `Oppo Phone A52` \| `Oppo` \| sort=`0`
- 建议核对后合并/删除 id=`1258390` \| `OPPO A52` \| `Oppo` \| sort=`0`

### Oppo Phone A54 5G  （2 条｜品牌: Oppo）
- **建议保留** id=`1258171` \| `Oppo Phone A54 5G` \| `Oppo` \| sort=`0`
- 建议核对后合并/删除 id=`1258309` \| `A54 5G` \| `Oppo` \| sort=`0`

### Phone Find X5 Pro  （2 条｜品牌: Oppo）
- **建议保留** id=`1258174` \| `Phone Find X5 Pro` \| `Oppo` \| sort=`0`
- 建议核对后合并/删除 id=`1258308` \| `Oppo Find X5 Pro` \| `Oppo` \| sort=`0`

### Samsung Phone A11  （2 条｜品牌: Samsung）
- **建议保留** id=`1257976` \| `Samsung Phone A11` \| `Samsung` \| sort=`84`
- 建议核对后合并/删除 id=`1258121` \| `Samsung Galaxy A11` \| `Samsung` \| sort=`22`

### Samsung Phone A20  （3 条｜品牌: Samsung）
- **建议保留** id=`1257952` \| `Samsung Phone A20` \| `Samsung` \| sort=`85`
- 建议核对后合并/删除 id=`1257936` \| `Samsung A20` \| `Samsung` \| sort=`4`
- 建议核对后合并/删除 id=`1258157` \| `Samsung Galaxy A20` \| `Samsung` \| sort=`0`

### Samsung Phone A30  （3 条｜品牌: Samsung）
- **建议保留** id=`1257953` \| `Samsung Phone A30` \| `Samsung` \| sort=`87`
- 建议核对后合并/删除 id=`1257919` \| `Samsung Phone A30` \| `Samsung` \| sort=`86`
- 建议核对后合并/删除 id=`1258122` \| `Samsung Galaxy A30` \| `Samsung` \| sort=`27`

### a35  （2 条｜品牌: Samsung）
- **建议保留** id=`1258410` \| `a35` \| `Samsung` \| sort=`0`
- 建议核对后合并/删除 id=`1258411` \| `Samsung A35` \| `Samsung` \| sort=`0`

### Samsung Phone A50  （2 条｜品牌: Samsung）
- **建议保留** id=`1257955` \| `Samsung Phone A50` \| `Samsung` \| sort=`91`
- 建议核对后合并/删除 id=`1258155` \| `Samsung Galaxy A50` \| `Samsung` \| sort=`0`

### Samsung Tablet A7  （2 条｜品牌: Samsung）
- **建议保留** id=`1258245` \| `Samsung Tablet A7` \| `Samsung` \| sort=`0`
- 建议核对后合并/删除 id=`1258244` \| `Tablet A7 ` \| `Samsung` \| sort=`0`

### Samsung Phone A70  （2 条｜品牌: Samsung）
- **建议保留** id=`1257956` \| `Samsung Phone A70` \| `Samsung` \| sort=`94`
- 建议核对后合并/删除 id=`1258233` \| `Samsung Galaxy A70` \| `Samsung` \| sort=`0`

### Samsung Phone A8 A530  （2 条｜品牌: Samsung）
- **建议保留** id=`1251847` \| `Samsung Phone A8 A530` \| `Samsung` \| sort=`96`
- 建议核对后合并/删除 id=`1250933` \| `Samsung A8 A530` \| `Samsung` \| sort=`15`

### Samsung Phone A8 Plus A730  （2 条｜品牌: Samsung）
- **建议保留** id=`1251846` \| `Samsung Phone A8 Plus A730` \| `Samsung` \| sort=`97`
- 建议核对后合并/删除 id=`1250934` \| `Samsung A8 Plus A730` \| `Samsung` \| sort=`16`

### Samsung Phone J5 Prime (G570)  （2 条｜品牌: Samsung）
- **建议保留** id=`1251843` \| `Samsung Phone J5 Prime (G570)` \| `Samsung` \| sort=`99`
- 建议核对后合并/删除 id=`1250954` \| `Samsung J5 Prime G570` \| `Samsung` \| sort=`70`

### Samsung Phone J7 Prime (G610)  （2 条｜品牌: Samsung）
- **建议保留** id=`1251841` \| `Samsung Phone J7 Prime (G610)` \| `Samsung` \| sort=`102`
- 建议核对后合并/删除 id=`1250959` \| `Samsung J7 Prime G610` \| `Samsung` \| sort=`74`

### Samsung Phone J7 Pro J730  （2 条｜品牌: Samsung）
- **建议保留** id=`1251840` \| `Samsung Phone J7 Pro J730` \| `Samsung` \| sort=`103`
- 建议核对后合并/删除 id=`1250960` \| `Samsung J7 Pro J730` \| `Samsung` \| sort=`75`

### Samsung Note10  （2 条｜品牌: Samsung）
- **建议保留** id=`1257972` \| `Samsung Note10` \| `Samsung` \| sort=`79`
- 建议核对后合并/删除 id=`1258163` \| `Samsung Galaxy Note10` \| `Samsung` \| sort=`0`

### Samsung Note10 Plus  （2 条｜品牌: Samsung）
- **建议保留** id=`1258029` \| `Samsung Note10 Plus` \| `Samsung` \| sort=`80`
- 建议核对后合并/删除 id=`1258164` \| `Samsung Galaxy Note10 Plus` \| `Samsung` \| sort=`0`

### Samsung Note20 Ultra  （2 条｜品牌: Samsung）
- **建议保留** id=`1258106` \| `Samsung Note20 Ultra` \| `Samsung` \| sort=`81`
- 建议核对后合并/删除 id=`1258124` \| `Samsung Galaxy Note20 Ultra` \| `Samsung` \| sort=`40`

### Samsung Phone Note8  （2 条｜品牌: Samsung）
- **建议保留** id=`1251853` \| `Samsung Phone Note8` \| `Samsung` \| sort=`109`
- 建议核对后合并/删除 id=`1250855` \| `Samsung Note8` \| `Samsung` \| sort=`83`

### Samsung Phone S10  （2 条｜品牌: Samsung）
- **建议保留** id=`1257916` \| `Samsung Phone S10` \| `Samsung` \| sort=`111`
- 建议核对后合并/删除 id=`1258252` \| `Samsung Galaxy s10 ` \| `Samsung` \| sort=`0`

### Samsung Phone S10 Plus  （2 条｜品牌: Samsung）
- **建议保留** id=`1257917` \| `Samsung Phone S10 Plus` \| `Samsung` \| sort=`112`
- 建议核对后合并/删除 id=`1258224` \| `Samsung Galaxy S10 plus` \| `Samsung` \| sort=`0`

### Samsung Galaxy S20  （2 条｜品牌: Samsung）
- **建议保留** id=`1258047` \| `Samsung Galaxy S20 ` \| `Samsung` \| sort=`41`
- 建议核对后合并/删除 id=`1258287` \| `Samsung S20` \| `Samsung` \| sort=`0`

### Samsung Galaxy S22 Ultra  （3 条｜品牌: Samsung）
- **建议保留** id=`1258162` \| `Samsung Galaxy S22 Ultra` \| `Samsung` \| sort=`0`
- 建议核对后合并/删除 id=`1258285` \| `Samsung Galaxy S22 Ultra` \| `Samsung` \| sort=`0`
- 建议核对后合并/删除 id=`1258337` \| `Samsung S22 Ultra` \| `Samsung` \| sort=`0`

### Samsung Phone S7  （2 条｜品牌: Samsung）
- **建议保留** id=`1251861` \| `Samsung Phone S7` \| `Samsung` \| sort=`119`
- 建议核对后合并/删除 id=`1258261` \| `Samsung Galaxy S7 ` \| `Samsung` \| sort=`0`

## 三、疑似垃圾模型（建议删除）

- 建议删除 id=`1258443` \| `__probe_should_409_or_fail__` \| `Samsung`
- 建议删除 id=`1258465` \| `__deleted__` \| `Samsung`

## 四、完全重复 — 建议删除条数（按品牌）

| 品牌 | 可删条数 |
|---|---|
| samsung | 14 |
| apple | 3 |
