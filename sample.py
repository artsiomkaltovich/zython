"""
enum Men = anon_enum(n);
enum Women = anon_enum(n);

array[Women, Men] of int: rankWomen;
array[Men, Women] of int: rankMen;

array[Men] of var Women: wife;
array[Women] of var Men: husband;

% assignment
constraint forall (m in Men) (husband[wife[m]]=m);
constraint forall (w in Women) (wife[husband[w]]=w);
% ranking
constraint forall (m in Men, o in Women) (
     rankMen[m,o] < rankMen[m,wife[m]] ->
         rankWomen[o,husband[o]] < rankWomen[o,m] );

constraint forall (w in Women, o in Men) (
     rankWomen[w,o] < rankWomen[w,husband[w]] ->
         rankMen[o,wife[o]] < rankMen[o,w] );
solve satisfy;

output ["wives= \(wife)\nhusbands= \(husband)\n"];

n = 5;
rankWomen =
 [| 1, 2, 4, 3, 5,
  | 3, 5, 1, 2, 4,
  | 5, 4, 2, 1, 3,
  | 1, 3, 5, 4, 2,
  | 4, 2, 3, 5, 1 |];

rankMen =
 [| 5, 1, 2, 4, 3,
  | 4, 1, 3, 2, 5,
  | 5, 3, 2, 4, 1,
  | 1, 5, 4, 3, 2,
  | 4, 3, 2, 1, 5 |];
"""
https://docs.minizinc.dev/en/stable/modelling2.html#array-access-constraints
import zython as zn
from itertools import product


n = 5
rank_women = [
    [1, 2, 4, 3, 5],
    [3, 5, 1, 2, 4],
    [5, 4, 2, 1, 3],
    [1, 3, 5, 4, 2],
    [4, 2, 3, 5, 1],
]
rank_men = [
    [5, 1, 2, 4, 3],
    [4, 1, 3, 2, 5],
    [5, 3, 2, 4, 1],
    [1, 5, 4, 3, 2],
    [4, 3, 2, 1, 5],
]


class MyModel(zn.Model):
    def __init__(self, rank_women, rank_men):
        n = len(rank_women)
        self.rank_women = zn.Array(rank_women)
        self.rank_men = zn.Array(rank_men)
        self.husband = zn.Array(zn.var(range(n)), shape=(n,))
        self.wife = zn.Array(zn.var(range(n)), shape=(n,))
        #
        # constraint forall (m in Men, o in Women) (
        #      rankMen[m,o] < rankMen[m,wife[m]] ->
        #          rankWomen[o,husband[o]] < rankWomen[o,m] );
        #
        # constraint forall (w in Women, o in Men) (
        #      rankWomen[w,o] < rankWomen[w,husband[w]] ->
        #          rankMen[o,wife[o]] < rankMen[o,w] );
        self.constraints = [
            zn.forall(range(n), lambda m: self.husband[self.wife[m]] == m),
            zn.forall(range(n), lambda w: self.wife[self.husband[w]] == w),
            zn.forall(
                range(n),
                range(n),
                lambda m, o: zn.implication(
                    self.rank_men[m, o] < self.rank_men[m, self.wife[m]],
                    self.rank_women[o, self.husband[o]] < self.rank_women[o, m],
                ),
            ),
            zn.forall(
                range(n),
                range(n),
                lambda w, o: zn.implication(
                    self.rank_women[w, o] < self.rank_women[w, self.husband[w]],
                    self.rank_men[o, self.wife[o]] < self.rank_men[o, w],
                ),
            ),
        ]
        # for m, o in product(range(n), repeat=2):
        #     self.constraints.append(
        #         zn.implication(
        #             self.rank_men[m, o] < self.rank_men[m, self.wife[m]],
        #             self.rank_women[o, self.husband[o]] < self.rank_women[o, m],
        #         ),
        #     )
        # for w, o in product(range(n), repeat=2):
        #     self.constraints.append(
        #         zn.implication(
        #             self.rank_women[w, o] < self.rank_women[w, self.husband[w]],
        #             self.rank_men[o, self.wife[o]] < self.rank_men[o, w],
        #         ),
        #     )


model = MyModel(rank_women, rank_men)
result = model.solve_satisfy(verbose=True)
print(result)
assert str(result) == "Solution(husband=[3, 0, 1, 4, 2], wife=[1, 2, 4, 0, 3])"
