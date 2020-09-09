# perfectionist
A repository with AI for the perfectionist game(https://louigiverona.com/perfectionist/)



## files
`gamev4.py` is currently the working prototype(extremely inefficient). Before using, adjust the parameters. The code is NOT edgecase safe
```py
# this is inside the file
X=<your board width value here>
Y=<you board height value here>
CUT=<the maximum lost>
MAX_BRANCH_POOL=<the maximum amount of future branches to keep>
FEVER=<endgame phase requirement tiles>
MAX_INT=<the maximum number of the tile. used to pigeon sort>
```
`get_best_fever_score.py`, `gamev8_fevertime_logic.py` is an endgame/fever time purpose only prototype.



## Contributers
* **Me Too Thanks#7924** *(discord)* - author of `get_best_fever_score.py`, `fetch_daily_board.py`

# Update log
**2020.8.8**
* added this log section
* v8 fevertime logic was finished

**2020.8.12**
* v9 generation code was finished

**2020.8.13**
* v9.2 generation code was finished
* fever time table was finished

**2020.8.17**
* v10 (doesnt work) was finished