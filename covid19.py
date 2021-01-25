import COVID19Py
import matplotlib.pyplot as plt
from sys import exit



def Graph(x, y, title):
  #darktheme cuz my eyes burn
  plt.style.use('dark_background')

  plt.plot(x,y)

  plt.xlabel('Timeline')

  '''#Label y-axis
  plt.ylabel('Confirmed Cases')'''

  plt.title(title)

  plt.show()

def subtract_backwards(lst):
  per_day = []
  isPrevious = False
  previous = None
  lst.reverse()

  for num in lst:
    if isPrevious == False:
      previous = num
      isPrevious = True
      continue
    else:
      #print(f'Current number: {num}, Previous number: {previous}')
      per_day.append(previous-num)
      previous = num
  per_day.reverse()
  return per_day


class Covid19Info:
  def __init__(self, loc):
    self.covid19 = COVID19Py.COVID19(data_source="jhu")
    #jhu = John Hopkins University (source)
    
    if loc.isdigit():
      self.location = self.covid19.getLocationById(loc)
      self.timelines = self.location.get('timelines')
      self.province = self.location.get('province')
      self.country = self.location.get('country')
    else:
      self.location = self.covid19.getLocationByCountryCode(loc, timelines=True)
      for location in self.location:
        self.province = location.get('province')
        self.country = location.get('country')
        self.timelines = location.get('timelines')

    if self.province == '':
      self.province = self.country

    self.run()

  def Cases(self):
    confirmed = self.timelines.get('confirmed')
    timeline = confirmed.get('timeline')

    case = [case for case in timeline.values()]
    

    week = int(input('What would you like to graph?\n1.Past Week\n2.Full Timeline\n'))
    if week == 1:
      time = [time[5:10] for time in timeline.keys()]
      time = time[len(time)-7:len(time)]
      print(time)
      case = case[len(case)-8:len(case)]
      cases_per_day = subtract_backwards(case)
      print(case)

      print(cases_per_day)
      Graph(time, cases_per_day, f'Confirmed COVID-19 Cases in {self.province} Past 7 days')


    elif week == 2:
        time = [time[0:10] for time in timeline.keys()]
        Graph(time, case, f'Total COVID-19 Cases in {self.province}')

  
  def Death(self):
    deaths = self.timelines.get('deaths')
    timeline = deaths.get('timeline')

    time = [time[0:10] for time in timeline.keys()]
    case = [case for case in timeline.values()]
    Graph(time, case, f'COVID-19 Deaths in {self.province}')


  def Data(self):
    latest_confirmed = self.location['latest'].get('confirmed')
    latest_deaths = self.location['latest'].get('deaths')

    print(f'LATEST COVID-19 STATISTICS in {self.country}\n')
    print(f'Confirmed COVID19 cases in BC: {latest_confirmed}')
    print(f'Deaths from COVID19 in BC: {latest_deaths}\n')


  def Exit(self):
    exit()

  def run(self):
    while True:
    #   try:
        num = int(input('What information would you like to access?\n1.Graph Confirmed Cases\n2.Graph Deaths\n3.Latest Data\n4.Exit\n'))
        action = {1:self.Cases, 2:self.Death, 3:self.Data, 4:self.Exit}
        action[num]()
    #   except (TypeError, ValueError, KeyError):
        print('invalid input')

#Where program starts
def run():
  covid19 = COVID19Py.COVID19(data_source="jhu")

  #get all locations
  locations = covid19.getLocations(timelines=False)
  while True:
    user_location = input('Enter "locations" to view all the locations\nEnter country code, ID or province: ')
    

    for location in locations:
      country = location.get('country')
      code = location.get('country_code')
      ID = location.get('id')
      province = location.get('province')

      if user_location == country:
        print('country success')
        Covid19Info(user_location)

      elif user_location ==  code:
        print('country code success')
        Covid19Info(user_location)

      elif user_location == str(ID):
        print('country id success')
        Covid19Info(user_location)

      elif user_location == province:
        print('pronvince success')
        Covid19Info(str(location.get('id')))

      elif user_location == 'locations':
        print(f'ID: {ID} Country: {country} Country Code: {code}')
    else:
      print('Error 404')
    
  
run()



''' FORMAT
{
  "location": {
    "id": 39,
    "country": "Norway",
    "country_code": "NO",
    "country_population": 5009150,
    "province": "",
    "county": "",
    "last_updated": "2020-03-21T06:59:11.315422Z",
    "coordinates": { },
    "latest": { },
    "timelines": {
      "confirmed": {
        "latest": 1463,
        "timeline": {
          "2020-03-16T00:00:00Z": 1333,
          "2020-03-17T00:00:00Z": 1463
        }
      },
      "deaths": { },
      "recovered": { }
    }
  }
}
'''
