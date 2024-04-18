# Nick Teller (nst6tx)
#https://www.geeksforgeeks.org/web-scraping-from-wikipedia-using-python-a-complete-guide/#
#https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
#https://www.geeksforgeeks.org/reading-writing-text-files-python/


from bs4 import BeautifulSoup
import requests



def write_header(path, d, y, h, s, r):
    d = str(d)
    y = str(y)
    Func = open(path + d + "0s_header.html", "r")
    header = Func.readlines()
    Func.close()
    #print(header)
    for i in range(len(header)):
        if header[i] == '    <h2 class="text-center text-black mb-4">' + d + 'x Season Overview</h2>\n':
            header[i] = '    <h2 class="text-center text-black mb-4">' + d + y + ' Season Overview</h2>\n'
        elif header [i] == '            <h2 class="text-center text-black">' + d + 'x Season Game by Game (x-x)</h2>\n':
             header[i] = '            <h2 class="text-center text-black">' + d + y + ' Season Game by Game '+ r +'</h2>\n'

    header = ''.join(header)
    Func = open(path + d + y + ".html", "w")
    Func.write(header)
    Func.close()

def write_overview(h,s,r):

    return


def scrape_scores(url):
    page = requests.get(url)
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    games = soup.find_all('tr', {"class": "CFB-schedule-row"})
    # for game in games:
    #     data = game.find_all("td")
    #     tmp = data[6].get_text()
    #     # print(tmp)

    shedule = []
    for game in games:
        data = game.find_all("td")
        tmp = []
        # print(len(data))
        for i in range(len(data)):
            text = data[i].get_text()
            text = text.replace("*", "")
            text = text.replace(u'\xa0', u' ')
            text = text.replace("No. ", "#")
            tmp.append(text)
        shedule.append(tmp)
    #print(shedule)
    headers = []
    h = soup.find('table', {"class": "wikitable"})
    h = h.find_all("th")
    for item in h:
        headers.append(item.get_text())
    #print(headers)

    team_info = soup.find_all('td', {"class": "infobox-data"})
    #print(team_info)
    # record = team_info[1].get_text()
    # record = record.replace("–", "-")
    record = "WRONG"
    for info in team_info:
        if info.get_text()[1] == "–" or info.get_text()[2] == "–":
            record = info.get_text()
            record = record.replace("–", "-")
            break

    return headers, shedule, record

def get_needed_scores_and_headers(h,s):
    needed_h = []
    needed_s = []
    for i in range(len(h)):
        if h[i] == "Opponent" or h[i] == "Rank" or h[i] == "Result":
            needed_h.append(h[i])
            tmp = []
            for j in range(len(s)):
                tmp.append(s[j][i])
            needed_s.append(tmp)
    return needed_h, needed_s

def main():
    # get URL
    # url = "https://en.wikipedia.org/wiki/1980_Virginia_Cavaliers_football_team"
    # h, s, r = scrape_scores(url)
    d = 198

    path = "../../html/1980s/"
    for i in range(10):
        h,s,r = scrape_scores("https://en.wikipedia.org/wiki/" + str(d) + str(i) + "_Virginia_Cavaliers_football_team")
        needed_h, needed_s = get_needed_scores_and_headers(h,s)
        write_header(path, d, i, needed_h, needed_s, r)


    #write this to a file or test with print


if __name__ == "__main__":
    main()
