import os; import sys; import time
from selenium.webdriver.common.by import By; from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from tabulate import tabulate; import json

 # K1-Pool Data (so far today's) resets @ 3:00 pm #

def OSType(): # is program running on linux, or windows? What file path to write HTML? 
    print("Building OS Directory for HTML")
    global file_path, root_path
    if os.name == 'posix':  # Linux
        file_path = "/home/asicfarm/Public/IRFarm_Server/1.6/IRFarm_1.6.3.html"
        root_path = "/home/asicfarm/Public/IRFarm_Server/1.6/IRFarm_1.6.3.py"
    elif os.name == 'nt':   # Windows
        file_path = "IRFarm_1.6.3.html"
        root_path = "IRFarm_1.6.3.py"

    else:
        raise OSError("Unsupported operating system")
def InitVars(): # User Static Variables Are set here...
    global RefreshDelay, iceriverusername, iceriverpassword, CoreOverheatTemp, CoreOverheat, VRMOverheatTemp, VRMOverheat, driver, k1poolaccountpage, k1pool3hrhr1, k1pool3hrhr2, k1pool3hrhr3, k1pool3hrhr4, k1pool3hrhr5, k1pool3hrhr6
    global k1online1, k1online2, k1online3, k1online4, k1online5, k1online6, k13hrhr, k130mhr, k1daily, k1total, max_retry_count, retry_delay, k1rewardtab, k1machinesonline
    global kwhcost, farmpowerwh, k1kasSFday, k1kasSFweek, k1kasSFmonth, k1rewardSFday, k1rewardSFweek, k1rewardSFmonth
    RefreshDelay = 300 # Seconds of delay before refreshing values
    iceriverusername='admin'; iceriverpassword='12345678' # Asic Machines login (all have to be the same)
    CoreOverheatTemp = 60
    CoreOverheat = 68
    VRMOverheatTemp = 100
    VRMOverheat = 95
    max_retry_count = 5  # Maximum number of retries ( K1 POOL )
    retry_delay = 4  # Delay between retries in seconds ( K1 POOL )
    k1poolaccountpage = 'https://k1pool.com/pool/kaspa/account/KrMAsyjkMVamRzLWiBamifKMFvQ5unG2Ssz'
    kwhcost = 0.2
    farmpowerwh = 1300

    k1rewardtab = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/ul/li[2]/a'
    
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
    k1machinesonline = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div[5]/div/div/div/div/div[2]/span[3]'

    k13hrhr =  '//html/body/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div[5]/div/div/div/div/div[4]/span[3]'
    k130mhr =  '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div[5]/div/div/div/div/div[3]/span[3]'
    k1total =  '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div/div/div[4]/span[3]'
    k1daily =  '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div[4]/div/div/div/div/div[3]/span[3]'

    k1kasSFday = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]'
    k1kasSFweek = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[6]/td[2]'
    k1kasSFmonth = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[7]/td[2]'
    k1rewardSFday = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[4]/td[4]'
    k1rewardSFweek = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[6]/td[4]'
    k1rewardSFmonth = '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[7]/td[4]'
def Boot():
    global driver
    OSType()
    InitVars()
    while 1 > 0:
        try:
            print('Initilizing WebDriver, Please Wait...')
            driver = webdriver.Firefox()
            BuildDataTables()
            WriteHTML()
            driver.quit()
            print("Data Extrapolation Success!                                                     Next Cycle: ", RefreshDelay, " seconds")
            time.sleep(RefreshDelay)
        except TimeoutException:
            print("TimeoutException occurred. Restarting the program.")
            driver.quit() # Close the WebDriver instance
            Boot()
        except NoSuchElementException:
            print("NoSuchElementException occurred. Restarting the program.")
            driver.quit() # Close the WebDriver instance
            Boot()

def coretemp(asic_id): # Detect Local miners tempatures 
    global corehigh1, corelow1, coreavg1
    global corehigh2, corelow2, coreavg2
    global corehigh3, corelow3, coreavg3
    global corehigh4, corelow4, coreavg4
    global corehigh5, corelow5, coreavg5
    global corehigh6, corelow6, coreavg6
    
    url = f'http://10.0.0.{asic_id}/user/timeseries?series=chiptemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    values = data_set['ret']['series'][-1][-1] # add another [-1] to select last digit 
    data_list = eval(str(values))

    corehigh = max(values)
    corelow = min(values)
    avg = sum(values) / len(values)
    coreavg = round(avg, 2)
    print(f"{asic_id}. Chip Temps (high,low,avg): ", corehigh, corelow, coreavg)
    
    globals()[f'corehigh{asic_id}'] = corehigh
    globals()[f'corelow{asic_id}'] = corelow
    globals()[f'coreavg{asic_id}'] = coreavg
def vrmtemp(asic_id): # Detect Local miners tempatures 
    global vrm1, vrm2, vrm3, vrm4, vrm5, vrm6
    
    url = f'http://10.0.0.{asic_id}/user/timeseries?series=boardtemp'
    driver.get(url)
    page = driver.find_element(By.TAG_NAME, "body").text
    data_set = json.loads(page)
    vrm = data_set['ret']['series'][-1][-1][-1]

    globals()[f'vrm{asic_id}'] = vrm
    print(f"VRM Temp for ASIC {asic_id}: {vrm}")
def k1data(): # Gather data from pool, and assemble most of the output variables for HTML 
    global hr1, hr2, hr3, hr4, hr5, hr6, machinesonline, current_date, current_time
    global k1onlinecheck1, k1onlinecheck2, k1onlinecheck3, k1onlinecheck4, k1onlinecheck5, k1onlinecheck6
    global farmhr3hr, farmhr30m, farmtotalkas, farmdailykas, farmweeklykas, farmmonthlykas
    global farmkasSFday, farmkasSFweek, farmkasSFmonth, rewardsSFday, rewardsSFweek, rewardsSFmonth
    global farmdailyelectric, farmweeklyelectric, farmmonthlyelectric
    try:
        print("Processing K1 Data")
        print("# of tries: ", )
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, k1pool3hrhr6))
        )
    except StaleElementReferenceException:
        print("K1-Pool XPATH's are changed/invisible/unavalible, Retrying if its just not loading...")
        print("# of tries @ K1-Pool: ", )
        time.sleep(retry_delay); k1data()
    except TimeoutException:
        print("Hitting some snags on Reciving Data K1-Pool, Please be patient...")
        print("# of tries @ K1-Pool: ")
        time.sleep(retry_delay); k1data()
    finally:
        t = time.localtime()
        current_date = time.strftime("%m-%d-%Y", t)
        current_time = time.strftime("%I:%M:%S %p", t)
        current_day_passing = time.strftime("%H", t)
        driver.execute_script("document.body.style.transform = 'scale(0.5)';")
        time.sleep(1)

        hr1 = driver.find_element(By.XPATH, k1pool3hrhr1).text
        hr2 = driver.find_element(By.XPATH, k1pool3hrhr2).text
        hr3 = driver.find_element(By.XPATH, k1pool3hrhr3).text
        hr4 = driver.find_element(By.XPATH, k1pool3hrhr4).text
        hr5 = driver.find_element(By.XPATH, k1pool3hrhr5).text
        hr6 = driver.find_element(By.XPATH, k1pool3hrhr6).text
        variables_dict = {
            '1:': hr1,
            '2:': hr2,
            '3:': hr3,
            '4:': hr4,
            '5:': hr5,
            '6:': hr6,
        }; print("\n Pool Hashrates: ", hr1, hr2, hr3, hr4, hr5, hr6)

        machinesonline = driver.find_element(By.XPATH, k1machinesonline).text
        k1onlinecheck1 = driver.find_element(By.XPATH, k1online1).text
        k1onlinecheck2 = driver.find_element(By.XPATH, k1online2).text
        k1onlinecheck3 = driver.find_element(By.XPATH, k1online3).text
        k1onlinecheck4 = driver.find_element(By.XPATH, k1online4).text
        k1onlinecheck5 = driver.find_element(By.XPATH, k1online5).text
        k1onlinecheck6 = driver.find_element(By.XPATH, k1online6).text
        variables_dict = {
                '1:': k1onlinecheck1,
                '2:': k1onlinecheck2,
                '3:': k1onlinecheck3,
                '4:': k1onlinecheck4,
                '5:': k1onlinecheck5,
                '6:': k1onlinecheck6,
                'Machines Online: ': machinesonline,
        }; print ("\n Last Seen: ", variables_dict)

        farmhr3hr = driver.find_element(By.XPATH, k13hrhr).text
        farmhr30m = driver.find_element(By.XPATH, k130mhr).text
        farmtotalkas = driver.find_element(By.XPATH, k1total).text
        variables_dict = {
            'Farm 3Hour:': farmhr3hr,
            'Farm 30Min:': farmhr30m,
            'Net Mined $KAS:': farmtotalkas,
        }; print ("\n", variables_dict)

        time.sleep(1)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, k1rewardtab)))
        element.click() # Click on the element

        farmdailykas = driver.find_element(By.XPATH, k1daily).text
        farmweeklykas = round(7 * (float(float(farmdailykas))), 2)
        farmmonthlykas = round(4 * (float(float(farmweeklykas))), 2)

        unroundedfarmkasSFday = driver.find_element(By.XPATH, k1kasSFday).text
        unroundedfarmkasSFweek = driver.find_element(By.XPATH, k1kasSFweek).text
        unroundedfarmkasSFmonth = driver.find_element(By.XPATH, k1kasSFmonth).text
        farmkasSFday = round(float(unroundedfarmkasSFday), 2)
        farmkasSFweek = round(float(unroundedfarmkasSFweek), 2)
        farmkasSFmonth = round(float(unroundedfarmkasSFmonth), 2)
        
        rewardsSFday = driver.find_element(By.XPATH, k1rewardSFday).text
        rewardsSFweek = driver.find_element(By.XPATH, k1rewardSFweek).text
        rewardsSFmonth = driver.find_element(By.XPATH, k1rewardSFmonth).text
        
        farmmonthlyelectric = round(((farmpowerwh/1000)*672*kwhcost))
        farmdailyelectric = (farmmonthlyelectric / 28)
        farmweeklyelectric = (farmmonthlyelectric / 4)
        variables_dict = {
            'Kas / day Est:': farmdailykas,
            'Kas / week Est:': farmweeklykas,
            'Kas / month Est:': farmmonthlykas,
            'Kas mined today:': farmkasSFday,
            'Kas mined this week:': farmkasSFweek,
            'Kas mined this month:': farmkasSFmonth,
            '\n$ Income Today:': rewardsSFday,
            '$ Income this week:': rewardsSFweek,
            '$ Income this month:': rewardsSFmonth,
            'Farm Costs $ / Month:': farmmonthlyelectric,
            'Farm Costs $ / day:': farmdailyelectric,
            'Farm Costs $ / week:': farmweeklyelectric
        }; print("\n", variables_dict)


def BuildDataTables(): # Gather $KAS price from URL and finish the last few output variables
    global kasprice
    for asic_id in range(1, 7):
        coretemp(asic_id)
        vrmtemp(asic_id)
    print("\n Finished Loading ASIC Data")
    print("\n loading K1-Pool Building Data, Please Wait...")
    driver.get(k1poolaccountpage); 
    k1data()
    print("Loading Crypto Price...")
    driver.get('https://www.coingecko.com/en/coins/kaspa')
    kaspricexpath = '/html/body/div[2]/main/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/span'
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, kaspricexpath))
        )
    finally:
        kasprice = driver.find_element(By.XPATH, kaspricexpath).text
        kasprice_value = float(kasprice.replace('$', ''))
        table_data = [['ASIC ID:', 'Date:', 'Time:', 'Core Temp:', 'Core Temp Avg:', 'VRM Temp:', '3hr Hashrate:', 'LastShare:'],
                      ['rig1', "current_date", "current_time", corehigh1, coreavg1, vrm1, hr1, k1onlinecheck1],
                      ['rig2', '', '', corehigh2, coreavg2, vrm2, hr2, k1onlinecheck2],
                      ['rig3', '', '', corehigh3, coreavg3, vrm3, hr3, k1onlinecheck3],
                     ['rig4', '', '', corehigh4, coreavg4, vrm4, hr4, k1onlinecheck4],
                      ['rig5', '', '', corehigh5, coreavg5, vrm5, hr5, k1onlinecheck5],
                      ['rig6', '', '', corehigh6, coreavg6, vrm6, hr6, k1onlinecheck6]]
        print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
        print("Est. $KAS So Far Today: ", round(farmkasSFday, 2), "          $KAS Price: ", kasprice, "          ASIC's Online: ", machinesonline)
def WriteHTML(): # This is where the main HTML acctualy gets written using output variables

    html_content = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" http-equiv="refresh" content="300">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IRFarm 1.6.3</title>
        <style>
            .onlinemachinesbanner {{
                color: #ffffff;
                padding: 10px 0;
                width: 100%;
                background-color: #00c2e7;
                border-radius: 5px;
                border-style: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.778); /* drop shadow */
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #ffffff;
                color: #000000;
            }}
            .container {{
                text-align: center;
                position: relative;
            }}
            .gridlayout h4 {{
            margin: 0; /* Remove vertical margin for elements within gridlayout */
            margin: 3px;
            }}
            .gridlayout {{
                display: grid;
                grid-template-columns: repeat(3, 1fr); /* Three columns with equal width */
                gap: 0; /* No gap between grid items */
                margin: 0; /* Remove any margin on the grid container */
                padding: 0; /* Remove any padding on the grid container */
            }}
            .A123 {{
                background-color: #00c2e7;
            }}
            .daycolumn {{
                background-color: #8aff73;
            }}
            .weekcolumn {{
                background-color: #ffb68e;
            }}
            .monthcolumn {{
                background-color: #ff92fa;
            }}
            table {{
                display: table;
                border-collapse: collapse;
                width: 100%;
                margin-top: 10px;
                box-shadow: 0 4px 8px rgb(0, 0, 0.778); /* drop shadow */
                border-radius: 10px;
            }}
            th, td {{ /* "details" whole table data*/
                border: 1px solid #0000001a; /* set table dividers color */
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15); /* drop shadow */
                text-align: left; /* only applies to headers */
                padding: 4px; /* space between cell walls, and interior text */
                font-size: 18px;
            }}
            .details_table_head {{ /* "details" table head*/
                background-color: #00c2e7;
                color: #ffffff;
            }}
            button {{
                padding: 10px 0;
                color: rgb(255, 255, 255);
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                background-color: #00c2e7;
                border-radius: 5px;
                border-style: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.778); /* drop shadow */
            }}
        </style>
    </head>

    <body link="blue" vlink="blue">
        <h2><center class="onlinemachinesbanner">Machines Online: {}</center><h2>
        <div class="gridlayout">
            <div><h4 class="A123"><center>HashRate - 3Hr:</center><center>{}</center></h4></div>
            <div><h4 class="A123"><center>HashRate - 30m:</center><center>{}</center></h4></div>
            <div><h4 class="A123"><center>Net Kas Mined: </center><center>{}</center></h4></div>
            <div><h4 class="daycolumn"><center>Mined Kas this day:</center><center>{}</center></v></h4></div>
            <div><h4 class="weekcolumn"><center>Mined Kas this week:</center><center>{}</center></h4></div>
            <div><h4 class="monthcolumn"><center>Mined Kas this month:</center><center>{}</center></h4></div>
            <div><h4 class="daycolumn"><center>Est. Kas/day</center><center>{}</center></h4></div>
            <div><h4 class="weekcolumn"><center>Est. Kas/week</center><center>{}</center></h4></div>
            <div><h4 class="monthcolumn"><center>Est. Kas/month</center><center>{}</center></h4></div>
            <div><h4 class="daycolumn"><center>$ Rewads this day:</center><center>{}</center></h4></div>
            <div><h4 class="weekcolumn"><center>$ Rewads this week</center><center>{}</center></h4></div>
            <div><h4 class="monthcolumn"><center>$ Rewads this month</center><center>{}</center></h4></div>
            <div><h4 class="daycolumn"><center>$ Costs / day:</center><center>{}</center></h4></div>
            <div><h4 class="weekcolumn"><center>$ Costs / week</center><center>{}</center></h4></div>
            <div><h4 class="monthcolumn"><center>$ Costs / month</center><center>{}</center></h4></div>
        </div>
        <div class="container">
            <button id="detailsBtn"><b>Details</b></button>
            <table id="SeprateData">
                <thead>
                    <tr class="details_table_head">
                        <td><left>ASIC:</left></td>
                        <td><left>Date:</left></td>
                        <td><left>Time:</left></td>
                        <td><left>Core Max:</left></td>
                        <td><left>Core Avg:</left></td>
                        <td><left>VRM Max:</left></td>
                        <td><left>HashRate @ Pool:</left></td>
                        <td><left>Last Valid Share:</left></td>
                        <td><left>Links:</a></left></td>
                    </tr>
                </thead>
                <tbody>
                <tr>
                    <td><center>ASIC 1</center></td>
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
                    <td><center>ASIC 2</center></td>
                    <td><center> </center></td>
                    <td><center> </center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center><a href="http://10.0.0.2">ASIC Settings</a></center></td>
                </tr>
                <tr>
                    <td><center>ASIC 3</center></td>
                    <td><center> </center></td>
                    <td><center> </center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center><a href="http://10.0.0.3">ASIC Settings</a></center></td>
                </tr>
                <tr>
                    <td><center>ASIC 4</center></td>
                    <td><center> </center></td>
                    <td><center> </center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center><a href="http://10.0.0.4">ASIC Settings</a></center></td>
                </tr>
                <tr>
                    <td><center>ASIC 5</center></td>
                    <td><center> </center></td>
                    <td><center> </center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center>{}</center></td>
                    <td><center><a href="http://10.0.0.5">ASIC Settings</a></center></td>
                </tr>
                <tr>
                    <td><center>ASIC 6</center></td>
                    <td><center> </center></td>
                    <td><center> </center></td>
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
            var op = 0; // initial opacity
            element.style.opacity = 0; // Ensure initial opacity is set
            element.style.display = 'table';

            var timer = setInterval(function () {{
                if (op >= 1) {{
                    clearInterval(timer);
                    return;
                }}
                else {{
                    op += 0.05; // Incrementing opacity gradually
                    element.style.opacity = op;
                    element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                }}
            }}, 20);
        }}
        function fadeOut(element) {{
            var op = 1; // initial opacity
            var timer = setInterval(function () {{
                if (op <= 0) {{ // Update the condition
                    clearInterval(timer);
                    element.style.display = 'none';
                    return;
                }}
                else {{
                op -= 0.05; // Decrementing opacity gradually
                element.style.opacity = op;
                element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                }}
            }}, 20);
        }}
    }}); 
</script>""".format(
    machinesonline, farmhr3hr, farmhr30m, farmtotalkas,
    farmkasSFday, farmkasSFweek, farmkasSFmonth,
    farmdailykas, farmweeklykas, farmmonthlykas,
    rewardsSFday, rewardsSFweek, rewardsSFmonth,
    farmdailyelectric, farmweeklyelectric, farmmonthlyelectric,
    current_date, current_time, corehigh1, coreavg1, vrm1, hr1, k1onlinecheck1,
    corehigh4, coreavg4, vrm4, hr4, k1onlinecheck4,
    corehigh3, coreavg3, vrm3, hr3, k1onlinecheck3,
    corehigh4, coreavg4, vrm4, hr4, k1onlinecheck4,
    corehigh5, coreavg5, vrm5, hr5, k1onlinecheck5,
    corehigh6, coreavg6, vrm6, hr6, k1onlinecheck6,
    ) # needs _48_ arguments
    
    try:
        file = open(file_path, "w")
        file.write(html_content)
    finally:
        file.close()

Boot()