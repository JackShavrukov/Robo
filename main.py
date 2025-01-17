import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
import os.path
from os import path

def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.insert(0, "Ticker", ticker)
    return data

def open_ticker_file(ticker): #Function for open or create DataFrame for Ticker
    if not path.exists(ticker+'.csv'): # If not file
        df = yf.download(ticker) # Read data from Yahoo
        df.to_csv(ticker+'.csv') # Write data to file
        print('Create new file for '+ticker) # Info
    print('File for '+ticker+' is present!') #Info
    return pd.read_csv(ticker+'.csv')

def open_tickers_list(tickerslist): # Funtion create or open Tickers list
    if not path.exists(tickerslist):  # Create file - Tickers.csv
        df_baset = pd.DataFrame({'Ticker': ['GOOG', 'MSFT']})  # Create DataFrame with basic Tickers
        df_baset.to_csv(tickerslist)  # Create File - Tickers.csv with basic tickers
    return pd.read_csv(tickerslist)  # Read file Tickers to DataFrame

# Start Main Block
df_tickers = open_tickers_list("Tickers.csv") # Open tickers list
for i in range(0, df_tickers.shape[0]): # Selecting tickers one by one
    current_ticker = df_tickers.loc[i, 'Ticker'] # Select current ticker
    print(i,' = ', current_ticker) #Info
    df_curr_tick = open_ticker_file(current_ticker) # Open DataFrame for current Ticker
    print(df_curr_tick) #Info



start = datetime.date(2024, 7, 5).strftime('%Y-%m-%d')
end = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

print(start)
print(end)

#df = get_stock_data("BAC", start, end)

#print(df.tail(200))
#df.to_csv("Ticker Info.csv")

df = yf.download('BAC',start, end)
del df['Volume']

print(df.tail(200))
df.to_csv("Ticker Info.csv")

# df['Adj Close'].plot()
# plt.show()

# df.info()

'''

start_time = time.time() #Fixing start time

df_pat = pd.DataFrame({'Cnt_point': [0], 'Vector_after': [0]})

df = pd.read_csv("VOO.csv") #Read file to DataFrame
df['Date'] = pd.to_datetime(df.Date, format = '%d.%m.%Y %H:%M:%S')

count_rec = df.shape[0]

for i in range(0, count_rec):
    df.loc[i, 'Close'] = df.loc[i, 'Close'].replace(",",".")
df['Close'] = pd.to_numeric(df.Close)


df["Vector"] = 0.00 # Создаем столбец Vector и заполняем его 0
df["Pattern"] = 0 # Создаем столбец для фиксации паттернов с кол-вом точек

for i in range(1, df.shape[0]): # Заполняем столбец Vector со значением раста-падения индекса в текущей дате
    df.loc[i, 'Vector'] = round((((df.loc[i, 'Close'] * 100) / df.loc[i-1, 'Close']) - 100), 4)

count_point = 5 # Стартовое кол-во точек в паттерне
count_pat = -1 # Счетчик кол-ва паттернов в выборке
start_exampl = count_rec - count_point #начальный индекс искомого паттерна
start_point = 0 #начальный индекс отсчета для поиска паттернов в массиве
vectors_up = 0 # Счетчик положительных векторов после окончания паттерна
vectors_down = 0 # Счетчик отрицательных векторов после окончания паттерна
global_count_pat = 0
sum_vectors_up = 0
sum_vectors_down = 0

while count_pat != 0: # Увеличиваем на 1 кол-во точек в паттерне до тех пор, пока кол-во паттернов в массиве не станер равно 0
    count_pat = 0
    for start_point in range(count_rec - count_point): #Двигаемся от начала массива к концу
        pattern = True # Установка признака что паттерн найден
        for n in range(count_point): # Проверка совпадения 1 паттерна от текущей точки с эталонным паттерном
            if df.loc[start_exampl+n, 'Vector'] > 0 and df.loc[start_point+n, 'Vector'] > 0:
                pass
            elif df.loc[start_exampl+n, 'Vector'] == 0 and df.loc[start_point+n, 'Vector'] == 0:
                pass
            elif df.loc[start_exampl+n, 'Vector'] < 0 and df.loc[start_point+n, 'Vector'] < 0:
                pass
            else:
                pattern = False
        if pattern: # Если найден паттерн
            count_pat += 1 # увеличиваем счетчик найденных паттернов на 1
            df.loc[start_point + count_point - 1, 'Pattern'] = count_point # Фиксируем наличие паттерна в массиве в поле Pattern
    count_point += 1
    start_exampl = count_rec - count_point
    start_point = 0

for i in range(count_rec - 1): #Выбираем все паттерны в отдельный Датафрейм
    if df.loc[i, 'Pattern'] > 0:
        df_pat.loc[ len(df_pat.index)] = [ df.loc[i, 'Pattern'], df.loc[i + 1, 'Vector']]


count_pat = -1
count_point = 5

while global_count_pat != df_pat.shape[0] -1 : # Группируем инфо по паттернам из Датафрейма
    count_pat = 0
    for i in range(df_pat.shape[0]):
        if df_pat.loc[i, 'Cnt_point'] == count_point and df_pat.loc[i, 'Vector_after'] > 0 :
            vectors_up +=1
            count_pat +=1
            global_count_pat +=1
        elif df_pat.loc[i, 'Cnt_point'] == count_point and df_pat.loc[i, 'Vector_after'] < 0 :
            vectors_down += 1
            count_pat += 1
            global_count_pat += 1
        elif df_pat.loc[i, 'Cnt_point'] == count_point and df_pat.loc[i, 'Vector_after'] == 0 :
            count_pat += 1
            global_count_pat += 1
    print("Для ", count_point, "точек, найдено ", count_pat, " уникальных паттернов. Рост был в ", vectors_up, "случаях. Падение в ", vectors_down, "случаях.")
    count_point +=1
    sum_vectors_up +=vectors_up
    sum_vectors_down +=vectors_down
    vectors_up = 0
    vectors_down = 0

print("Найденно уникальных паттернов:", global_count_pat, ". Прогноз роста - ", sum_vectors_up, ". Прогноз падения - ", sum_vectors_down, ".")
print("Прогноз роста = ", round((sum_vectors_up / global_count_pat)*100,2), "%.", "Прогноз падения = ", round((sum_vectors_down/global_count_pat)*100,2), "%.")

# df_pat.to_csv("Patterns.csv")

# print(df.tail(60))

# Визуализация графика
plt.bar(df_pat.index, df_pat['Vector_after'])
plt.show()

# df1.info()

print("")
print ("Time elapsed: {:.2f}s".format(time.time() - start_time)) # How long script worked in second
df.to_csv("Res.csv")

'''
