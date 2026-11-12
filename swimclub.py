#Import statistics module for calculating mean
import statistics
#Import custom utility module for helper functions
import hfpy_utils
#Folder containing swim data files
FOLDER = 'swimdata/'
#Function to read swim data from a file
def read_swim_data(filename):
    """Read swim data from a file and return swimmer details and average time.
    
    Args:
        filename (str): Name of the swim data file.

    Returns:
        tuple: Swimmer details (name, age, distance, stroke), list of times, and average time.
    """
    swimmer,age,distance,stroke = filename.removesuffix(".txt").split("-")    
    with open(FOLDER + filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(',')
    converts=[]
    for t in times:
        # The minutes value might be missing if the time is less than a minute
        if ':' in t:
            minutes, rest = t.split(':')
            seconds,hundreth=rest.split('.')
        else:
            minutes = 0
            seconds,hundreth=t.split('.')            
        converted_time=(int(minutes)*60*100)+int(seconds)*100+int(hundreth)
        converts.append(converted_time)    
    average=statistics.mean(converts)
    #mins_secs,hundreths=str(round(average/100,2)).split('.')
    mins_secs,hundreths=f"{(average/100):.2f}".split('.')
    mins_secs=int(mins_secs)
    minutes=mins_secs//60
    seconds=mins_secs - minutes*60
    # Using string formatting to create the average time as "minutes:seconds.hundreths"
    #average=str(minutes)+":"+str(seconds)+"."+hundreths
     # Using f-string to format the average time as "minutes:seconds.hundreths"
    average=f"{minutes}:{seconds:0>2}.{hundreths}"
    #Returned as tuple containing swimmer details, list of times, and average time
    return swimmer, age, distance, stroke, times, average, converts

CHARTS="charts/"
def produce_bar_chart(fn):
    """Given the name of a swimmer's file, produce a HTML/SVG based bar chart.
    
    Save the chart to the CHARTS folder. Return the path to the bar chart file."""
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)    
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under-{age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                <html>
                    <head>
                        <title>{title}</title>
                    </head>
                    <body>
                    <h3>{title}</h3>"""
    body = ""
    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body + f"""
                    <svg height="30" width="400">
                        <rect height="30" width={bar_width} style="fill:rgb(0,0,255);" />
                    </svg>{t}<br />"""
    footer=f"""
                <p>Average time: {average}</p>    
            </body>
            </html>"""
    page= header + body + footer
    save_to = f"{CHARTS} {fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)

    return save_to