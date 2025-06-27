import sys
from pyutils import dict2json

class UpdatableActivity:
    def __init__(self,aActivity:dict):
        self.iAct=aActivity

        self.set_vars()
    def set_vars(self):
        self.id=self.iAct["id"]
        self.commute=self.iAct["commute"]
        self.trainer=self.iAct["trainer"]
        self.hide_from_home=False
        self.description=""
        self.name=self.iAct["name"]
        self.sport_type=self.iAct["sport_type"]
        self.gear_id=self.iAct["gear_id"]
        
        # The following attributes are not meant to be included in the json
        self.athlete_id=self.iAct["athlete"]["id"]
    def json(self):
        """
        contains:
            id
            commute
            trainer
            hide_from_home
            description
            name
            sport_type:
                instance of sporttype
            gear_id
        """
        try:
            iDic={}
            iDic["id"]=self.id
            iDic["commute"]=self.commute
            iDic["trainer"]=self.trainer
            iDic["hide_from_home"]=self.hide_from_home
            iDic["description"]=self.description
            iDic["name"]=self.name
            iDic["sport_type"]=self.sport_type
            iDic["gear_id"]=self.gear_id
        
            iJson=dict2json(iDic)
            return iJson
        except Exception as e:
            err="Error in UpdatableActivity.json function. Error: "
            err+=str(e)+" : "+str(sys.exc_info())
            raise Exception(err)

def set_new_description(aAct:UpdatableActivity,aAthleteInfo:dict):
    bike=[
        "EBikeRide","EMountainBikeRide","GravelRide","MountainBikeRide"
        ,"Ride","VirtualRide"
    ]
    run=["Run","TrailRun","VirtualRun"]
    swim=["Swim"]

    if aAct.sport_type in bike: iKey="ytd_ride_totals"
    elif aAct.sport_type in run: iKey="ytd_run_totals"
    elif aAct.sport_type in swim: iKey="ytd_swim_totals"
    else: return
    
    iDic={}
    iDic["count"]=aAthleteInfo[iKey]["count"]
    iDic["distance"]=formatNumber(aAthleteInfo[iKey]["distance"])
    iDic["elapsed_time"]=formatTime(aAthleteInfo[iKey]["elapsed_time"])
    iDic["elevation_gain"]=formatNumber(aAthleteInfo[iKey]["elevation_gain"])

    iDesc="Year Totals"
    iDesc+="\n    Distance: {dst} km".format(dst=iDic["distance"])
    iDesc+="\n    Time: {tm} h".format(tm=iDic["elapsed_time"])
    iDesc+="\n    Elevation Gain: {eg} m".format(eg=iDic["elevation_gain"])
    iDesc+="\n\nPowerd by My App"
    iDesc+="\nhttps://github.com/Joan-Frago/strava_data_importer"
    
    aAct.description=iDesc

def formatNumber(a:int|float) -> str:
    b=str(a)[::-1]
    c=""
    cnt=0
    for i in b:
        if i==".": cnt=-1
        if cnt==3 or cnt==6 or cnt==9 or cnt==12: c+="."
        c+=i
        cnt+=1
    return c[::-1]

def formatTime(a:int|float) -> str:
    b=a/3600
    b=round(b,2)
    return str(b)

