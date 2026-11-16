# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/hizarukuro/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/hizarukuro/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A complete chess engine in one small Python file. It plays on a 0x88 board with full rules — castling, en passant, promotion, check, stalemate, the fifty-move rule and the 200-ply adjudication the house applies. Search is negamax with alpha-beta pruning (PVS), a quiescence search over captures, promotions and evasions, a Zobrist transposition table, killer moves, null-move pruning, late-move reductions and check extensions. Evaluation is a full PeSTO tapered evaluation — middlegame and endgame piece-square tables for all six piece types, blended by game phase — plus a passed-pawn bonus; the tables are stored as file-symmetric half-tables, character-encoded at 6-centipawn resolution to fit the size limit. Every move is searched to a fixed cap of 80,000 nodes — never a clock — so a game replays move for move exactly. Validated head-to-head against the previous version of this engine over 200 games (63.0% score) and in the kit's practice gauntlet (three trials, mean Elo 1581). The committed `main.py` is the `makefun compress` packing of the readable source kept beside it.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8130 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=c23ct4sn&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
