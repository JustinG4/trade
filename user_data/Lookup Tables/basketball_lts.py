# lookup tables for web scraping

team_lt = {
   "Boston Celtics":"/nba/team/_/name/bos/boston-celtics",
   "Brooklyn Nets":"/nba/team/_/name/bkn/brooklyn-nets",
   "New York Knicks":"/nba/team/_/name/ny/new-york-knicks",
   "Philadelphia 76ers":"/nba/team/_/name/phi/philadelphia-76ers",
   "Toronto Raptors":"/nba/team/_/name/tor/toronto-raptors",
   "Chicago Bulls":"/nba/team/_/name/chi/chicago-bulls",
   "Cleveland Cavaliers":"/nba/team/_/name/cle/cleveland-cavaliers",
   "Detroit Pistons":"/nba/team/_/name/det/detroit-pistons",
   "Indiana Pacers":"/nba/team/_/name/ind/indiana-pacers",
   "Milwaukee Bucks":"/nba/team/_/name/mil/milwaukee-bucks",
   "Denver Nuggets":"/nba/team/_/name/den/denver-nuggets",
   "Minnesota Timberwolves":"/nba/team/_/name/min/minnesota-timberwolves",
   "Oklahoma City Thunder":"/nba/team/_/name/okc/oklahoma-city-thunder",
   "Portland Trail Blazers":"/nba/team/_/name/por/portland-trail-blazers",
   "Utah Jazz":"/nba/team/_/name/utah/utah-jazz",
   "Golden State Warriors":"/nba/team/_/name/gs/golden-state-warriors",
   "LA Clippers":"/nba/team/_/name/lac/la-clippers",
   "Los Angeles Lakers":"/nba/team/_/name/lal/los-angeles-lakers",
   "Phoenix Suns":"/nba/team/_/name/phx/phoenix-suns",
   "Sacramento Kings":"/nba/team/_/name/sac/sacramento-kings",
   "Atlanta Hawks":"/nba/team/_/name/atl/atlanta-hawks",
   "Charlotte Hornets":"/nba/team/_/name/cha/charlotte-hornets",
   "Miami Heat":"/nba/team/_/name/mia/miami-heat",
   "Orlando Magic":"/nba/team/_/name/orl/orlando-magic",
   "Washington Wizards":"/nba/team/_/name/wsh/washington-wizards",
   "Dallas Mavericks":"/nba/team/_/name/dal/dallas-mavericks",
   "Houston Rockets":"/nba/team/_/name/hou/houston-rockets",
   "Memphis Grizzlies":"/nba/team/_/name/mem/memphis-grizzlies",
   "New Orleans Pelicans":"/nba/team/_/name/no/new-orleans-pelicans",
   "San Antonio Spurs":"/nba/team/_/name/sa/san-antonio-spurs"
}


def getTeamLink(team):
    return team_lt[team]


stats_lt = {
   "Boston Celtics":"/nba/team/stats/_/name/bos/boston-celtics",
   "Brooklyn Nets":"/nba/team/stats/_/name/bkn/brooklyn-nets",
   "New York Knicks":"/nba/team/stats/_/name/ny/new-york-knicks",
   "Philadelphia 76ers":"/nba/team/stats/_/name/phi/philadelphia-76ers",
   "Toronto Raptors":"/nba/team/stats/_/name/tor/toronto-raptors",
   "Chicago Bulls":"/nba/team/stats/_/name/chi/chicago-bulls",
   "Cleveland Cavaliers":"/nba/team/stats/_/name/cle/cleveland-cavaliers",
   "Detroit Pistons":"/nba/team/stats/_/name/det/detroit-pistons",
   "Indiana Pacers":"/nba/team/stats/_/name/ind/indiana-pacers",
   "Milwaukee Bucks":"/nba/team/stats/_/name/mil/milwaukee-bucks",
   "Denver Nuggets":"/nba/team/stats/_/name/den/denver-nuggets",
   "Minnesota Timberwolves":"/nba/team/stats/_/name/min/minnesota-timberwolves",
   "Oklahoma City Thunder":"/nba/team/stats/_/name/okc/oklahoma-city-thunder",
   "Portland Trail Blazers":"/nba/team/stats/_/name/por/portland-trail-blazers",
   "Utah Jazz":"/nba/team/stats/_/name/utah/utah-jazz",
   "Golden State Warriors":"/nba/team/stats/_/name/gs/golden-state-warriors",
   "LA Clippers":"/nba/team/stats/_/name/lac/la-clippers",
   "Los Angeles Lakers":"/nba/team/stats/_/name/lal/los-angeles-lakers",
   "Phoenix Suns":"/nba/team/stats/_/name/phx/phoenix-suns",
   "Sacramento Kings":"/nba/team/stats/_/name/sac/sacramento-kings",
   "Atlanta Hawks":"/nba/team/stats/_/name/atl/atlanta-hawks",
   "Charlotte Hornets":"/nba/team/stats/_/name/cha/charlotte-hornets",
   "Miami Heat":"/nba/team/stats/_/name/mia/miami-heat",
   "Orlando Magic":"/nba/team/stats/_/name/orl/orlando-magic",
   "Washington Wizards":"/nba/team/stats/_/name/wsh/washington-wizards",
   "Dallas Mavericks":"/nba/team/stats/_/name/dal/dallas-mavericks",
   "Houston Rockets":"/nba/team/stats/_/name/hou/houston-rockets",
   "Memphis Grizzlies":"/nba/team/stats/_/name/mem/memphis-grizzlies",
   "New Orleans Pelicans":"/nba/team/stats/_/name/no/new-orleans-pelicans",
   "San Antonio Spurs":"/nba/team/stats/_/name/sa/san-antonio-spurs"
}


def getStatsLink(team):
    return stats_lt[team]


team_lt = {
   "Boston Celtics":"/nba/team/roster/_/name/bos/boston-celtics",
   "Brooklyn Nets":"/nba/team/roster/_/name/bkn/brooklyn-nets",
   "New York Knicks":"/nba/team/roster/_/name/ny/new-york-knicks",
   "Philadelphia 76ers":"/nba/team/roster/_/name/phi/philadelphia-76ers",
   "Toronto Raptors":"/nba/team/roster/_/name/tor/toronto-raptors",
   "Chicago Bulls":"/nba/team/roster/_/name/chi/chicago-bulls",
   "Cleveland Cavaliers":"/nba/team/roster/_/name/cle/cleveland-cavaliers",
   "Detroit Pistons":"/nba/team/roster/_/name/det/detroit-pistons",
   "Indiana Pacers":"/nba/team/roster/_/name/ind/indiana-pacers",
   "Milwaukee Bucks":"/nba/team/roster/_/name/mil/milwaukee-bucks",
   "Denver Nuggets":"/nba/team/roster/_/name/den/denver-nuggets",
   "Minnesota Timberwolves":"/nba/team/roster/_/name/min/minnesota-timberwolves",
   "Oklahoma City Thunder":"/nba/team/roster/_/name/okc/oklahoma-city-thunder",
   "Portland Trail Blazers":"/nba/team/roster/_/name/por/portland-trail-blazers",
   "Utah Jazz":"/nba/team/roster/_/name/utah/utah-jazz",
   "Golden State Warriors":"/nba/team/roster/_/name/gs/golden-state-warriors",
   "LA Clippers":"/nba/team/roster/_/name/lac/la-clippers",
   "Los Angeles Lakers":"/nba/team/roster/_/name/lal/los-angeles-lakers",
   "Phoenix Suns":"/nba/team/roster/_/name/phx/phoenix-suns",
   "Sacramento Kings":"/nba/team/roster/_/name/sac/sacramento-kings",
   "Atlanta Hawks":"/nba/team/roster/_/name/atl/atlanta-hawks",
   "Charlotte Hornets":"/nba/team/roster/_/name/cha/charlotte-hornets",
   "Miami Heat":"/nba/team/roster/_/name/mia/miami-heat",
   "Orlando Magic":"/nba/team/roster/_/name/orl/orlando-magic",
   "Washington Wizards":"/nba/team/roster/_/name/wsh/washington-wizards",
   "Dallas Mavericks":"/nba/team/roster/_/name/dal/dallas-mavericks",
   "Houston Rockets":"/nba/team/roster/_/name/hou/houston-rockets",
   "Memphis Grizzlies":"/nba/team/roster/_/name/mem/memphis-grizzlies",
   "New Orleans Pelicans":"/nba/team/roster/_/name/no/new-orleans-pelicans",
   "San Antonio Spurs":"/nba/team/roster/_/name/sa/san-antonio-spurs"
}


def getRosterLink(team):
    return roster_lt[team]

