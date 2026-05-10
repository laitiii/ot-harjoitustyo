# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovellus on yksinkertainen tower defense -peli, joka on toteutettu Pythonilla ja Pygamella. Pelaajan tavoitteena on estää vihollisia pääsemästä kentän loppuun rakentamalla torneja reitin varrelle ja tuhoamalla viholliset ennen kuin ne saavuttavat maalin.

## Käyttäjät
Projekti on yksinkertainen peli, joten käyttäjätyyppejä on vain yksi eli pelaaja.

## Käyttöliittymä

Pelissä on aloitusnäkymä, pelinäkymä sekä game over -näkymä.

Aloitusnäkymästä pelaaja voi käynnistää uuden pelin. Pelinäkymässä näkyvät pelialue, vihollisten kulkureitti, käytettävissä olevat tornit, pelaajan rahat, elämät ja kierrosnumero. Lopetusnäkymä näytetään, kun pelaaja häviää pelin tai selvittää kaikki kentät.

## Perusversion tarjoama toiminnallisuus

### Pelin alussa

- Pelaajalle näytetään start -näkymä
- Pelaaja voi aloittaa pelin

### Pelaamisen aikana

- Pelaajalle näytetään pelin perusinformaatio, kuten elämät ja käytettävissä oleva rahamäärä 
- Kentällä on valmiiksi määritelty reitti, jota pitkin viholliset kulkevat 
- Viholliset liikkuvat kentällä ennalta määriteltyä reittiä pitkin 
- Pelaaja voi sijoittaa torneja puolustamaan reitin varrelle käyttämällä rahaa 
- Tornit hyökkäävät automaattisesti kantamansa sisällä oleviin vihollisiin 
- Pelissä on rakennusvaihe 
- Viholliset syntyvät aalloissa
- Jokainen aalto on edellistä vaikeampi: vihollisten määrä ja osumapisteet kasvavat
- Vihollisen tuhoamisesta pelaaja saa rahaa 
- Jos vihollinen pääsee maaliin asti, pelaaja menettää elämiä 
- Peli päättyy, kun pelaajan elämät loppuvat 

### Pelin päättyessä

- Pelaajalle näytetään game over tai victory -näkymä 
- Pelaaja voi halutessaan aloittaa uuden pelin alusta 

## Jatkokehitysideoita

Perusversion jälkeen peliä täydennetään ajan salliessa esimerkiksi seuraavilla toiminnallisuuksilla:

- useampia vihollistyyppejä
- useampia tornityyppejä
- tornien päivittäminen pelin aikana
- useita eri kenttiä
- valikot pelin pausettamiseen ja jatkamiseen
- pistelaskuri
- ääniefektit
- grafiikan ja animaatioiden parantaminen
