from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import shutil
import glob
import os


def DataPull(path):
    # instantiate a chrome options object so you can set the size and headless preference
    # some of these chrome options might be uncessary but I just used a boilerplate
    chrome_options = Options()
    chrome_options.add_argument('--window-size=200x200')
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
    driver = webdriver.Chrome(options=chrome_options, executable_path="D:\Diddly\Python\chromedriver.exe")
    
    countries = (
    "ad","ar","au","at","be",
    "bo","br","bg","ca","cl",
    "co","cr","cy","cz","dk",
    "do","ec","sv","ee","fi",
    "fr","de","gr","gt","hn",
    "hk","hu","id","is","ie","it",
    "jp","lv","li","lt","lu","my",
    "mt","mx","mc","nl","nz",
    "ni","no","pa","py","pe",
    "ph","pl","pt","es","sg",
    "sk","se","ch","tw","tr",
    "gb","us","uy")
    
  #   all_markets = {
  #   "AD": "Andorra","AR": "Argentina","AU": "Australia",
  #   "AT": "Austria",
  #   "BE": "Belgium",
  #   "BO": "Bolivia",
  #   "BR": "Brazil",
  #   "BG": "Bulgaria",
  #   "CA": "Canada",
  #   "CL": "Chile",
  #   "CO": "Colombia",
  #   "CR": "Costa Rica",
  #   "CY": "Cyprus",
  #   "CZ": "Czech Republic",
  #   "DK": "Denmark",
  #   "DO": "Dominican Republic",
  #   "EC": "Ecuador",
  #   "SV": "El Salvador",
  #   "EE": "Estonia",
  #   "FI": "Finland",
  #   "FR": "France",
  #   "DE": "Germany",
  #   "GR": "Greece",
  #   "GT": "Guatemala",
  #   "HN": "Honduras",
  #   "HK": "Hong Kong",
  #   "HU": "Hungary",
  #   "ID": "Indonesia",
  #   "IS": "Iceland",
  #   "IE": "Republic of Ireland",
  #   "IT": "Italy",
  #   "JP": "Japan",
  #   "LV": "Latvia",
  #   "LI": "Liechtenstein",
  #   "LT": "Lithuania",
  #   "LU": "Luxembourg",
  #   "MY": "Malaysia",
  #   "MT": "Malta",
  #   "MX": "Mexico",
  #   "MC": "Monaco",
  #   "NL": "Netherlands",
  #   "NZ": "New Zealand",
  #   "NI": "Nicaragua",
  #   "NO": "Norway",
  #   "PA": "Panama",
  #   "PY": "Paraguay",
  #   "PE": "Peru",
  #   "PH": "Philippines",
  #   "PL": "Poland",
  #   "PT": "Portugal",
  #   "ES": "Spain",
  #   "SG": "Singapore",
  #   "SK": "Slovakia",
  #   "SE": "Sweden",
  #   "CH": "Switzerland",
  #   "TW": "Taiwan",
  #   "TR": "Turkey",
  #   "GB": "United Kingdom",
  #   "US": "United States",
  #   "UY": "Uruguay"
  # };
  
    for country in countries:
        driver.get('https://spotifycharts.com/regional/{}/daily/latest'.format(country))
        
        try:
            l = driver.find_element_by_link_text('DOWNLOAD TO CSV')
            set1 = l
            set1.click()
        except NoSuchElementException:
            continue
        
        time.sleep(5)
        
        driver.get('https://spotifycharts.com/regional/{}/weekly/latest'.format(country))
        
        try:
            l = driver.find_element_by_link_text('DOWNLOAD TO CSV')
            set1 = l
            set1.click()
        except NoSuchElementException:
            continue
        
        time.sleep(5)
        
        timestr = time.strftime("%Y%m%d")
        os.chdir(r"C:\Users\ardyb\Downloads")
        destination_folder = "D:\Diddly\Python\Stream\Data"
        
        for file in glob.glob("*daily-latest.csv"):
            shutil.move(file, destination_folder)
        
        for file in glob.glob("*weekly-latest.csv"):
            shutil.move(file, destination_folder)
        
        os.chdir(destination_folder)
        os.rename('regional-{}-daily-latest.csv'.format(country), "{}_top200_daily_{}.csv".format(country, timestr))
        os.rename('regional-{}-weekly-latest.csv'.format(country), "{}_top_200_weekly_{}.csv".format(country, timestr))
        
    driver.quit()