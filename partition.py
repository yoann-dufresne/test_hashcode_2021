import sys
from collections import Counter

nb_pizzas = 0
twos = 0
threes = 0
fours = 0
pizzas = []
ingredients = set()


# --- Parsing ---

nb_pizzas, twos, threes, fours = [int(x) for x in sys.stdin.readline().strip().split()]
max_teams = [twos, threes, fours]

for line in sys.stdin:
  pizza = list(line.strip().split()[1:])
  pizzas.append(pizza)
  ingredients = ingredients.union(set(pizza))
ingredients = list(ingredients)
print("nb ingredients", len(ingredients))


class Solution2:

  def __init__(self):
    self.used = {idx: False for idx in range(len(pizzas))}
    self.assignment = [[], [], []]
    self.score = 0

  def available_team(self):
    counts = [len(x) for x in self.assignment]
    print(counts)
    print(max_teams)
    return counts != max_teams

  def add_team(self, pizza_idxs):
    # pizza availability
    for idx in pizza_idxs:
      if self.used[idx]:
        return False

    # team availability
    team_size = len(pizza_idxs)
    if team_size < 2 or team_size > 4 or len(self.assignment[team_size-2]) >= max_teams[team_size-2]:
      return False

    # Compute score
    ingredients = []
    for pidx in pizza_idxs:
      self.used[pidx] = True
      ingredients += pizzas[pidx]
    self.score += pow(len(set(ingredients)), 2)
    self.assignment[team_size-2].append([x for x in pizza_idxs])

    return True

  def rm_team(self, pizza_idxs):
    # pizza availability
    for idx in pizza_idxs:
      if not self.used[idx]:
        return False

    # team availability
    team_size = len(pizza_idxs)
    if team_size < 2 or team_size > 4:
      return False

    # Compute score
    ingredients = Counter()
    for pidx in pizza_idxs:
      self.used[pidx] = False
      ingredients += pizzas[pidx]
    self.score -= pow(len(ingredients), 2)
    self.assignment[team_size-2].remove(pizza_idxs)

    return True

  def save(self, prefix):
    with open(f"{prefix}_{self.score}.out", "w") as fp:
      print(sum(len(x) for x in self.assignment), file=fp)

      for tup in self.assignment[0]:
        print("2", " ".join(str(x) for x in tup), file=fp)

      for tup in self.assignment[1]:
        print("3", " ".join(str(x) for x in tup), file=fp)

      for tup in self.assignment[2]:
        print("4", " ".join(str(x) for x in tup), file=fp)


# --- Combinatorial functions ---

def comp_tup(t):
  return t[0]/t[1], t[0]/len(t[2]), -len(t[2]), -t[1]

from itertools import combinations
def sorted_best_tuples(pizza_idxs, max_tup_size):
  weighted_candidates = []
  for t_size in range(2, max_tup_size+1):
    candidates = combinations(pizza_idxs, t_size)
    for candidate_tuple in candidates:
      tup_ingredients = []
      for pidx in candidate_tuple:
        tup_ingredients += list(pizzas[pidx])
      weighted_candidates.append((pow(len(set(tup_ingredients)), 2), len(tup_ingredients), candidate_tuple))

  weighted_candidates.sort(reverse=True, key=comp_tup)

  return weighted_candidates[:len(weighted_candidates)]

def greedy_fill(sol2, available_pizza_idxs):
  sorted_pizza_tuples = sorted_best_tuples(available_pizza_idxs, 4)
  # print(sorted_pizza_tuples)

  d_score = 0
  for score, nb_ingredients, pizza_tuple in sorted_pizza_tuples:
    added = sol2.add_team(pizza_tuple)
    if added:
      d_score += score


import random
def init_sol():
  pizza_idxs = list(range(nb_pizzas))
  random.shuffle(pizza_idxs)
  pizza_idxs.sort(reverse=True, key=lambda x: len(pizzas[x]))

  sol2 = Solution2()

  while(len(pizza_idxs) >= 4 and sol2.available_team()):
    # Greedy by slices of size 48
    to_add = pizza_idxs[:24]
    pizza_idxs = pizza_idxs[24:]

    greedy_fill(sol2, to_add)
    print (len(pizza_idxs))
    print("tmp score", sol2.score)

  return sol2

def improve_sol(sol, nb_remove=36):



def main2():
  s = init_sol()
  print(s.score)
  # print(s.assignment)
  s.save(sys.argv[1])


main2()

