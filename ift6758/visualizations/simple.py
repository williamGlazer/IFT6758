import pandas as pd

class NHLSimpleVisualization:
    """
    Class to create simple visualizations from pandas dataframes created
    with NHLCleaner
    """
    
    pd = None
    
    def __init__(self, pd: pd.DataFrame) -> None:
        self.pd = pd
    
    def shot_types() -> None:
        