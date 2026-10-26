Routing table from Gate

| Target | Distance | Path |
|---|---:|---|
| Admin | 2 | Gate → Admin |
| Annex | unreachable | - |
| Canteen | 9 | Gate → Admin → Canteen |
| Dorm | 14 | Gate → Admin → Library → Lab → Dorm |
| Gate | 0 | Gate |
| Gym | 11 | Gate → Admin → Canteen → Gym |
| Lab | 8 | Gate → Admin → Library → Lab |
| Library | 3 | Gate → Admin → Library |

Routing table from Dorm

| Target | Distance | Path |
|---|---:|---|
| Admin | 12 | Dorm → Gym → Canteen → Admin |
| Annex | unreachable | - |
| Canteen | 5 | Dorm → Gym → Canteen |
| Dorm | 0 | Dorm |
| Gate | 14 | Dorm → Gym → Canteen → Admin → Gate |
| Gym | 3 | Dorm → Gym |
| Lab | 6 | Dorm → Lab |
| Library | 11 | Dorm → Lab → Library |
