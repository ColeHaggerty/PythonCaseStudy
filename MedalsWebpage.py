import sqlite3

contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<style>
table {
    border-spacing: 0;
    width: 100%;
    border: 1px solid #ddd;
}

th {
    cursor: pointer;
}

th, td {
    text-align: left;
    padding: 16px;
}

tr:nth-child(even) {
    background-color: #f2f2f2
}
</style>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>2018 Winter Olympic Medal Count</title>
</head>
<body>

<p><strong>2018 Winter Olympics Medal Count</strong></p>

<table>
<table id="myTable">
  <tr>
   <!--When a header is clicked, run the sortTable function, with a parameter, 0 for sorting by names, 1 for sorting by country:-->  

    <th onclick="sortTableNum(0)">Rank</th>
    <th onclick="sortTableAlph(1)">NOC</th>
    <th onclick="sortTableNum(2)">Gold</th>
    <th onclick="sortTableNum(3)">Silver</th>
    <th onclick="sortTableNum(4)">Bronze</th>
    <th onclick="sortTableNum(5)">Total</th>

    
  
$TableData

</table>
<script>

function sortTableAlph(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc"; 
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function sortTableNum(n) {
var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
table = document.getElementById("myTable");
switching = true;
//Set the sorting direction to ascending:
dir = "asc"; 
 while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/

      if (dir == "asc") {
        if (Number(x.innerHTML) > Number(y.innerHTML)) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (Number(x.innerHTML) < Number(y.innerHTML)) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
            if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>

</body>
</html>
'''

def get_table_data():
    sql_get_data = """ SELECT * FROM OlympicMedals """
    conn = sqlite3.connect("./OlympicMedals.db")
    c = conn.cursor()
    return c.execute(sql_get_data).fetchall()
     

def build_table_rows(table_data):
    TR_OPEN = "<tr>"
    TR_CLOSE = "</tr>"
    TD_OPEN = "<td>"
    TD_CLOSE = "</td>"

    table_rows = ""

    for row in table_data:
        tmp_str = TR_OPEN
        for data in row:
            tmp_str += (TD_OPEN + str(data) + TD_CLOSE)
        tmp_str += (TR_CLOSE)
        table_rows += (tmp_str)

    return table_rows

def main():
    browseLocal(contents.replace("$TableData", build_table_rows(get_table_data())))

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='tempBrowseLocal.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename))

main()