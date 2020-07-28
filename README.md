# perfectionist
A repository with AI for the perfectionist game(https://louigiverona.com/perfectionist/)



## files
`gamev4.py` is currently the working prototype. Before using, adjust the parameters. The code is NOT edgecase safe
```py
# this is inside the file
X=<your board width value here>
Y=<you board height value here>
CUT=<the maximum lost>
MAX_BRANCH_POOL=<the maximum amount of future branches to keep>
FEVER=<endgame phase requirement tiles>
MAX_INT=<the maximum number of the tile. used to pigeon sort>
```
`get_best_fever_score.py` is an endgame/fever time purpose only prototype.

## Contributers
* **Me Too Thanks#7924** *(discord)* - author of `get_best_fever_score.py`