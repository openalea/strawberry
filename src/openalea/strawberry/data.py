""" Module providing shared data access
"""
from pathlib import Path

from openalea.deploy.shared_data import shared_data
import openalea.strawberry


data_directory = shared_data(openalea.strawberry.__path__)
count = 0
d = Path(openalea.strawberry.__path__[0])
while data_directory is None and count <=3:
    d = d/'..'
    data_directory = shared_data(d)
    count+=1

