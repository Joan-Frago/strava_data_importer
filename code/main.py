import sys

import pyutils

from object_types import UpdatableActivity,set_new_description

iJsonFile="/opt/strava_data_importer/config/secret/secret.json"

_logger=pyutils.Logger(log_path="/opt/strava_data_importer/log/strava.log")

def get_secrets_config():
    global json_data
    global iClientId
    global iClientSecret
    global iAccessToken
    global iRefreshToken

    json_data=pyutils.get_json_data(iJsonFile)
    secrets=json_data["secrets"]

    iCategory=secrets["category"]
    iClub=secrets["club"]
    iClientId=secrets["client"]["id"]
    iClientSecret=secrets["client"]["secret"]
    iAccessToken=secrets["token"]["access"]
    iRefreshToken=secrets["token"]["refresh"]

def get_last_activity() -> list:
    # List Athlete Activities
    iUrl="https://www.strava.com/api/v3/athlete/activities?"

    before=pyutils.GetEpochTimestamp()
    before_date=pyutils.Timestamp2Date(before)
    year=before_date.year
    month=before_date.month
    day=before_date.day
    after=pyutils.GetEpochTimestamp(aDate=(2025,6,29,0,0,0))

    page=1
    per_page=30
    iParams=[("before",before),("after",after),("page",page),("per_page",per_page)]
    iHeaders={"Authorization":"Bearer "+str(iAccessToken)}

    iRet=pyutils.getJsonData(aUrl=iUrl,aParams=iParams,aHeaders=iHeaders)

    return iRet

def refresh_token():
    # Refresh token
    iUrl="https://www.strava.com/oauth/token"
    iData={
        "client_id":iClientId,
        "client_secret":iClientSecret,
        "grant_type":"refresh_token",
        "refresh_token":iRefreshToken
    }
    
    iRet=pyutils.postJsonData(aUrl=iUrl,aData=iData)
    
    # If there is no info about the scope, the user needs to reauthorize
    if iRet.get("scope",None)==None:
        _logger.info("User needs to reauthorize")

    iNewAccessToken=iRet["access_token"]

    # update config json
    iNewConfig=json_data
    iNewConfig["secrets"]["token"]["access"]=iNewAccessToken

    iJsonConfig=pyutils.dict2json(iNewConfig)
    pyutils.writeFile(iJsonFile,iJsonConfig)

    global iAccessToken
    iAccessToken=iNewAccessToken

def update_activity(iAct):
    iUpdAct=UpdatableActivity(iAct)

    # Get relevant athlete info
    iUrl="https://www.strava.com/api/v3/athletes/{id}/stats"
    iUrl=iUrl.format(id=iUpdAct.athlete_id)
    iHeaders={"Authorization":"Bearer "+str(iAccessToken)}
    iRet=pyutils.getJsonData(aUrl=iUrl,aHeaders=iHeaders)
    
    # Put that data in the updatable activity
    set_new_description(aAct=iUpdAct,aAthleteInfo=iRet)

    # Post to strava
    iUrl="https://www.strava.com/api/v3/activities/{id}"
    iUrl=iUrl.format(id=iUpdAct.id)
    iHeaders={"Authorization":"Bearer "+str(iAccessToken)}
    iData=iUpdAct.json()
    
    iRet=pyutils.putJsonData(aUrl=iUrl,aHeaders=iHeaders,aData=iData)
    _logger.debug(pyutils.dict2json(iRet))

if __name__=="__main__":
    get_secrets_config()

    refresh_token()
    iLastAct=get_last_activity()
    
    if iLastAct==[]: sys.exit() # break execution if there are no activities
    for i in iLastAct:
        update_activity(i)

    sys.exit()
