# OS-weather

Weather dajgno application


#Installation and requirements

    This app is tested with Python 3.5.2
        
    To install the libs used:

        $pip instal -r requirements.txt
        
    By default Django use sqlite, if you load big files maybe the app will be a little bit slowly.

#Running

    $cd src/os_weather/
        
    The first time you need to exec
       
        $python manage.py migrate
        
        
    To run the app
        
        $python manage.py runserver
        
        
    In http://localhost:8000 you can check the app, in "/loader" you can load the datasets sensors in this page, in the folder 
    "data" you have some datasets to test it, and in /charts you can query the data to look the charts.

