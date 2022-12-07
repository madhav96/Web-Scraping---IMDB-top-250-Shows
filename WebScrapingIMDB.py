from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
sheet = excel.active

sheet.append(['Show Rank','Show Name','Year of Release','IMDB Rating'])


try:
    source = requests.get('https://www.imdb.com/chart/toptv/')
    
    #To catch the error
    source.raise_for_status()

    #Using the web browsers 'inspect' we will now extract data fromm the html code
    soup = BeautifulSoup(source.text,'html.parser')

    #This will help us load all the data in <tr> tag in the <tbody> tag of the webpage that has class "lister-list"
    shows = soup.find('tbody',class_="lister-list").find_all('tr')

    for show in shows:
        #extract name in text form from the <a> tag
        name = show.find('td',class_="titleColumn").a.text
        #To avoid getting all the text in the <td> tag we need to use get_text()   
        rank = show.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]
        #extract year from span tag and remove parenthesis 
        year = show.find('td',class_="titleColumn").span.text.strip('()')
        #Extract rating from strong tag 
        rating = show.find('td',class_="ratingColumn imdbRating").strong.text

        print(rank, name, year, rating)
        sheet.append([rank, name, year, rating])

except Exception as e:
    print(e)
#Save our in an excel workbook
excel.save('IMDB Top 250 TV Shows.xlsx')
