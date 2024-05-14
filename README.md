# pygdo-blackjack
A blackjack chat-game for [pygdo](https://github.com/gizmore/pygdo).

I forgot to use sessions to save game states,
but this is actually only needed in `bin/pygdo/` when not using repl,
or http services that don't re-use threads (apache wsgi works fine)


### Installation

[Install](https://github.com/gizmore/pygdo/tree/main/DOCS/01_INSTALLATION.md)
the [pygdo](https://github.com/gizmore/pygdo)
system. (**forbidden** ;)), then:

```
./gdo_adm.sh provide blackjack
./gdo_adm.sh install black*
```

### CLI Methods

- [bj.bet](./method/bet.py) amt - Bet an amount of your credits.
- [bj.draw](./method/draw.py) {ncards} - Draw card(s).
- [bj.hold](./method/hold.py)  - Let the dealer play.
- [bj.reset](./method/reset.py) - Reset credits.
- [bj.stats](./method/reset.py) {player} - Print bank or player stats.


### HTTP Methods:

Currently hooks into the left sidebar.

Methods:

1) [http://localhost/blackjack.site.html](http://localhost/blackjack.site.html)
   (combines all relevant CLI Methods in a single page app. [SRC](./method/site.py))



#### License

This module is licensed under the PyGDOv8 License and is proprietary software.
