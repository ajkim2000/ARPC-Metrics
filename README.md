# ARPC-Metrics

metrics("Name of Column to Analyze") : Attains necessary information pertaining to passed in "Column"
    Example: asc = metrics("ASSIGNED_SUPPORT_COMPANY")  
             asc -> Represents DataFrame returned by function, holds all necessary data pertaining to "ASSIGNED_SUPPORT_COMPANY"

visualizeV(DataFrame, "Name of Column to Analyze", "Name of Metric", Boolean Value) : Creates visualization vertical bar graph of passed in metric and data
        DataFrame: DataFrame returned by the previous metrics() function
        "Name of Column to Analyze": Desired Column from data
        "Name of Metric": Desired form of metric, the two default values are as follows : 
                          "Average_Time" - Metric for average time until ticket is resolved/closed per Column value.
                          "Total_Tickets" - Metric for total tickets resolved/closed per Column value.
        Boolean Value: True/False values passed in to decide whether bar graph should be sorted in ascending order (True) or unsorted (False)
    Exampe: visualizeV(asg, "ASSIGNED_GROUP", "Total_Tickets", False)
    Above call will create vertical bar graph showing "Total_Tickets" per element in "ASSIGNED_GROUP" with unsorted bars (False)

visualizeH(DataFrame, "Name of Column to Analyze", "Name of Metric", Boolean Value) : Creates visualization horizontal bar graph of passed in metric and data
        DataFrame: DataFrame returned by the previous metrics() function
        "Name of Column to Analyze": Desired Column from data
        "Name of Metric": Desired form of metric, the two default values are as follows : 
                          "Average_Time" - Metric for average time until ticket is resolved/closed per Column value.
                          "Total_Tickets" - Metric for total tickets resolved/closed per Column value.
        Boolean Value: True/False values passed in to decide whether bar graph should be sorted in ascending order (True) or sorted in descending order (False)
    Exampe: visualizeH(asg, "ASSIGNEE", "Total_Tickets", True)
    Above call will create horizontal bar graph showing "Total_Tickets" per element in "ASSIGNEE" with sorted bars in ascending order(True)
       
visualizeTime() : Analyzes and finds overall time frame of given data. Creates horizontal bar graph ticket age statistics in found time frame (0-30 days old, 31-60 days old, 61-more)
