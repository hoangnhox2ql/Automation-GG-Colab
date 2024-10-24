import requests

# Đường dẫn tới Google Colab notebook trên Google Drive (ID notebook)
colab_notebook_url = "https://colab.research.google.com/drive/1kkw4HgAP_BLAfOpxNoZj-RCaYt53jVpR#scrollTo=HpvR-ZG1D0Dv"

# Thực hiện request để chạy notebook
response = requests.post(colab_notebook_url + "/execute")

if response.status_code == 200:
    print("Notebook đã được chạy thành công!")
else:
