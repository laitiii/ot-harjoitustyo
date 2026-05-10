
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
    participant Index
    participant GC as GameController
    participant Renderer
    participant WaveMgr as WaveManager
    participant Entities

    Index->>GC: initialize and run
    loop each frame
        GC->>Index: poll events
        alt build + SPACE
            GC->>WaveMgr: start_wave
            WaveMgr-->>GC: spawn_positions
            GC->>Entities: spawn enemies
        end
        GC->>Renderer: draw state
        GC->>WaveMgr: spawn_pending_enemy
        WaveMgr-->>GC: spawn_pos or none
        GC->>Entities: update_all (move, attack, cleanup)
        GC->>GC: check_wave_state
        GC->>Index: tick 60
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
