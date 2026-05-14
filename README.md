
# Quiz 3

## Demo
![alt text](example.gif)

## 執行方式

### 方法一: 開啟執行檔
* 直接下載並開啟 <a href="crawler.exe"> crawler.exe</a>
* 環境須為Windows且須有Chrome瀏覽器

### 方法二: 執行python檔
* 需有python，並安裝以下套件:
```
pip install selenium
pip install webdriver_manager
```
* 執行
```
cd main
python crawler.py
```

## Tools
* BeautifulSoup: 解析靜態網頁，爬輸入選項
* selenium: 動態操作網頁，自動化輸入表單測試

## Steps
### Step 1: 觀察網頁結構

#### 表單
* 找出需要輸入的欄位及其element供後面自動化輸入用
* 欄位說明如下

| 表單輸入欄位 | 變數名 |  格式/範圍 | Element |
| :---: | :---: | :---: | :---:|
| 保險對象(幫誰保險) | peopleTab | 包含 "多人一起保、幫自己保、幫他人保"選項，分別對應為 1,2,3  |.people_tab_accu+編號|
| 旅遊國家 | travelCountry | 字串，網頁上包含的國家，最多10個| input.ti-valid.ti-new-tag-input|
| 投保人數與年齡 | peopleCount | 保險人數，包含多個類別年齡層，總數1-4人 | input.clarity-unmask -> img[src='/ec/travel/overseas/img/plus.f343272d.svg']|
| 出發日 | startDate | YYYY-MM-DD，近60天內 | div.startDate input|
| 返回日 | endDate |  YYYY-MM-DD，出發日開始180天內 | div.endDate input|
| 時間 | time |每小時，00:00 - 23:00 | #timeSelect -> [value='"+時間+"']|

#### 按鈕

| 功能 | Element |
| :---: | :---: |
|保險對象確認|.people_confirm_accu+編號|
|試算保費，提交表單資料|.count1_go_accu|
|保期確認|.date_confirm_accu|
|投保審核確認|.swal2-confirm|
### Step 2: 爬取國家選項
* 以 <a href="/main/get_country_list.py"> get_country_list</a> 取得所有國家名
* 詳見<a href="/data/country.txt"> country.txt</a> 


### Step 3: 生成假資料
* 以 <a href="/main/generate_random_data.py"> generate_random_data</a> 隨機產生資料
* 範例: <a href="/data/test.json">test.json</a>
```
{
	"people_tab": "1",
	"startDate": "2026-06-01",
	"endDate": "2026-07-01",
	"time": "08:00",
	"peopleCount": [
		{
			"elderCount": 1,
			"adultCount": 1,
			"youthCount": 2,
			"childCount": 0,
			"babyCount": 0
		}
	],
	"travelCountry": [
		"波多黎各",
		"卡達",
		"荷屬安地列斯",
		"布吉納法索",
		"獅子山",
		"塞席爾"
	]
}
```

### Step 4: 加上自動化操作
* 加上對DOM物件的操作: 
	* 定位: find_element()
	* 動作指令: click(), send_keys()
	* 執行JS: execute_script()
* 加入等待網頁/DOM物件loading的時間: sleep(5), WebDriverWait(driver, 10,1).until()