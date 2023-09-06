import os
import pandas as pd 
from sweep_line import *

def from_csv_2_segments(file: str = "segmentos.csv") -> List[Segment]:
    #dataframe with columns x0, y0, x1, y1
    dir_ = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(dir_, file))
    segments = []

    for index, row in df.iterrows():
        start = Vector(np.array([[row["x0"]], [row["y0"]]]))
        end = Vector(np.array([[row["x1"]], [row["y1"]]]))
        segments.append(Segment(start, end, sort_ends=True))
    return segments

custom_test_segments = from_csv_2_segments()
SweepLine(custom_test_segments).run(plotting=True)