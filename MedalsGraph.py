import sqlite3
import matplotlib.pyplot as plt
import matplotlib.style as style


conn = sqlite3.connect("./OlympicMedals.db")
c = conn.cursor()

def Graph_Medals():
    c.execute("""SELECT NOC, Gold, Silver, Bronze 
                 FROM OlympicMedals
                 ORDER BY Rank Asc
                 LIMIT 10
                    """)
    NOC = []
    Gold = []
    Silver = []
    Bronze = []
    data = c.fetchall()
    for row in data:     
        Name = row[0].strip().split("(")[0]
        NOC.append(Name)
        Gold.append(row[1])
        Silver.append(row[2])
        Bronze.append(row[3])
#Plot graph
    plt.plot(NOC, Gold, color='gold',marker='o')
    plt.plot(NOC, Silver, color='silver',marker='o')
    plt.plot(NOC, Bronze,color= 'darkgoldenrod',marker='o')
    plt.xticks(rotation=45)
    plt.legend(['Gold', 'Silver', 'Bronze'], loc='best')
    plt.margins(0,.1)
    plt.show()

Graph_Medals()
