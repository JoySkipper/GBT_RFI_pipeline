from bs4 import BeautifulSoup
import pandas as pd

"""

soup = BeautifulSoup(open("/users/jskipper/public_html/rfi.html"),'html.parser')


table = soup.find_all('table')[0]
#print(table)
#print(soup.prettify())
new_table = pd.DataFrame(columns=range(1,6), index = [0])

GBT_receiver_locations = { 
    'Rcvr_342':{'row':0,'column': 0},
    'Rcvr_450':{'row': 0,'column': 1},
    'Rcvr_600':{'row': 1,'column': 0},
    'Rcvr_800':{'row': 1,'column': 1},
    'Prime Focus 2': {'row': 2,'column': 0},
    'Rcvr1_2':{'row': 2,'column': 1},
    'Rcvr2_3':{'row': 3,'column': 0},
    'Rcvr4_8':{'row': 3,'column': 1},
    'Rcvr8_10':{'row': 4,'column': 0},
    'Rcvr12_18':{'row': 4,'column': 1},
    'RcvrArray19_26':{'row': 5,'column': 0},
    'Rcvr26_40':{'row': 5,'column': 1},
    'Rcvr40_52':{'row': 6,'column': 0},
    'Rcvr68_92':{'row': 6,'column': 1},
}

receiver = "Rcvr_342"
row_value = GBT_receiver_locations[receiver]['row']
column_value = GBT_receiver_locations[receiver]['column']

row_counter = 0
for row in table.find_all('tr'):
    if row_value == row_counter: 
        column_counter = 0
        for column in row.find_all('td'):
            if column_counter == column_value:
                for entry in column.findChildren("option"):
                    
                    print(entry)
                    #entry.replace_with(', <option value=\"http://www.gb.nrao.edu/IPG/rfiarchive_files/GBTDataImages/GBTRFI11_21_17_3.html\">11_21_17</option>, ')
                    #print(entry)   
                    break
            column_counter += 1

        #print(columns[column_value])
    row_counter += 1

"""

with open("/users/jskipper/public_html/rfi.html","rw") as f:
    print(f.read())
