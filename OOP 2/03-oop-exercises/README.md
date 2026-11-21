# Exercise 3 - OOP problems (slide 67)

Statement: https://gist.github.com/bdallard/b2f2c910e3a9b564a30c86991c97b4fc

| File | Content |
|---|---|
| [`operator_overloading.py`](operator_overloading.py) | Complex (`+`, `-`), Person (`>` by age), Vector (`*` = dot product), Circle (all 6 comparisons), Point2D (compared by distance to origin), Matrix (`*`) |
| [`inheritance.py`](inheritance.py) | Vehicle → Car / Bicycle, Person → Student / Employee, BankAccount → SavingsAccount (with `transfer`) |
| [`test_oop.py`](test_oop.py) | Unit tests for every problem |

The statement skips "Problem 3" in the operator-overloading part, so numbering goes 1, 2, 4, 5, 6, 7.

```bash
python3 operator_overloading.py
python3 inheritance.py
python3 test_oop.py
```

Notes on the choices:
- Comparison dunders return `NotImplemented` for other types, so Python can fall back properly.
- `Point2D` uses `functools.total_ordering`: only `__eq__` and `__lt__` are written, the other four are generated.
- `Student` / `Employee` call `super().__init__` and extend `introduce()` instead of rewriting it.
- `transfer` reuses `withdraw` and `deposit`, so the "insufficient balance" rule lives in one place.
