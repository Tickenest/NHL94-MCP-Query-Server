\# NHL '94 Database Schema



\## General Notes

\- There are two databases: GENS and SNES. Their schemas are mostly identical,

&#x20; except that the skaters and goalies tables in gensDatabase.db contain additional

&#x20; columns (toi), the matches table in gensDatabase.db contains additional columns

&#x20; (homefchecks, homedchecks, awayfchecks, awaydchecks), and the skaters table in

&#x20; gensDatabase.db contains additional columns (checks).

\- Use platform = "gens" or platform = "snes" when calling execute\_sql.

\- RegOrPlay: "R" = regular season game, "P" = playoff game.

\- Period 4 = overtime.

\- When a value can be either -1 or 1, -1 refers to the Away team and 1 refers to

&#x20; the Home team.

\- The goals and penalties tables contain denormalized context columns (league, datetime,

&#x20; hometeam, hometeamabbrev, homeplayer, awayteam, awayteamabbrev, awayplayer) that

&#x20; are copied from the matches table. When answering questions about goals or

&#x20; penalties, you can get game context directly from the goals or penalties table without

&#x20; joining to matches.

\---



\## Table: matches

One row represents one complete game.

Primary key: (match\_id, RegOrPlay)



| Column Name | Type | Description |

|---|---|---|

| matchid | INTEGER | Unique identifier for the game |

| regorplay | TEXT | "R" = regular season, "P" = playoff |

| league | TEXT | Name of the league season in which the game was played |

| datetime | TEXT | Date and time at which the game was played, in YYYY-MM-DD HH:MM:SS format |

| hometeam | TEXT | The long name of the home team |

| hometeamabbrev | TEXT | The 2-3 letter abbreviation of the home team name |

| homeplayer | TEXT | The name of the human who played as the home team |

| awayteam | TEXT | The long name of the away team |

| awayteamabbrev | TEXT | The 2-3 letter abbreviation of the away team name |

| awayplayer | TEXT | The name of the human who played as the away team |

| awayscore | INTEGER | The number of goals scored by the away team |

| awayshots | INTEGER | The number of shots by the away team |

| awayshootpct | REAL | The shooting percentage of the away team |

| awayppgoals | INTEGER | The number of power play goals scored by the away team |

| awaypptries | INTEGER | The number of power play tries by the away team |

| awayshgoals | INTEGER | The number of shorthanded goals scored by the away team |

| awaybreakgoals | INTEGER | The number of breakaway goals scored by the away team |

| awaybreaktries | INTEGER | The number of breakaway attempts by the away team |

| awayonetimergoals | INTEGER | The number of one-timer goals scored by the away team |

| awayonetimertries | INTEGER | The number of one-timer tries by the away team |

| awaypenshotgoals | INTEGER | The number of penalty shot goals scored by the away team |

| awaypenshottries | INTEGER | The number of penalty shot tries by the away team |

| awayfaceoffwins | INTEGER | The number of faceoff wins by the away team |

| awaychecks | INTEGER | The number of checks by the away team |

| awaypim | INTEGER | The number of penalties in minutes that the away team had |

| awayattackzonetime | INTEGER | The number of seconds of attack zone time that the away team had |

| awaypasscomps | INTEGER | The number of pass completions by the away team |

| awaypasstries | INTEGER | The number of pass attempts by the away team |

| awaygoalsp1 | INTEGER | The number of goals scored by the away team in period 1 |

| awayshotsp1 | INTEGER | The number of shots on goals by the away team in period 1 |

| awaygoalsp2 | INTEGER | The number of goals scored by the away team in period 2 |

| awayshotsp2 | INTEGER | The number of shots by the away team in period 2 |

| awaygoalsp3 | INTEGER | The number of goals scored by the away team in period 3 |

| awayshotsp3 | INTEGER | The number of shots by the away team in period 3 |

| awaygoalsot | REAL | The number of goals scored by the away team in overtime - is null if no overtime was played |

| awayshotsot | REAL | The number of shots by the away team in overtime - is null if no overtime was played |

| homescore | INTEGER | The number of goals scored by the home team |

| homeshots | INTEGER | The number of shots by the home team |

| homeshootpct | REAL | The shooting percentage of the home team |

| homeppgoals | INTEGER | The number of power play goals scored by the home team |

| homepptries | INTEGER | The number of power play tries by the home team |

| homeshgoals | INTEGER | The number of shorthanded goals scored by the home team |

| homebreakgoals | INTEGER | The number of breakhome goals scored by the home team |

| homebreaktries | INTEGER | The number of breakhome attempts by the home team |

| homeonetimergoals | INTEGER | The number of one-timer goals scored by the home team |

| homeonetimertries | INTEGER | The number of one-timer tries by the home team |

| homepenshotgoals | INTEGER | The number of penalty shot goals scored by the home team |

| homepenshottries | INTEGER | The number of penalty shot tries by the home team |

| homefaceoffwins | INTEGER | The number of faceoff wins by the home team |

| homechecks | INTEGER | The number of checks by the home team |

| homepim | INTEGER | The number of penalties in minutes that the home team had |

| homeattackzonetime | INTEGER | The number of seconds of attack zone time that the home team had |

| homepasscomps | INTEGER | The number of pass completions by the home team |

| homepasstries | INTEGER | The number of pass attempts by the home team |

| homegoalsp1 | INTEGER | The number of goals scored by the home team in period 1 |

| homeshotsp1 | INTEGER | The number of shots on goals by the home team in period 1 |

| homegoalsp2 | INTEGER | The number of goals scored by the home team in period 2 |

| homeshotsp2 | INTEGER | The number of shots by the home team in period 2 |

| homegoalsp3 | INTEGER | The number of goals scored by the home team in period 3 |

| homeshotsp3 | INTEGER | The number of shots by the home team in period 3 |

| homegoalsot | REAL | The number of goals scored by the home team in overtime - is null if no overtime was played |

| homeshotsot | REAL | The number of shots by the home team in overtime - is null if no overtime was played |

| db | INTEGER | The highest decibel level of crowd noise during the game |

| sim | INTEGER | 0 if the game was not a simmed result, 1 if the game was a simmed result |

| winningscore | INTEGER | The number of goals scored by the winning team, or by each team, if the game ended tied |

| losingscore | INTEGER | The number of goals scored by the losing team, or by each team, if the game ended tied |

| gameduration | INTEGER | The number of seconds that the game lasted |

| otgame | INTEGER | 1 if the game went into overtime, 0 if not |

| away0goalperiods | INTEGER | Number of periods in which the away team scored 0 goals |

| away1goalperiods | INTEGER | Number of periods in which the away team scored 1 goal |

| away2goalperiods | INTEGER | Number of periods in which the away team scored 2 goals |

| away3goalperiods | INTEGER | Number of periods in which the away team scored 3 goals |

| away4goalperiods | INTEGER | Number of periods in which the away team scored 4 goals |

| away5goalperiods | INTEGER | Number of periods in which the away team scored 5 goals |

| home0goalperiods | INTEGER | Number of periods in which the home team scored 0 goals |

| home1goalperiods | INTEGER | Number of periods in which the home team scored 1 goal |

| home2goalperiods | INTEGER | Number of periods in which the home team scored 2 goals |

| home3goalperiods | INTEGER | Number of periods in which the home team scored 3 goals |

| home4goalperiods | INTEGER | Number of periods in which the home team scored 4 goals |

| home5goalperiods | INTEGER | Number of periods in which the home team scored 5 goals |

| home0assistgoals | INTEGER | Number of goals with 0 assists scored by the home team |

| home1assistgoals | INTEGER | Number of goals with 1 assist scored by the home team |

| home2assistgoals | INTEGER | Number of goals with 2 assists scored by the home team |

| away0assistgoals | INTEGER | Number of goals with 0 assists scored by the away team |

| away1assistgoals | INTEGER | Number of goals with 1 assist scored by the away team |

| away2assistgoals | INTEGER | Number of goals with 2 assists scored by the away team |

| homep1pens | INTEGER | Number of penalties committed by the home team in period 1 |

| homep2pens | INTEGER | Number of penalties committed by the home team in period 2 |

| homep3pens | INTEGER | Number of penalties committed by the home team in period 3 |

| homeotpens | INTEGER | Number of penalties committed by the home team in overtime |

| awayp1pens | INTEGER | Number of penalties committed by the away team in period 1 |

| awayp2pens | INTEGER | Number of penalties committed by the away team in period 2 |

| awayp3pens | INTEGER | Number of penalties committed by the away team in period 3 |

| awayotpens | INTEGER | Number of penalties committed by the away team in overtime |

| homeinjuringpens | INTEGER | Number of Injuring penalties committed by the home team |

| awayinjuringpens | INTEGER | Number of Injuring penalties committed by the away team |

| neutralzonetime | INTEGER | Number of seconds of neutral zone time |

| homefgoals | INTEGER | Number of goals scored by home forwards |

| homefassists | INTEGER | Number of assists by home forwards |

| homefpoints | INTEGER | Number of points by home forwards |

| homefshots | INTEGER | Number of shots by home forwards |

| homedgoals | INTEGER | Number of goals scored by home defensemen |

| homedassists | INTEGER | Number of assists by home defensemen |

| homedpoints | INTEGER | Number of points by home defensemen |

| homedshots | INTEGER | Number of shots by home defensemen |

| awayfgoals | INTEGER | Number of goals scored by away forwards |

| awayfassists | INTEGER | Number of assists by away forwards |

| awayfpoints | INTEGER | Number of points by away forwards |

| awayfshots | INTEGER | Number of shots by away forwards |

| awaydgoals | INTEGER | Number of goals scored by away defensemen |

| awaydassists | INTEGER | Number of assists by away defensemen |

| awaydpoints | INTEGER | Number of points by away defensemen |

| awaydshots | INTEGER | Number of shots by away defensemen |

| meangamestate | REAL | A real number giving a general assessment of the overall game state. Positive = home advantage, negative = away advantage |

| minus5marginduration | INTEGER | Number of seconds for which the away team was winning by 5 or more goals |

| minus4marginduration | INTEGER | Number of seconds for which the away team was winning by 4 goals |

| minus3marginduration | INTEGER | Number of seconds for which the away team was winning by 3 goals |

| minus2marginduration | INTEGER | Number of seconds for which the away team was winning by 2 goals |

| minus1marginduration | INTEGER | Number of seconds for which the away team was winning by 1 goal |

| plus0marginduration | INTEGER | Number of seconds for which the game was tied |

| plus1marginduration | INTEGER | Number of seconds for which the home team was winning by 1 goal |

| plus2marginduration | INTEGER | Number of seconds for which the home team was winning by 2 goals |

| plus3marginduration | INTEGER | Number of seconds for which the home team was winning by 3 goals |

| plus4marginduration | INTEGER | Number of seconds for which the home team was winning by 4 goals |

| plus5marginduration | INTEGER | Number of seconds for which the home team was winning by 5 or more goals |

| numleadchanges | INTEGER | Number of times that the team in the lead changed |

| homelast1secondgoals | INTEGER | Number of goals scored by the home team in the last 1 second of a period |

| awaylast1secondgoals | INTEGER | Number of goals scored by the away team in the last 1 second of a period |

| homelast5secondgoals | INTEGER | Number of goals scored by the home team in the last 5 seconds of a period |

| awaylast5secondgoals | INTEGER | Number of goals scored by the away team in the last 5 seconds of a period |

| homelast10secondgoals | INTEGER | Number of goals scored by the home team in the last 10 seconds of a period |

| awaylast10secondgoals | INTEGER | Number of goals scored by the away team in the last 10 seconds of a period |

| homeclutchgoals | INTEGER | Number of clutch goals (final minute of period 3 to tie the game or take the lead) scored by the home team |

| awayclutchgoals | INTEGER | Number of clutch goals (final minute of period 3 to tie the game or take the lead) scored by the away team |

| homecoastingtime | INTEGER | Number of seconds of coasting time for the home team |

| awaycoastingtime | INTEGER | Number of seconds of coasting time for the away team |

| endcoastingseconds | INTEGER | Number of unbroken coasting seconds for the winning team at the end of the game |

| coastingtimemultiplier | REAL | Elo multiplier for the winning team based upon their number of endcoastingseconds |

| homegoals10secondcif | INTEGER | Goals scored within 10 seconds of a center ice faceoff by the home team |

| awaygoals10secondcif | INTEGER | Goals scored within 10 seconds of a center ice faceoff by the away team |

| homegoals20secondcif | INTEGER | Goals scored within 20 seconds of a center ice faceoff by the home team |

| awaygoals20secondcif | INTEGER | Goals scored within 20 seconds of a center ice faceoff by the away team |

| homegoals30secondcif | INTEGER | Goals scored within 30 seconds of a center ice faceoff by the home team |

| awaygoals30secondcif | INTEGER | Goals scored within 30 seconds of a center ice faceoff by the away team |

| homegoalsafterp1 | INTEGER | Home team's score at the end of period 1 |

| homegoalsafterp2 | INTEGER | Home team's score at the end of period 2 |

| homegoalsafterp3 | INTEGER | Home team's score at the end of period 3 |

| awaygoalsafterp1 | INTEGER | Away team's score at the end of period 1 |

| awaygoalsafterp2 | INTEGER | Away team's score at the end of period 2 |

| awaygoalsafterp3 | INTEGER | Away team's score at the end of period 3 |

| marginafterp1 | INTEGER | The difference in goals scored by the two teams after period 1 (positive = home team leads, negative = away team leads) |

| marginafterp2 | INTEGER | The difference in goals scored by the two teams after period 2 (positive = home team leads, negative = away team leads) |

| marginafterp3 | INTEGER | The difference in goals scored by the two teams after period 3 (positive = home team leads, negative = away team leads) |

| homelargestlead | INTEGER | The size of the largest lead held by the home team at any time |

| awaylargestlead | INTEGER | The size of the largest lead held by the away team at any time |

| largestdeficitovercome | INTEGER | The largest deficit overcome by either team to tie the game |

| homelargestleadthentied | INTEGER | The largest lead that the home team held that the away team overcame to tie the game at some point |

| awaylargestleadthentied | INTEGER | The largest lead that the away team held that the home team overcame to tie the game at some point |

| homestomp | INTEGER | 1 if the home team achieved a stomp, 0 if not |

| awaystomp | INTEGER | 1 if the away team achieved a stomp, 0 if not |

| hometacos | INTEGER | 1 if the home team scored at least 10 goals in the game, 0 if not |

| awaytacos | INTEGER | 1 if the away team scored at least 10 goals in the game, 0 if not |

| homelongestgoalstreak | INTEGER | Longest streak of goals scored only by the home team in the game |

| awaylongestgoalstreak | INTEGER | Longest streak of goals scored only by the away team in the game |

| homewiretowirewin | INTEGER | 1 if the home team won 1-0 or took a 2-0 lead and never trailed, 0 if not |

| awaywiretowirewin | INTEGER | 1 if the away team won 1-0 or took a 2-0 lead and never trailed, 0 if not |

| tiedduringp2 | INTEGER | 1 if the game was tied at any point during period 2, 0 if not |

| tiedduringp3 | INTEGER | 1 if the game was tied at any point during period 3, 0 if not |

| homequickest3goals | INTEGER | The minimum number of seconds elapsed across all rolling 3-goal windows of home team goals |

| awayquickest3goals | INTEGER | The minimum number of seconds elapsed across all rolling 3-goal windows of away team goals |

| homequickest4goals | INTEGER | The minimum number of seconds elapsed across all rolling 4-goal windows of home team goals |

| awayquickest4goals | INTEGER | The minimum number of seconds elapsed across all rolling 4-goal windows of home team goals |

| homequickest5goals | INTEGER | The minimum number of seconds elapsed across all rolling 5-goal windows of home team goals |

| awayquickest5goals | INTEGER | The minimum number of seconds elapsed across all rolling 5-goal windows of home team goals |

| upgoals | INTEGER | Number of goals scored in the up direction |

| downgoals | INTEGER | Number of goals scored in the down direction |

| homeupgoals | INTEGER | Number of goals scored by the home team in the up direction |

| awayupgoals | INTEGER | Number of goals scored by the away team in the up direction |

| homedowngoals | INTEGER | Number of goals scored by the home team in the down direction |

| awaydowngoals | INTEGER | Number of goals scored by the away team in the down direction |

| upshots | REAL | Number of shots in the up direction |

| downshots | REAL | Number of shots in the down direction |

| homeupshots | INTEGER | Number of shots by the home team in the up direction |

| awayupshots | INTEGER | Number of shots by the away team in the up direction |

| homedownshots | INTEGER | Number of shots by the home team in the down direction |

| awaydownshots | INTEGER | Number of shots by the away team in the down direction |

| otduration | INTEGER | Number of seconds of the duration of overtime - null if overtime was not played |

| homeuptime | INTEGER | Number of seconds that the home team was going in the up direction |

| awaydowntime | INTEGER | Number of seconds that the away team was going in the down direction |

| homedowntime | INTEGER | Number of seconds that the home team was going in the down direction |

| awayuptime | INTEGER | Number of seconds that the away team was going in the up direction |



\### gensDatabase.db-only columns

| Column Name | Type | Description |

|---|---|---|

| homefchecks | INTEGER | Number of checks by home forwards |

| homedchecks | INTEGER | Number of checks by home defensemen |

| awayfchecks | INTEGER | Number of checks by away forwards |

| awaydchecks | INTEGER | Number of checks by away defensemen |



\---



\## Table: skaters

One row represents one skater's stat line from one game.

Primary key: rowid



| Column Name | Type | Description |

|---|---|---|

| matchid | INTEGER | Unique identifier for the game |

| regorplay | TEXT | "R" = regular season, "P" = playoff |

| team | TEXT | The abbreviation of the team name of the skater |

| ha | INTEGER | 1 if the skater plays for the home team, -1 if the skater plays for the away team |

| name | TEXT | The name of the skater |

| position | TEXT | "F" = forward, "D" = defenseman |

| goals | INTEGER | The number of goals scored by the skater in the game |

| assists | INTEGER | The number of assists by the skater in the game |

| points | INTEGER | The number of points (goals + assists) by the skater in the game |

| sog | INTEGER | The number of shots by the skater in the game |



\### gensDatabase.db-only columns

| Column Name | Type | Description |

|---|---|---|

| checks | INTEGER | The number of checks by the skater in the game |

| toi | INTEGER | The number of seconds that the skater was on the ice in the game |



\---



\## Table: goalies

One row represents one goalie's stat line from one game.

Primary key: (match\_id, RegOrPlay, goalie\_name)



| Column Name | Type | Description |

|---|---|---|

| matchid | INTEGER | Unique identifier for the game |

| regorplay | TEXT | "R" = regular season, "P" = playoff |

| team | TEXT | The abbreviation of the team name of the goalie |

| ha | INTEGER | 1 if the goalie plays for the home team, -1 if the goalie plays for the away team |

| name | TEXT | The name of the goalie |

| ga | INTEGER | The number of goals allowed by the goalie in the game |

| sv | INTEGER | The number of saves by the goalie in the game |

| sha | INTEGER | The number of shots faced by the goalie in the game |

| assists | INTEGER | The number of assists by the goalie in the game |



\### gensDatabase.db-only columns

| Column Name | Type | Description |

|---|---|---|

| toi | INTEGER | The number of seconds that the skater was on the ice in the game |



\---



\## Table: goals

One row represents one goal from one game.

Primary key: (match\_id, RegOrPlay, period, seconds\_elapsed, scorer\_name)



| Column Name | Type | Description |

|---|---|---|

| matchid | INTEGER | Unique identifier for the game |

| regorplay | TEXT | "R" = regular season, "P" = playoff |

| league | TEXT | Name of the league season in which the game was played |

| datetime | TEXT | Date and time at which the game was played, in YYYY-MM-DD HH:MM:SS format |

| hometeam | TEXT | The long name of the home team |

| hometeamabbrev | TEXT | The 2-3 letter abbreviation of the home team name |

| homeplayer | TEXT | The name of the human who played as the home team |

| awayteam | TEXT | The long name of the away team |

| awayteamabbrev | TEXT | The 2-3 letter abbreviation of the away team name |

| awayplayer | TEXT | The name of the human who played as the away team |

| awayscore | INTEGER | The away team's score after this goal was scored |

| homescore | INTEGER | The home team's score after this goal was scored |

| ha | INTEGER | 1 if the home team scored this goal, -1 if the away team scored this goal |

| period | INTEGER | The period number in which the goal was scored (4 for overtime) |

| seconds | INTEGER | The number of seconds elapsed in the period when the goal was scored |

| scorer | TEXT | The name of the skater who scored the goal |

| assist1 | TEXT | The name of the player who registered the primary assist (NULL if there was no primary assist) |

| assist2 | TEXT | The name of the player who registered the secondary assist (NULL if there was no secondary assist) |

| status | TEXT | "EV" = even-strength goal, "PP" = power play goal, "PP2" = 2-man power play goal, "SH" = shorthanded goal, "SH2" = 2-man shorthanded goal |

\---



\## Table: penalties

One row represents one penalty from one game.

Primary key: (match\_id, RegOrPlay, period, seconds\_elapsed, player\_name)



| Column Name | Type | Description |

|---|---|---|

| matchid | INTEGER | Unique identifier for the game |

| regorplay | TEXT | "R" = regular season, "P" = playoff |

| league | TEXT | Name of the league season in which the game was played |

| datetime | TEXT | Date and time at which the game was played, in YYYY-MM-DD HH:MM:SS format |

| hometeam | TEXT | The long name of the home team |

| hometeamabbrev | TEXT | The 2-3 letter abbreviation of the home team name |

| homeplayer | TEXT | The name of the human who played as the home team |

| awayteam | TEXT | The long name of the away team |

| awayteamabbrev | TEXT | The 2-3 letter abbreviation of the away team name |

| awayplayer | TEXT | The name of the human who played as the away team |

| ha | INTEGER | 1 if the home team scored committed this penalty, -1 if the away team committed this penalty |

| period | INTEGER | The period number in which the penalty was committed (4 for overtime) |

| seconds | INTEGER | The number of seconds elapsed in the period when the penalty was committed |

| skater | TEXT | The name of the skater who committed the penalty |

| pen | TEXT | The type of penalty committed |

