import sys
from collections import Counter

nb_pizzas = 0
twos = 0
threes = 0
fours = 0
pizzas = []


# --- Parsing ---

nb_pizzas, twos, threes, fours = [int(x) for x in sys.stdin.readline().strip().split()]

for line in sys.stdin:
  pizza = Counter(line.strip().split()[1:])
  pizzas.append(pizza)



# --- Solution class ---

class Solution:
  def __init__(self):
    self.people = [idx for idx in range(min(len(pizzas), 2*twos + 3*threes + 4 * fours))]
    self.nb_two, self.nb_three, self.nb_four = 0, 0, 0

  def global_score(self):
    score = 0

    start_two = 0
    for idx in range(start_two, start_two + self.nb_two * 2, 2):
      if (len(pizzas[self.people[idx]]) > 0 and len(pizzas[self.people[idx+1]]) > 0):
        local_score = len(pizzas[self.people[idx]] + pizzas[self.people[idx+1]])
        score += local_score*local_score

    start_three = self.nb_two * 2
    for idx in range(start_three, start_three + self.nb_three * 3, 3):
      if (len(pizzas[self.people[idx]]) > 0 and len(pizzas[self.people[idx+1]]) > 0 and len(pizzas[self.people[idx+2]]) > 0):
        local_score = len(pizzas[self.people[idx]] + pizzas[self.people[idx+1]] + pizzas[self.people[idx+2]])
        score += local_score*local_score

    start_four = self.nb_two * 2 + self.nb_three * 3
    for idx in range(start_four, start_four + self.nb_four * 4, 4):
      if (len(pizzas[self.people[idx]]) > 0 and len(pizzas[self.people[idx+1]]) > 0 and len(pizzas[self.people[idx+2]]) > 0) and len(pizzas[self.people[idx+3]]) > 0:
        local_score = len(pizzas[self.people[idx]] + pizzas[self.people[idx+1]] + pizzas[self.people[idx+2]] + pizzas[self.people[idx+3]])
        score += local_score*local_score

    return score

  def save(self, prefix, score):
    with open(f"{prefix}_{score}.out", "w") as fp:
      print(self.nb_two + self.nb_three + self.nb_four, file=fp)

      start_idx = 0
      for idx in range(start_idx, start_idx + 2 * self.nb_two, 2):
        print(f"2 {self.people[idx]} {self.people[idx+1]}", file=fp)

      start_idx += self.nb_two * 2
      for idx in range(start_idx, start_idx + 3 * self.nb_three, 3):
        print(f"3 {self.people[idx]} {self.people[idx+1]} {self.people[idx+2]}", file=fp)

      start_idx += self.nb_three * 3
      for idx in range(start_idx, start_idx + 4 * self.nb_four, 4):
        print(f"4 {self.people[idx]} {self.people[idx+1]} {self.people[idx+2]} {self.people[idx+3]}",  file=fp)


# --- opti functions ---

import random
def random_assign():
  sol = Solution()
  sol.people = [i for i in range(nb_pizzas)]
  random.shuffle(sol.people)
  remaining = nb_pizzas

  # two assign
  if 2 * twos > remaining:
    sol.nb_two = remaining // 2
    if remaining % 2 == 1 and threes > 0:
      sol.nb_two -= 1
      sol.nb_three = 1
      return sol
  else:
    sol.nb_two = twos
    remaining -= 2 * sol.nb_two

  # three assign
  if 3 * threes > remaining:
    sol.nb_three = remaining // 3
    if remaining % 3 == 1 and fours > 0:
      sol.nb_three -= 1
      sol.nb_four = 1
      return sol
    elif remaining % 3 == 2 and sol.nb_three >= 2 and fours > 1:
      sol.nb_three -= 2
      sol.nb_four = 2
      return sol
  else:
    sol.nb_three = threes
    remaining -= 3 * sol.nb_three

  # four assign
  sol.nb_four = min(remaining // 4, fours)

  return sol


# --- main ---

best_score = 0
best_sol = Solution()

for _ in range(10000):
  rnd = random_assign()
  score = rnd.global_score()
  if best_score < score:
    print("score", rnd.global_score())
    best_score = score
    best_sol = rnd
    rnd.save(sys.argv[1], score)

