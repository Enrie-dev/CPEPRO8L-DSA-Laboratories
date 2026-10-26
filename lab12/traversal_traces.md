BFS trace from Gate

| Selected | Queue (front→back) | Visited | Order so far |
|---|---|---|---|
| - | [Gate] | {Gate} |  |
| Gate | [Admin, Library] | {Admin, Gate, Library} | Gate |
| Admin | [Library, Canteen] | {Admin, Canteen, Gate, Library} | Gate Admin |
| Library | [Canteen, Lab] | {Admin, Canteen, Gate, Lab, Library} | Gate Admin Library |
| Canteen | [Lab, Gym] | {Admin, Canteen, Gate, Gym, Lab, Library} | Gate Admin Library Canteen |
| Lab | [Gym, Dorm] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab |
| Gym | [Dorm] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab Gym |
| Dorm | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Library Canteen Lab Gym Dorm |

DFS trace from Gate

| Selected (popped) | Stack (bottom→top) | Visited | Order so far |
|---|---|---|---|
| - | [Gate] | {} |  |
| Gate | [Library, Admin] | {Gate} | Gate |
| Admin | [Library, Library, Canteen] | {Admin, Gate} | Gate Admin |
| Canteen | [Library, Library, Lab, Gym] | {Admin, Canteen, Gate} | Gate Admin Canteen |
| Gym | [Library, Library, Lab, Dorm] | {Admin, Canteen, Gate, Gym} | Gate Admin Canteen Gym |
| Dorm | [Library, Library, Lab, Lab] | {Admin, Canteen, Dorm, Gate, Gym} | Gate Admin Canteen Gym Dorm |
| Lab | [Library, Library, Lab, Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab} | Gate Admin Canteen Gym Dorm Lab |
| Library | [Library, Library, Lab] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Lab (already visited, skip) | [Library, Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Library (already visited, skip) | [Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |
| Library (already visited, skip) | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Gate Admin Canteen Gym Dorm Lab Library |

Program results from Gate: BFS = Gate Admin Library Canteen Lab Gym Dorm ; DFS = Gate Admin Canteen Gym Dorm Lab Library

BFS trace from Dorm

| Selected | Queue (front→back) | Visited | Order so far |
|---|---|---|---|
| - | [Dorm] | {Dorm} |  |
| Dorm | [Gym, Lab] | {Dorm, Gym, Lab} | Dorm |
| Gym | [Lab, Canteen] | {Canteen, Dorm, Gym, Lab} | Dorm Gym |
| Lab | [Canteen, Library] | {Canteen, Dorm, Gym, Lab, Library} | Dorm Gym Lab |
| Canteen | [Library, Admin] | {Admin, Canteen, Dorm, Gym, Lab, Library} | Dorm Gym Lab Canteen |
| Library | [Admin, Gate] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Lab Canteen Library |
| Admin | [Gate] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Lab Canteen Library Admin |
| Gate | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Lab Canteen Library Admin Gate |

DFS trace from Dorm

| Selected (popped) | Stack (bottom→top) | Visited | Order so far |
|---|---|---|---|
| - | [Dorm] | {} |  |
| Dorm | [Lab, Gym] | {Dorm} | Dorm |
| Gym | [Lab, Canteen] | {Dorm, Gym} | Dorm Gym |
| Canteen | [Lab, Lab, Admin] | {Canteen, Dorm, Gym} | Dorm Gym Canteen |
| Admin | [Lab, Lab, Library, Gate] | {Admin, Canteen, Dorm, Gym} | Dorm Gym Canteen Admin |
| Gate | [Lab, Lab, Library, Library] | {Admin, Canteen, Dorm, Gate, Gym} | Dorm Gym Canteen Admin Gate |
| Library | [Lab, Lab, Library, Lab] | {Admin, Canteen, Dorm, Gate, Gym, Library} | Dorm Gym Canteen Admin Gate Library |
| Lab | [Lab, Lab, Library] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Canteen Admin Gate Library Lab |
| Library (already visited, skip) | [Lab, Lab] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Canteen Admin Gate Library Lab |
| Lab (already visited, skip) | [Lab] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Canteen Admin Gate Library Lab |
| Lab (already visited, skip) | [] | {Admin, Canteen, Dorm, Gate, Gym, Lab, Library} | Dorm Gym Canteen Admin Gate Library Lab |

Program results from Dorm: BFS = Dorm Gym Lab Canteen Library Admin Gate ; DFS = Dorm Gym Canteen Admin Gate Library Lab
