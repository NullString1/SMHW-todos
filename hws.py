import requests, datetime, json, calendar, ctypes, PIL
from time import sleep
from PIL import ImageFont, Image, ImageDraw

USERNAME = "USERNAME" #Enter username
PASSWORD = "PASSWORD" #Enter password
SCHOOLID = "SCHOOLID" #Enter school id

#Get current date
date = datetime.datetime.now()
today = date.strftime("%Y-%m-%d")
#Add datetime object as well
today2 = datetime.datetime.strptime(today, "%Y-%m-%d")
global status, todos, data

class homework:
    def __init__(self, completed, due, teacher_name, subject, title):
        self.completed = completed
        self.due = due
        self.teacher_name = teacher_name
        self.subject = subject
        self.title = title

        

def GetAuth(user, password, school_id):
    global status, token
    status = 0
    #Set payload and data for oauth2 request
    payload = {"client_id": "55283c8c45d97ffd88eb9f87e13f390675c75d22b4f2085f43b0d7355c1f","client_secret": "c8f7d8fcd0746adc50278bc89ed6f004402acbbf4335d3cb12d6ac6497d3"}
                   
    data = {"username": user, "password": password, "school_id": school_id, "grant_type": "password",
                    "grant_type": "password", "school_id": school_id}
    temp = requests.post("https://api.showmyhomework.co.uk/oauth/token", params=payload, data=data,
                                 headers={"Accept": "application/smhw.v3+json"})
    #Parse reply data from oauth2 request
    reply = temp.text
    reply = reply.replace("'", '"')
    reply = json.loads(reply)
    token = reply["smhw_token"]
    token_expires = reply["expires_in"]
    refresh_token = reply["refresh_token"]
    
def Download():
    global status, todos
    status = 1
    #Set headers for todos list request
    headers = {"Accept": "application/smhw.v3+json", "Authorization": "Bearer " + token}

    response = requests.get("https://api.showmyhomework.co.uk/api/todos",
                            headers = headers)
    #Parse data from todos request
    todos = json.loads(response.text)["todos"]

def Parse():
    global status, todos, hws
    status = 2
    hws=[]
    for hw in todos:
        hw["due_on"] = hw["due_on"].split("T") 
        if datetime.datetime.strptime(hw["due_on"][0], "%Y-%m-%d") >= today2: #Filters out old hws
            homeworka = homework(hw["completed"], hw["due_on"][0], hw["teacher_name"], hw["subject"], hw["class_task_title"])
            hws.append(homeworka)
    hws=sorted(hws, key=lambda hw: hw.due)
    
    for hw in hws: # Output
        hw.day = calendar.day_name[datetime.datetime.strptime(hw.due, "%Y-%m-%d").weekday()]
        if hw.completed: hw.compl="✓"
        else: hw.compl="✗"
        print(hw.compl + "   " + hw.subject + " - " + hw.title + " - " + hw.day + " - " + hw.due)
def Exit():
    global status
    status = 5
    #Raise System Exit Call after 60 seconds
    print("Wait 60 Seconds To Exit")
    #sleep(60)
    raise SystemExit

def Picture():
    img=Image.new("RGB", (1920,1080),(27,148,239))
    draw = ImageDraw.Draw(img)

    draw.line([0, 100, 1920, 100], fill=(14,121,201), width=100)
    draw.text([0, 80], hws[0].compl + hws[0].subject + " - " + hws[0].title + " - " + hws[0].day + " - " + hws[0].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw.line([0, 280, 1920, 280], fill=(14,121,201), width=100)
    draw.text([0, 260], hws[1].compl + hws[1].subject + " - " + hws[1].title + " - " + hws[1].day + " - " + hws[1].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw.line([0, 460, 1920, 460], fill=(14,121,201), width=100)
    draw.text([0, 440], hws[2].compl + hws[2].subject + " - " + hws[2].title + " - " + hws[2].day + " - " + hws[2].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw.line([0, 640, 1920, 640], fill=(14,121,201), width=100)
    draw.text([0, 620], hws[3].compl + hws[3].subject + " - " + hws[3].title + " - " + hws[3].day + " - " + hws[3].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw.line([0, 820, 1920, 820], fill=(14,121,201), width=100)
    draw.text([0, 800], hws[4].compl + hws[4].subject + " - " + hws[4].title + " - " + hws[4].day + " - " + hws[4].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw.line([0, 1000, 1920, 1000], fill=(14,121,201), width=100)
    draw.text([0, 980], hws[5].compl + hws[5].subject + " - " + hws[5].title + " - " + hws[5].day + " - " + hws[5].due, font=ImageFont.truetype('DejaVuSans.ttf', 40))
    draw = ImageDraw.Draw(img)

    img.save("test.jpg")
    sleep(5)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "IMAGE PATH" , 0)

GetAuth(USERNAME, PASSWORD, SCHOOLID)
Download()
Parse()
#Picture() #Not recommended
Exit()
