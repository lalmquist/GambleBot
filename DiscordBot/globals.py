import json

global Members
global GambleHistory

with open('Members.json') as f:
    Members = json.load(f)

with open('GambleHistory.json') as f:
    GambleHistory = json.load(f)