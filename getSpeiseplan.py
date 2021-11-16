#!/usr/bin/python3
# %%

#get pdf
from pathlib import Path
import requests
import fitz
import cv2
import pytesseract
from EasyROI import EasyROI
import pickle

days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

class KitCasinoSpeiseplan:
    
    def __init__(self):
        self.urlDeutsch='https://www.aserv.kit.edu/downloads/VAM-CAT/Speiseplan_deutsch.pdf'
        self.filenameDeutsch='speiseplanDeutsch.pdf'
        self.image=None

    def convertToImage(self):
        doc = fitz.open(self.filenameDeutsch)
        page = doc.loadPage(0)
        pix = page.getPixmap(matrix=fitz.Matrix(1.5, 1.5))
        pix.writePNG(f"{self.filenameDeutsch}.png")
        self.image=cv2.imread(f"{self.filenameDeutsch}.png")

    def setRois(self):
        roi_helper = EasyROI(verbose=True)
        self.rois=dict()
        for day in days:
            print(f"Please select ROIs for {day}...")
            rois_day = roi_helper.draw_rectangle(self.image, 5)
            self.rois[day]=rois_day
        with open('rois.pickle', 'wb') as handle:
            pickle.dump(self.rois, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def getRois(self):
        with open('rois.pickle', 'rb') as handle:
            self.rois = pickle.load(handle)

    def downloadSpeiseplan(self):
        filename = Path(self.filenameDeutsch)
        response = requests.get(self.urlDeutsch)
        filename.write_bytes(response.content)
        self.convertToImage()

    def parseSpeiseplan(self):
        for day in days:
            roi=self.rois[day]
            for i in range(5):
                x=roi["roi"][i]["tl_x"]
                y=roi["roi"][i]["tl_y"]
                w=roi["roi"][i]["w"]
                h=roi["roi"][i]["h"]
                essen=pytesseract.image_to_string(self.image[y:y+h,x:x+w],lang='deu')
                print(f"Essen({day}, {i}): {essen}")


if __name__ == "__main__":
    speiseplan=KitCasinoSpeiseplan()
    speiseplan.downloadSpeiseplan()
    speiseplan.getRois()
    speiseplan.parseSpeiseplan()
# %%
