#!/usr/bin/python3
# %%

#get pdf
from pathlib import Path
import requests

#parse pdf
import camelot

class KitCasinoSpeiseplan:
    def __init__(self):
        self.urlDeutsch='https://www.aserv.kit.edu/downloads/VAM-CAT/Speiseplan_deutsch.pdf'
        self.filenameDeutsch='speiseplanDeutsch.pdf'

    def downloadSpeiseplan(self):
        filename = Path(self.filenameDeutsch)
        response = requests.get(self.urlDeutsch)
        filename.write_bytes(response.content)

    def readSpeiseplan(self):
        table = camelot.read_pdf(self.filenameDeutsch,flavor='stream')
        self.speiseplanRaw=table[0].df

if __name__ == "__main__":
    speiseplan=KitCasinoSpeiseplan()
    speiseplan.readSpeiseplan()

    df=speiseplan.speiseplanRaw

# %%
print(df)





# %%
df[0].tolist()
# %%
