import os; import time; import selenium; from selenium import webdriver
from selenium.webdriver.common.by import By; from selenium.webdriver import Keys
from selenium.webdriver import ActionChains; import keyboard; import re
import json; from tabulate import tabulate

def init():
    global RefreshDelay, username, password, CoreOverheatTemp, CoreOverheat, VRMOverheatTemp, VRMOverheat, driver, k1poolaccountpage 
    global k1pool3hrhr1, k1pool3hrhr2, k1pool3hrhr3, k1pool3hrhr4, k1pool3hrhr5, k1pool3hrhr6
    global k1online1, k1online2, k1online3, k1online4, k1online5, k1online6
    print('Initilizing WebDriver, Please Wait...')
    driver = webdriver.Firefox(); driver.minimize_window()
    RefreshDelay = 300 # Seconds of delay before refreshing values
    username='admin'; password='12345678' # Asic Machines login (all have to be the same)
    CoreOverheatTemp = 60
    CoreOverheat = 68
    VRMOverheatTemp = 100
    VRMOverheat = 95

    #Im using k1 pool, so this ports into my address, and reads out my individule miners ACCTUAL @ pool hashrate
    k1poolaccountpage = 'https://k1pool.com/pool/kaspa/account/KrMAsyjkMVamRzLWiBamifKMFvQ5unG2Ssz'
    k1pool3hrhr1 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[1]/td[3]'
    k1pool3hrhr2 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[2]/td[3]'
    k1pool3hrhr3 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[3]/td[3]'
    k1pool3hrhr4 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[4]/td[3]'
    k1pool3hrhr5 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[5]/td[3]'
    k1pool3hrhr6 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[6]/td[3]'
    k1online1 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[1]/td[4]'
    k1online2 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]'
    k1online3 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[3]/td[4]'
    k1online4 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[4]/td[4]'
    k1online5 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[5]/td[4]'
    k1online6 = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[6]/td[4]'


def coretemp1():
    global corehigh1, corelow1, coreavg1
    url = 'http://10.0.0.1/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh1 = max(values)
    corelow1 = min(values)
    avg = sum(values) / len(values)
    coreavg1 = round(avg, 2)
    print("1. Chip Temps (high,low,avg): ", corehigh1, corelow1, coreavg1)
def coretemp2():
    global corehigh2, corelow2, coreavg2
    url = 'http://10.0.0.2/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh2 = max(values)
    corelow2 = min(values)
    avg = sum(values) / len(values)
    coreavg2 = round(avg, 2)
    print("2. Chip Temps (high,low,avg): ", corehigh2, corelow2, coreavg2)
def coretemp3():
    global corehigh3, corelow3, coreavg3
    url = 'http://10.0.0.3/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh3 = max(values)
    corelow3 = min(values)
    avg = sum(values) / len(values)
    coreavg3 = round(avg, 2)
    print("3. Chip Temps (high,low,avg): ", corehigh3, corelow3, coreavg3)
def coretemp4():
    global corehigh4, corelow4, coreavg4
    url = 'http://10.0.0.4/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh4 = max(values)
    corelow4 = min(values)
    avg = sum(values) / len(values)
    coreavg4 = round(avg, 2)
    print("4. Chip Temps (high,low,avg): ", corehigh4, corelow4, coreavg4)
def coretemp5():
    global corehigh5, corelow5, coreavg5
    url = 'http://10.0.0.5/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh5 = max(values)
    corelow5 = min(values)
    avg = sum(values) / len(values)
    coreavg5 = round(avg, 2)
    print("5. Chip Temps (high,low,avg): ", corehigh5, corelow5, coreavg5)
def coretemp6():
    global corehigh6, corelow6, coreavg6
    url = 'http://10.0.0.6/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh6 = max(values)
    corelow6 = min(values)
    avg = sum(values) / len(values)
    coreavg6 = round(avg, 2)
    print("6. Chip Temps (high,low,avg): ", corehigh6, corelow6, coreavg6)

def vrmtemp1():
    global vrm1
    url = 'http://10.0.0.1/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm1 = data_set['ret']['series'][-1][-1][-1]

    print("VRM Temp: ", vrm1)
def vrmtemp2():
    global vrm2
    url = 'http://10.0.0.2/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm2 = data_set['ret']['series'][-1][-1][-1]

    print("VRM Temp: ", vrm2)
def vrmtemp3():
    global vrm3
    url = 'http://10.0.0.3/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm3 = data_set['ret']['series'][-1][-1][-1]
    
    print("VRM Temp: ", vrm3)
def vrmtemp4():
    global vrm4
    url = 'http://10.0.0.4/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm4 = data_set['ret']['series'][-1][-1][-1]
    
    print("VRM Temp: ", vrm4)
def vrmtemp5():
    global vrm5
    url = 'http://10.0.0.5/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm5 = data_set['ret']['series'][-1][-1][-1]
    
    print("VRM Temp: ", vrm5)
def vrmtemp6():
    global vrm6
    url = 'http://10.0.0.6/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm6 = data_set['ret']['series'][-1][-1][-1]
    
    print("VRM Temp: ", vrm6)
def k1data():
    driver.get(k1poolaccountpage)
    time.sleep(5)
    global hr1, hr2, hr3, hr4, hr5, hr6
    global k1onlinecheck1, k1onlinecheck2, k1onlinecheck3, k1onlinecheck4, k1onlinecheck5, k1onlinecheck6
    hr1 = driver.find_element(By.XPATH, k1pool3hrhr1).text
    hr2 = driver.find_element(By.XPATH, k1pool3hrhr2).text
    hr3 = driver.find_element(By.XPATH, k1pool3hrhr3).text
    hr4 = driver.find_element(By.XPATH, k1pool3hrhr4).text
    hr5 = driver.find_element(By.XPATH, k1pool3hrhr5).text
    hr6 = driver.find_element(By.XPATH, k1pool3hrhr6).text
    k1onlinecheck1 = driver.find_element(By.XPATH, k1online1).text
    k1onlinecheck2 = driver.find_element(By.XPATH, k1online2).text
    k1onlinecheck3 = driver.find_element(By.XPATH, k1online3).text
    k1onlinecheck4 = driver.find_element(By.XPATH, k1online4).text
    k1onlinecheck5 = driver.find_element(By.XPATH, k1online5).text
    k1onlinecheck6 = driver.find_element(By.XPATH, k1online6).text
    print("3hr HR @ Pool: ", hr1, ' Last share: ', k1onlinecheck1)
    print("3hr HR @ Pool: ", hr2, ' Last share: ', k1onlinecheck2)
    print("3hr HR @ Pool: ", hr3, ' Last share: ', k1onlinecheck3)
    print("3hr HR @ Pool: ", hr4, ' Last share: ', k1onlinecheck4)
    print("3hr HR @ Pool: ", hr5, ' Last share: ', k1onlinecheck5)
    print("3hr HR @ Pool: ", hr6, ' Last share: ', k1onlinecheck6)
    
def htmldata():
    TotalHashrate = 0
    file = open("IRFarm_1.6.html", "w")
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Table with Details Button</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #e6e6e6;
}}
.container {{
    text-align: center;
    position: relative;
    margin-top: 20px;
}}
table {{
    display: none;
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
}}
th, td {{
    border: 1px solid #00cedd;
    text-align: left;
    padding: 8px;
}}
th {{
    background-color: #00cedd;
}}
button {{
    padding: 5px 0;
    font-size: 16px;
    cursor: pointer;
    width: 100%;
    background-color: #00cedd;
    border-radius: 10px;
    border-style: none;
}}
</style>

</head>
<body>
<!--3 hour Hashrate:-->
<!--Est. $kas / day:</left></p>-->>
<!--Total $Kas Mined:-->>
<div class="container">
<button id="detailsBtn">Details</button>
<table id="SeprateData">
   <thead>
    <tr>
        <th><center>ASIC ID:</center></th>
        <th><center>Date:</center></th>
        <th><center>Time:</center></th>
        <th><center>Max Core:</center></th>
        <th><center>Avg Core:</center></th>
        <th><center>Max VRM:</center></th>
        <th><center>3Hr Hashrate:</center></th>
        <th><center>Device Last Seen:</center></th>
        <th><center>Links:</center></th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><center>rig1</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center><a href="http://10.0.0.1">ASIC Settings</a></center></td>
    </tr>
    <tr>
        <td><center>rig2</center></td>
        <td><center>_</center></td>
        <td><center>_</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center><a href="http://10.0.0.2">ASIC Settings</a></center></td>
    </tr>
    <tr>
        <td><center>rig3</center></td>
        <td><center>_</center></td>
        <td><center>_</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center><a href="http://10.0.0.3">ASIC Settings</a></center></td>
    </tr>
    <tr>
        <td><center>rig4</center></td>
        <td><center>_</center></td>
        <td><center>_</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center>{}</center></td>
        <td><center><a href="http://10.0.0.4">ASIC Settings</a></center></td>
    </tr>
<tr>
    <td><center>rig5</center></td>
    <td><center>_</center></td>
    <td><center>_</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center><a href="http://10.0.0.5">ASIC Settings</a></center></td>
</tr>
<tr>
    <td><center>rig6</center></td>
    <td><center>_</center></td>
    <td><center>_</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center>{}</center></td>
    <td><center><a href="http://10.0.0.6">ASIC Settings</a></center></td>
</tr>
</tbody>
</table>
</div>
</body>
</html>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('detailsBtn').addEventListener('click', function() {{
        var table = document.getElementById('SeprateData');
        if (table.style.display === 'none') {{
            fadeIn(table);
        }} else {{
            fadeOut(table);
        }}
    }});

    function fadeIn(element) {{
        var op = 0.1;  // initial opacity
        element.style.display = 'table';
        var timer = setInterval(function () {{
            if (op >= 1) {{
                clearInterval(timer);
                return;
            }}
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op += 0.1; // Incrementing opacity
        }}, 10);
    }}

    function fadeOut(element) {{
        var op = 1;  // initial opacity
        var timer = setInterval(function () {{
            if (op <= 0.1){{
                clearInterval(timer);
                element.style.display = 'none';
            }}
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op -= op * 0.1;
        }}, 10);
    }}
}});
</script>
""".format(current_date, current_time, corehigh1, coreavg1, vrm1, hr1, k1onlinecheck1, corehigh2, coreavg2, vrm2, hr2, k1onlinecheck2, corehigh3, coreavg3, vrm3, hr3, k1onlinecheck3, corehigh4, coreavg4, vrm4, hr4, k1onlinecheck4, corehigh5, coreavg5, vrm5, hr5, k1onlinecheck5, corehigh6, coreavg6, vrm6, hr6, k1onlinecheck6)

    file.write(html_content)
    file.close()

def displaytable():
    global current_date, current_time
    coretemp1(); coretemp2(); coretemp3()
    coretemp4(); coretemp5(); coretemp6()
    vrmtemp1(); vrmtemp2(); vrmtemp3()
    vrmtemp4(); vrmtemp5(); vrmtemp6()
    k1data()
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S %p", t); current_date = time.strftime("%m/%d")
    table_data = [['ASIC ID:', 'Date:', 'Time:', 'Core Temp:', 'Core Temp Avg:', 'VRM Temp:', '3hr Hashrate:', 'LastShare:'],
                  ['rig1', current_date, current_time, corehigh1, coreavg1, vrm1, hr1, k1onlinecheck1],
                  ['rig2', '', '', corehigh2, coreavg2, vrm2, hr2, k1onlinecheck2],
                  ['rig3', '', '', corehigh3, coreavg3, vrm3, hr3, k1onlinecheck3],
                  ['rig4', '', '', corehigh4, coreavg4, vrm4, hr4, k1onlinecheck4],
                  ['rig5', '', '', corehigh5, coreavg5, vrm5, hr5, k1onlinecheck5],
                  ['rig6', '', '', corehigh6, coreavg6, vrm6, hr6, k1onlinecheck6]]
    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

init()
while 1 > 0:
    displaytable()
    htmldata()
    time.sleep(RefreshDelay)