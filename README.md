# Texas A&M Football Recruits Web Scrape Project
 
With football season around the corner I figured it would be intersting to see where all the recruits are coming from. If you went to Texas A&M you can make a pretty good guess where the recruits are coming from, looking at you Houston, but there was a suprising amopunt of recruits from all over.

This data was taken direcxtly from teh A&M football page and placed into my SQL server wghere it is housed and presented using tableau. The Website unfortunaly decided to change the formatting of their data just about every year so the code might look a little overkill but unfortunaly this is what it required.

My script first opens the main page and collects the links associated with all of the players, with a few years as the exceptions due to a change in formatting. After links are collected the script will upen up each link and scrpae the data from that specific player, the scraped data is then processed and sent to the SQL server. The data is sent to the server after every year so that if the format changed the data it did collect will not be lost if the script fails.

Below is the Dashboard created in Tableau to present the data, here you can see the hotspots of the recruiting along with the top schools, average height, average weight, and the top position.

<hr size="" width="" color="" >  

<div class='tableauPlaceholder' id='viz1661186175878' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Te&#47;TexasAMFootballRecruits&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TexasAMFootballRecruits&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Te&#47;TexasAMFootballRecruits&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                
https://public.tableau.com/views/TexasAMFootballRecruits/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link
