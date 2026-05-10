
# Arkkitehtuurikuvaus

## Pakkauskaavio

Sovelluksen modulaarinen rakenne ja keskeiset riippuvuudet.

```mermaid
graph LR
    subgraph src
        index[index.py]
        gc[game_controller.py]
        renderer[renderer.py]
        wm[wave_manager.py]
        level[level_data.py]
        const[constants.py]
    end
    subgraph entities
        enemy[entities/enemy.py]
        tower[entities/tower.py]
    end
    assets[assets/*]

    index -->|instantiates| gc
    gc -->|imports| const
    gc -->|imports| level
    gc -->|uses| renderer
    gc -->|uses| wm
    gc -->|creates| enemy
    gc -->|creates| tower
    gc -->|loads| assets
```

[GameController](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/game_controller.py) on sovelluksen keskus: se lataa "asetukset" [constants](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/constants.py), tason [level_data](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/level_data.py), alustaa [renderer](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/renderer.py) ja käyttää [wave_manager](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/wave_manager.py) instanssia. Entiteetit ovat omassa paketissaan [entities](https://github.com/laitiii/ot-harjoitustyo/tree/main/src/entities) ja luodaan suorituksen aikana.

## Pelisilmukan sekvenssikaavio

Kuvaa yhden frame-päivityksen (≈60 FPS) korkean tason tapahtumat: tapahtumankäsittely, piirtäminen, päivitykset ja spawn-logiikka.

```mermaid
sequenceDiagram
    participant Main as index.py
    participant GC as GameController
    participant WM as WaveManager
    participant R as Renderer
    participant E as Enemy
    participant T as Tower
    participant PG as Pygame

    Main->>GC: initialize game and run
    loop FrameLoop
        GC->>PG: poll events
        alt build_state_and_SPACE
            GC->>WM: start_wave wave spawn_pos
            WM-->>GC: spawn_positions
            GC->>E: spawn enemies
        end
        GC->>R: draw state, enemies, towers
        GC->>GC: update
        GC->>WM: spawn_pending_enemy now spawn_pos
        WM-->>GC: spawn_pos_or_None
        alt spawn_pos_returned
            GC->>E: create enemy
        end
        GC->>E: move enemies
        GC->>T: update towers
        T-->>E: damage enemy
        GC->>GC: cleanup_dead_enemies
        GC->>PG: clock_tick
    end
```

`index.py` käynnistää `GameController.run()` (katso [index.py](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/index.py)). Jokaisella framella tapahtumat luetaan Pygamesta, piirretään tila `Renderer`-luokan kautta, spawn-logiikkaa hoitaa `WaveManager` ja pelilogiikka (liikkeet, tornien hyökkäykset, kuolleiden siivous) tapahtuu `GameController.update()`-metodissa.

## Tilakaavio

Pelin tilojen ja niiden väliset siirtymät.

```mermaid
stateDiagram-v2
        [*] --> Menu
        Menu --> Build : SPACE / reset_game()
        Build --> Game : SPACE / start_wave()
        Game --> Build : wave_completed
        Game --> GameOver : lives <= 0
        GameOver --> Build : SPACE / reset_game()
```

- `Menu`: päävalikko, jossa käyttäjä aloittaa pelin.
- `Build`: rakenteluvaihe, pelaaja sijoittaa torneja; paina `SPACE` käynnistääksesi aallon (`GameController.start_wave()`).
- `Game`: aktiivinen peli; viholliset spawnaavat ja liikkuvat polkua pitkin, tornit ampuvat.
- `GameOver`: kun `lives` ≤ 0; `SPACE` palauttaa rakenteluvaiheeseen ja resetoidaan peli.
