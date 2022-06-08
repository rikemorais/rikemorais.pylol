import pandas as pd
from database import api


# API
def datadragon():
    data = api.rgapi()
    filters = data.filter(
        items=[
            'championId',
            'championLevel',
            'championPoints',
            'championPointsUntilNextLevel',
        ]
    )
    rename = filters.rename(
        columns={
            'championId': 'ID',
            'championLevel': 'Level',
            'championPoints': 'Points',
            'championPointsUntilNextLevel': 'Next',
        }
    )
    champions =  pd.read_json("champions.json")
    join = rename.join(champions.set_index("ID"), on="ID", how="left")
    return join
