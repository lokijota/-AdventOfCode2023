# Advent Of Code2023 - www.adventofcode.com

My solutions to Advent of Code 2023. Using Python again this year, but no longer with GitHub copilot. As usual, co-opeting with MgTheSilverSardine.

Using Python 3.11.4 .

Useful links:

- https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ (as I can't use Conda anymore)
- https://regex101.com/

## Interesting challenges:

- Challenge 7: a chance to use Quicksort. The poker challenge.
- Challenge 10 part 1: find the length of a path in a map. Djikstra not quite needed.
- Challenge 10 part 2: find the "area delimited by the path". Navigate along the edges keeping a direction + flood fill.
- Challenge 12: damaged springs -- a sort of string matching of different alternatives. Found a very fast solution, if not particularly smart, after a lot of silly coding to get there.
- Challenge 15: stupid challenge all about understanding the problem, not solving it. To throw off GPT-n?. Anyway, didn't like this one. 
- Challenge 16: this was the one with laser beams and reflections on a square matrix/map, very quantum-like.
- Challenge 17: Dijsktra on steroids. Path-finding but can't go more than 4 nodes in the same direction. Too ages to get to a working solution. In the end, each node was divided in 16 nodes, 4 for each cardinal direction and 4 for each distances. After this it was a "normal" shortest path, but still taking 1800 seconds, so I'm sure a faster solution can be found. Edit: worked on a new version, massively simplified, based on Uniform-Cost Search (Dijkstra for large Graphs) and using heapq, also generating next positions on run-time instead of ahead of time, that runs... in under a second. Sigh. Spent many hours on this one, also making silly distraction and bugs all the time. Happy with the final solution, finally.


