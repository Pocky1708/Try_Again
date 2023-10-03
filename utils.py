from kivy.app import App
from jnius import autoclass, cast, PythonJavaClass, java_method

PythonActivity = autoclass('org.kivy.android.PythonActivity')
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
context = cast('android.content.Context', currentActivity.getApplicationContext())

FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
FirebaseFirestore = autoclass('com.google.firebase.firestore.FirebaseFirestore')

HashMap = autoclass('java.util.HashMap')

FirebaseApp.initializeApp(context)

instance = FirebaseFirestore.getInstance()

APP_INSTANCE = App.get_running_app()

# writing

def write_weather_data():
    myMap = HashMap()
    myMap.put("temperature", 25)
    myMap.put("sky", "cloudy")
    myMap.put("wind_speed", 11.5)
    myMap.put("wind_speed_unit", "km")
    instance.collection("weather").document("today").set(myMap)

def read_weather_data():
    task = instance.collection("weather").document("today").get()
    task.addOnSuccessListener(TodaySuccessListener())


class TodaySuccessListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/android/gms/tasks/OnSuccessListener']
    # Include line or this exception happens
    # jnius.jnius.JavaException: JVM exception occurred: interface com.google.android.gms.tasks.OnCompleteListener is not visible from class loader java.lang.IllegalArgumentException
    __javacontext__ = "app"

    # You get "ValueError: need more than 1 value to unpack" <- if you dont add ;
    # https://github.com/kivy/pyjnius/blob/master/jnius/jnius_utils.pxi#L43
    @java_method('(Ljava/lang/Object;)V')
    def onSuccess(self, doc):
        data = doc.getData()
        for key in data.keySet():
            APP_INSTANCE.weather_data[key] = data.get(key)

today_listener = None

def stream_weather_data():
    global today_listener
    todayRef = instance.collection("weather").document("today")
    if today_listener is None:
        today_listener = todayRef.addSnapshotListener(TodaySnapshotStream())


def remove_listener_of_weather_data():
    global today_listener
    if today_listener is not None:
        today_listener.remove()



class TodaySnapshotStream(PythonJavaClass):
    __javainterfaces__ = ['com/google/firebase/firestore/EventListener']
    __javacontext__ = "app"

    # I'm using java/lang/Object though if you want to be specific, you can use
    # com/google/firebase/firestore/DocumentSnapshot
    @java_method('(Ljava/lang/Object;Lcom/google/firebase/firestore/FirebaseFirestoreException;)V')
    def onEvent(self, doc, error):
        try:
            data = doc.getData()
            for key in data.keySet():
                APP_INSTANCE.weather_data[key] = data.get(key)
            print(APP_INSTANCE.weather_data)
        except Exception as e:
            print(e)
