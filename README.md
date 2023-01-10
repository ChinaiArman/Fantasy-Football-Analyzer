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

### What is Fantasy Football?:

Fantasy Football is a form of sports betting. The objective is to assemble a winning team of players from the NFL. The performance of each team hinges on the performance of the players in the actual game. The better the player plays in the NFL, the more points they generate in Fantasy. Participants play in a league (usually of size 12) in a season long competition. The format is as follows

1) A Draft
2) The Regular Season
3) Post Season / Championship

In the draft, participants take turns selecting players for their team. The best players go off the board first, and the draft lasts for 16 rounds. At the end of the draft, everyone will have their team's roster. 

The Regular Season lasts roughly 12 weeks, where teams go head to head. The winner of each week is determined by whos starting lineup scored the most points. This generates a win/loss record, which determines who makes it into playoffs. 

After the 12 weeks, the best teams move on to the playoffs. Most leagues function as single elimination head to head matches, and the winner of the championship usually receives a prize of some sort, while last place in the whole league will receive a 'loser punishment' (depends league to league).

### The premise for the project:

As you can see from this format, a lot of a teams success or failure is determined very early on, in the draft. There is a lot of luck in Fantasy betting, but also a  lot of prediction and statistics. Because the best players go off the board first, and each round that passes the players on the board get less valuable (as they are worse / generate less points), it creates an economy or price for each player, called ADP. ADP stands for average draft position, or the amount of capital you have to give up to roster a specific player. 

The goal of this project is to find value based on a players ADP. In each round of the draft, there are always players that greatly exceed what their ADP expected of them, and players who bust and underperform throughout the season. Finding value at ADP is the key to winning in Fantasy Football.

### What the project does:

This algorithm uses trends observed in the stats of breakout player stats in the season BEFORE they broke out, in order to find idicators for future breakouts or value at ADP. 
