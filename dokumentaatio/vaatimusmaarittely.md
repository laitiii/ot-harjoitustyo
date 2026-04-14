# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus on yksinkertainen tower defense -peli, joka on toteutettu Pythonilla ja Pygamella. Pelaajan tavoitteena on estää vihollisia pääsemästä kentän loppuun rakentamalla torneja reitin varrelle ja tuhoamalla viholliset ennen kuin ne saavuttavat maalin.

## Käyttöliittymä

Alussa pelissä on vain pelinäkymä, myöhemmin lisätään aloitusnäkymä sekä lopetus- tai game over -näkymä

Aloitusnäkymästä pelaaja voi käynnistää uuden pelin. Pelinäkymässä näkyvät pelialue, vihollisten kulkureitti, käytettävissä olevat tornit, pelaajan rahat, elämät ja mahdollinen pistemäärä tai kierrosnumero. Lopetusnäkymä näytetään, kun pelaaja häviää pelin tai selvittää kaikki kentät.

## Perusversion tarjoama toiminnallisuus

### Pelin alussa

- Pelaajalle näytetään pelin perusinformaatio, kuten elämät ja käytettävissä oleva rahamäärä ✅
- Kentällä on valmiiksi määritelty reitti, jota pitkin viholliset kulkevat ✅

### Pelaamisen aikana

- Viholliset liikkuvat kentällä ennalta määriteltyä reittiä pitkin ✅
- Pelaaja voi sijoittaa torneja puolustamaan reitin varrelle käyttämällä rahaa
- Tornit hyökkäävät automaattisesti kantamansa sisällä oleviin vihollisiin
- Vihollisen tuhoamisesta pelaaja saa rahaa
- Jos vihollinen pääsee maaliin asti, pelaaja menettää elämiä ✅
- Peli päättyy, kun pelaajan elämät loppuvat ✅

### Pelin päättyessä

- Pelaajalle näytetään game over tai victory -näkymä
- Pelaaja voi halutessaan aloittaa uuden pelin alusta

## Jatkokehitysideoita

Perusversion jälkeen peliä täydennetään ajan salliessa esimerkiksi seuraavilla toiminnallisuuksilla:

- useampia vihollistyyppejä
- useampia tornityyppejä
- tornien päivittäminen pelin aikana
- useita eri kenttiä
- aaltojen vaikeuden kasvu pelin edetessä
- valikot pelin pausettamiseen ja jatkamiseen
- pistelaskuri
- ääniefektit
- grafiikan ja animaatioiden parantaminen
