from utils.utils import *

if __name__ == '__main__':
    def get_html(url, params=None):
        h = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/74.0'}
        response = requests.get(url, params=params, headers=None)
        return response.text


    date = SearchDate()
    url = f'https://10times.com/canada/conferences?month=today&datefrom={date.today}&dateto={date.today}'
    links = ScrappyDoo(url=url)

datalist = []
for url in links.get_content():
    print(url)
    soup = BeautifulSoup(get_html(url), 'html.parser')

    # event info
    eventname = soup.find('h1').get_text()

    try:
        organizer = soup.find('h3', {'id': 'org-name'}).get_text().split('\n')[0]
    except AttributeError:
        organizer = soup.find('h3').get_text().split('\n')[0]

    description = soup.find('p', class_="desc mng word-break").get_text(strip=True)
    location = [i.get_text() for i in soup.find_all('p') if i.find('span') != None][0]
    eventdate = EventDate(soup.select('span[content]')[0].get_text().replace('-', '').split())
    rawtables = [i.find('table', class_='table noBorder mng').find_all('td') for i in
                 soup.find_all('div', class_='row11')]
    info = [rawtables[0][i].get_text().split(" ", 1) for i in range(len(rawtables[0]))]
    infodata = [i[1].strip('\n').strip() for i in info[:4]]
    time = [" ".join(i[:2]) for i in [i.split() for i in infodata[0].split('-')]]  # time
    participants = (re.findall(r"[0-9]+\s-\s[0-9]+ | [0-9]+", infodata[2]))[0].strip()
    tags = (', '.join(infodata[3].replace('Type', '').replace('&', '').split()))

    # attendees data
    users = soup.find('div', class_="visitor clearfix")
    attendeedata = []
    if users is None:
        attendeedata.append(None)
    else:
        try:
            for i in soup.find('div', class_="visitor clearfix"):
                try:
                    attendeedata.append(
                        [i.find('h4').get_text(), ' '.join(i.get_text().replace('Connect', '').split()[-2:]),
                         i.find('a').get('href')])
                except AttributeError:
                    continue
        except TypeError:
            continue

    datalist.append([url,
                     eventname,
                     organizer,
                     description,
                     location,
                     eventdate.startdate,
                     eventdate.enddate,
                     time[0],
                     time[1],
                     tags,
                     participants,
                     attendeedata])
    print('Processed')

df = pd.DataFrame(datalist, columns=['Link',
                                     'EventName',
                                     'Organizer',
                                     'Description',
                                     'Address',
                                     'StartDate',
                                     'EndDate',
                                     'StartTime',
                                     'EndTime',
                                     'Tags',
                                     'ExpectedParticipants',
                                     'AttendeeData'])
