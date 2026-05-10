# Testausdokumentti

Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestilla sekä manuaalisesti peliä pelaamalla.

## Yksikkö- ja integraatiotestaus

Sovelluslogiikasta vastavaa `GameController`-luokkaa testataan [TestGameController](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/tests/test_game_controller.py)-testiluokalla

Vihollisaaltojen luomisesta ja ajastuksesta vastaa `WaveManager`-luokka. Sitä testataan [TestWaveManager](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/tests/test_wave_manager.py)-testiluokalla

Renderöinnistä vastaava `Renderer` luokka testataan [TestRenderer](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/tests/test_renderer.py)-testiluokalla

Tornit ja viholliset testataan [TestTower](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/tests/test_tower.py) ja [TestEnemy](https://github.com/laitiii/ot-harjoitustyo/blob/main/src/tests/test_enemy.py)-testiluokilla


## Testikattavuus 
Testikattavuus projektille on 71%. Enempää testejä ei oikeastaan ole mielekästä tehdä, sillä pygamen kanssa työskennellessä on paljon, mitä ei ole järkevä testata.
<img width="829" height="342" alt="image" src="https://github.com/user-attachments/assets/819d6210-720d-4455-9678-b73e866ad6ca" />


## Järjestelmätestaus

Sovellusta on testattu manuaalisesti sekä Windows10,11 sekä Cubbli Linux ympäristöissä. Myös testien toimivuus on testattu näissä ympäristöissä.
