# Sportfishing Hauls Scraper
 Scrapes data from San Diego's Independence Sportfishing, 
 who posts catch reports from deep sea fishing trips such 
 [as this](http://www.independencesportfishing.com/detailed_report.php?report_id=168239), then scrapes data from weather underground's San Diego Airport location.
 
 ## Interface
 
 There is a long way and a short way to use this repo. You can replicate what I did here
 by setting up your own MySQL database and populating it using my tools, or use my checkpointed data in the CSV
  by reading `raw_fishing_data.csv`.
 
 
 #### The short way
 If you don't want to scrape the data again, I've dumped the data as of December 20th, 2020. It can be accessed like,

```
import pandas as pd
pd.read_csv("raw_fishing_data.csv")
```

or simply read into excel or your spreadsheet tool of choice.

 #### The long way
 This involves making a mysql database and waiting a couple days to scrape the data.
 
 \# TODO: Documentation of running the scrapers and populating the database
 
 The populated MySQL database can be queried easily into a pandas object like,
 ```python
from db_utils.db_queries import sql_all_reports_with_weather
from db_utils.mysql_db_connection import get_mysql_connection

db = get_mysql_connection()
fishing_data = sql_all_reports_with_weather(db)
fishing_data.head(3)
```

yielding a table with a schema like:

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date_posted</th>
      <th>headline</th>
      <th>post_body</th>
      <th>low_temp</th>
      <th>avg_temp</th>
      <th>high_temp</th>
      <th>inches_precip</th>
      <th>miles_visible</th>
      <th>max_wind</th>
      <th>sea_pressure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2020-12-17</td>
      <td>ON THE HUNT</td>
      <td>We were on the hunt for Yellowtail today but never able to connect. We...</td>
      <td>46.0</td>
      <td>57.34</td>
      <td>64.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>10.0</td>
      <td>30.08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020-12-18</td>
      <td>SCRATCHING AWAY</td>
      <td>Searched for Yellowtail again today to find non biters. Good action on bass, ...</td>
      <td>52.0</td>
      <td>58.04</td>
      <td>66.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>9.0</td>
      <td>30.23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2020-12-16</td>
      <td>GOOD ACTION</td>
      <td>Another good day of fishing for the guys. It was slow...</td>
      <td>43.0</td>
      <td>56.38</td>
      <td>72.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>9.0</td>
      <td>30.17</td>
    </tr>
  </tbody>
</table>

