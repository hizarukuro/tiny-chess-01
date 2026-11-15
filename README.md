# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/hizarukuro/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/hizarukuro/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A complete chess engine in one small Python file. It plays on a 0x88 board with full rules — castling, en passant, promotion, check, stalemate, the fifty-move rule and the 200-ply adjudication the house applies. Search is negamax with alpha-beta pruning, a quiescence search over captures, promotions and evasions, a Zobrist transposition table, killer moves, null-move pruning, late-move reductions and check extensions. Evaluation is material plus piece-square tables stored as file-symmetric half-tables, a tapered middlegame/endgame king table and a bishop-pair bonus. Every move is searched to a fixed cap of 100,000 nodes — never a clock — so a game replays move for move exactly. In the kit's own practice gauntlet (six games against the house depth and node anchors) it scores in the same band as the house baseline entry, winning against the depth-4 and 100k-node anchors. The committed `main.py` is the `makefun compress` packing of the readable source kept beside it.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8130 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=c23ct4sn&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
