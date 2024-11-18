# Advent Of Code2023 - www.adventofcode.com

My solutions to Advent of Code 2023. Using Python again this year, but no longer with GitHub copilot. As usual, co-opeting with MgTheSilverSardine.

Using Python 3.11.4 .

Useful links:

- https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ (as I can't use Conda anymore)
- https://regex101.com/
- https://networkx.com/
- sympy

## Interesting challenges:

- Challenge 7: a chance to use Quicksort. The poker challenge.
- Challenge 10 part 1: find the length of a path in a map. Djikstra not quite needed.
- Challenge 10 part 2: find the "area delimited by the path". Navigate along the edges keeping a direction + flood fill.
- Challenge 12: damaged springs -- a sort of string matching of different alternatives. Found a very fast solution, if not particularly smart, after a lot of silly coding to get there.
- Challenge 15: stupid challenge all about understanding the problem, not solving it. To throw off GPT-n?. Anyway, didn't like this one. 
- Challenge 16: this was the one with laser beams and reflections on a square matrix/map, very quantum-like.
- Challenge 17: Dijsktra on steroids. Path-finding but can't go more than 4 nodes in the same direction. Too ages to get to a working solution. In the end, each node was divided in 16 nodes, 4 for each cardinal direction and 4 for each distances. After this it was a "normal" shortest path, but still taking 1800 seconds, so I'm sure a faster solution can be found. Edit: worked on a new version, massively simplified, based on Uniform-Cost Search (Dijkstra for large Graphs) and using heapq, also generating next positions on run-time instead of ahead of time, that runs... in under a second. Sigh. Spent many hours on this one, also making silly distraction and bugs all the time. Happy with the final solution, finally.

- Challenge 21: the first part was relatively simple and got a solution with run-time of 0.03 secs. Second part I solved out-of-code. First I adapted the code to "virtualize" the rectangle, ie, allow for coordinates outside the central one, and don't crash. Then I printed out the area for steps up to almost 2000. Opened the file in Excel and saw how many O there were after 65 steps, then 65+131*n. I then put these sequences in Wolfram alpha, and when alternating the nsteps (327, 589, 851, 1113) I got a formula that interpolates them: `4*(14888*n^2 + 7487*n)`. Note: the reason for alternativng the steps is that because the step size is 131 (a prime/odd number), adjacent full squares will have "alternating polarity", i.e., the grid will fill in alternate free positions. Note that when alternating on the count of 0 starting with 196, 458, 720, 982, ... doesn't lead to a interpolation formula, I assume due to the polarity/prime issue. Left a file `calculations.xls` with the math. And this uses the hint that `26501365 = 202300*131 + 65`, which I saw in a google result summary blurb. :-/

- Challenge 24: solved with the help of sympy for linear algebra. Part 2 could have been solved on paper only. Had to refresh equations of the line from way back when.

- Challenge 25: tried to solve this by myself but didn't find a solution running in OK time. Ended up half-cheating and solving visually with the help of Networkx. Researching the problem after submitting, I found about min-cut: https://en.wikipedia.org/wiki/Minimum_cut and the solution in Python here which is so simple it hurts: https://www.reddit.com/r/adventofcode/comments/18qbsxs/2023_day_25_solutions/?rdt=35125 . Live and learn.

## Final note

Third year in a row. Not always happy with solutions, but happy I didn't go check other's solutions and that I solved them all for the third consecutive year.