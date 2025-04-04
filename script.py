pip install yfinance pandas tabulate gspread google-auth google-auth-oauthlib google-auth-httplib2
import yfinance as  yf
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.colab import auth
from oauth2client.service_account import ServiceAccountCredentials

#salin file credentials ke colab
from google.colab import drive
import shutil
# Mount Google Drive
drive.mount('/content/drive')

# Path ke file di Google Drive
drive_path = "/content/drive/My Drive/colab/credentials.json"
local_path = "/content/credentials.json"

# Salin file ke Colab
shutil.copy(drive_path, local_path)

# 🔹 Autentikasi Google Colab ke Google Drive
auth.authenticate_user()

# 🔹 Load credentials dari file JSON
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)

# 🔹 Buka Google Sheets (Ganti dengan nama Sheet Anda)
spreadsheet = gc.open("datayfinance") #nama sheet
worksheet = spreadsheet.worksheet("tabelincome") #nama worksheet

# 🔹 Daftar saham Indonesia di Yahoo Finance
tickers = ["AMRT.JK", "ITMG.JK", "ADRO.JK", "ASII.JK", "BBCA.JK", "LSIP.JK", "LPPF.JK","MNCN.JK", "ADHI.JK"]

# 🔹 Ambil Data Keuangan
data_list = []
for ticker in tickers:
    stock = yf.Ticker(ticker)
    financials = stock.financials  # Laporan keuangan

    if financials.empty:
        print(f"Tidak bisa mengambil data untuk {ticker}")
        continue

    # Ambil 2 tahun terakhir
    years = list(financials.columns)
    if len(years) < 2:
        print(f"Data kurang dari 2 tahun untuk {ticker}")
        continue

    current_year = years[0].year
    previous_year = years[1].year

    revenue_current = financials.loc["Total Revenue", years[0]] if "Total Revenue" in financials.index else "N/A"
    revenue_previous = financials.loc["Total Revenue", years[1]] if "Total Revenue" in financials.index else "N/A"
    net_income_current = financials.loc["Net Income", years[0]] if "Net Income" in financials.index else "N/A"
    net_income_previous = financials.loc["Net Income", years[1]] if "Net Income" in financials.index else "N/A"

    data_list.append([ticker, revenue_previous, revenue_current, net_income_previous, net_income_current])

# 🔹 Buat DataFrame
df = pd.DataFrame(data_list, columns=["Ticker", "Revenue Previous Year", "Revenue Current Year",
                                      "Net Income Previous Year", "Net Income Current Year"])

# 🔹 Simpan ke Google Sheets
#worksheet.clear()  # Hapus data lama
#set_with_dataframe(worksheet, df)

print(df)
