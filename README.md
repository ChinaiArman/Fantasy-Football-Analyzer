# Fantasy Football Analyzer - A Personal Project

<b>Arman Chinai</b>

---

## Objective

Create a python application to analyze fantasy football data and identify potential breakout players for the upcoming season. The project must make use of Python's data science packages, provide a modular and reusable solution, and work with large sets of NFL player data to create accurate predictions.

## Important Links

* GitHub: https://github.com/ChinaiArman/Fantasy-Football-Analyzer
* Figma: https://www.figma.com/file/NfDNQX0DYgagGRk15F5Nuq/Fantasy-Football-Analyzer-Figma?node-id=0%3A1&t=q6QbbwZOgAhM718W-0
* TRELLO: https://trello.com/invite/b/MLI7WDYs/ATTI1c2108e78f7c47088e510d18df0ecbfd6FD8E060/agile-planning-board

### Technologies Used:

* Python
* Pandas
* CSVs

---

`### What Is Fantasy Football?:`

Fantasy Football is a form of sports betting. The objective is to assemble a winning team of players from the NFL. The performance of each team hinges on the performance of the players in the actual game. The better the player plays in the NFL, the more points they generate in Fantasy. Participants play in a league (usually of size 12) in a season long competition. The format is as follows

1) A Draft
2) The Regular Season
3) Post Season / Championship

In the draft, participants take turns selecting players for their team. The best players go off the board first, and the draft lasts for 16 rounds. At the end of the draft, everyone will have their team's roster. 

The Regular Season lasts roughly 12 weeks, where teams go head to head. The winner of each week is determined by whos starting lineup scored the most points. This generates a win/loss record, which determines who makes it into playoffs. 

After the 12 weeks, the best teams move on to the playoffs. Most leagues function as single elimination head to head matches, and the winner of the championship usually receives a prize of some sort, while last place in the whole league will receive a 'loser punishment' (depends league to league).

### The Premise For The Project:

As you can see from this format, a lot of a teams success or failure is determined very early on, in the draft. There is a lot of luck in Fantasy betting, but also a  lot of prediction and statistics. Because the best players go off the board first, and each round that passes the players on the board get less valuable (as they are worse / generate less points), it creates an economy or price for each player, called ADP. ADP stands for average draft position, or the amount of capital you have to give up to roster a specific player. 

The goal of this project is to find value based on a players ADP. In each round of the draft, there are always players that greatly exceed what their ADP expected of them, and players who bust and underperform throughout the season. Finding value at ADP is the key to winning in Fantasy Football.

### What The Project Does:

This algorithm uses trends observed in the stats of breakout player stats in the season BEFORE they broke out, in order to find idicators for future breakouts or value at ADP. To do this, lots of NFL player data was collected and stored in CSVs. These CSVs were interpreted with Pandas in Python, and the trends identified were applied to the dataframes to remove players with low or no breakout potential. The remaining players in the dataframes had the upside to breakout, and thus were good investments at their respective ADPs. Because players tend to fall into tiers, rather than a linear decent with respect to value over ADP, each tier was graded on different criteria. For example, higher ADP players are expected to be good, so finding a player who is going to breakout in this tier will have to have a very high ceiling. Where as, at lower ADPs, these players are less valuable and cost less, so to constitute as a breakout here is slightly easier / different from higher up.

### The End Result:

The end result of this project are CSVs containing breakout players / good investments for the upcoming season. When using 2021s player data, the algorithm I created went 20/30 for players that it expected to breakout. However, some of those players suffered season ending injuries (an aspect of luck that cannot be predicted easily), so when removing the injured players, the algorithm went 20/25, or 80%. 

Once the next season is closer to beginning, and the ADP of players is stable and well known, I will run the algorithm again and identify the new breakout stars for next year.

### What I learned:

This project taught me a lot about data science. I got to refine a lot of my skills in Pandas, and practice turning large sets of data into useful information. I also got to practice a lot of my development skills. I used a lot of clean functions, with strong documentation. The functions were all modular, so I could reuse them year after year.
