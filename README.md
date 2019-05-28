# ClickCrop
>### This project is written by Python2.7
>### 研究動機
>帳號密碼竊取的手法有很多種，例如中間人攻擊進行側錄、網站釣魚，甚至是讓使用者在不知情的情況下點擊木馬病毒。但由於這些程式或網頁只侷限在特定的範圍中，因此我們想設計一款利用木馬病毒，可以自動去比對圖片及文字檔後產生出帳號密碼的程式。
>### 架構
>在螢幕截圖中，一旦使用者打開chrome之後便會開始截圖，我們只擷取點擊的200*100的畫面，優點是可以將不必要的資訊進行過濾，此外檔案大小也會影響到文字辨識的速度，而在鍵盤側錄的方面將使用者所按的鍵皆存入文字檔中。接者使用文字辨識系統，將圖片上傳至google會回傳辨識後的文字檔，我們對文字檔做正規表示法的分析，將帳號分析出來。最後將帳號格式丟進鍵盤側錄的文字檔分析出帳號密碼。
>### 函式庫
> - pyHook
> - win32api
> - PIL (Python Imaging Library)
> - Google Vision API
>### 使用說明
>為了使用GOOGLE OCR API，必須到[Goole Vision API](https://cloud.google.com/vision/?hl=zh-tw&utm_source=google&utm_medium=cpc&utm_campaign=japac-TW-all-zh-dr-bkws-all-super-trial-e-dr-1003987&utm_content=text-ad-none-none-DEV_c-CRE_263273745766-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+~+T1+%7C+EXA+%7C+ML+%7C+1:1+%7C+TW+%7C+zh+%7C+Vision+%7C+google+ocr+%7C+en-KWID_43700031887751276-kwd-12194465573&userloc_1012812&utm_term=KW_google%20ocr&gclid=Cj0KCQjwla7nBRDxARIsADll0kAm087UVe67FWVgCUH8KLXFvuuQBelGzPyUg6igvACKyq61bz6zlHMaAi4DEALw_wcB)進行註冊，取得專屬的json檔案之後才可使用。