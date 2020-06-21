from django.shortcuts import render
from .services import APIService
import subprocess
import threading
import time

_service = APIService()
def ping():
    while True:
        try:
            print("[INFO] Service Thread Started.")
            _service.get_district_daily_covid_data()
            #_service.get_tweets()  # Not a free API. Find the solution for storing tweets based on location. 
        except Exception as e:
            print('[ERROR] Connectin Problems arises!', e.args)
        else:
            print('[INFO] Service Thread Execution Successful !')
        finally:
            print("[INFO] Service Thread going to sleep for 30 min.")
            time.sleep(1800)    # Will sleep for 1800 sec = 30 min.

t = threading.Thread(target=ping)
t.daemon = True
t.start() # this will run the `ping` function in a separate thread


def home(request):
    print('Last Updated: '+APIService._lastUpadated)
    return render(request, 'iindex.html', {'status':None, 'data': APIService._districtDaily })

def main(request):
    if request.method == 'POST':
        covid, district, status = None, None, None
        covidX = []
        pin = request.POST['pincode']
        try:
            temp = _service.getCovidCount(pin)
            covid = temp['Covid_Count']
            covidX = covid[-1]
            district = temp['District']
        except Exception as e:
            print('[ERROR] While fetching the PIN.',e)
            status = 'white'
        if status != 'white':
            last = covid[-21]
            for day in covid[-20:]:
                if last['active'] >= day['active']:
                    status = 'green'
                else:
                    status = 'orange'
                    break
            if status == 'orange' and covid[-15]['confirmed']*2 <= covid[-1]['confirmed']:
                status = 'red'
    return render(request, 'main.html', {'status': status,'district': district,'pin':pin, 'covid': covidX, 'sentiment':APIService._sentimentData})

def about(request):
    return render(request, 'about.html')