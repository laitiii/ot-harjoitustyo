import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassapaate_on_olemassa(self):
        self.assertIsNotNone(self.kassapaate)

    def test_kassapaatteessa_on_aluksi_rahaa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullisia_ja_maukkaita_lounaita_ei_ole_aluksi_myyty(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # Käteinen

    def test_edullinen_lounas_kateisella_tasarahalla(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(240)

        self.assertEqual(palautus, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_lounas_kateisella_tasarahalla(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(palautus, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_lounas_kateisella_vaihtorahalla(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(palautus, 60)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_lounas_kateisella_vaihtorahalla(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(palautus, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_lounas_kateisella_ei_onnistu_jos_raha_ei_riita(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(palautus, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_lounas_kateisella_ei_onnistu_jos_raha_ei_riita(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(300)

        self.assertEqual(palautus, 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    # Kortti

    def test_edullinen_lounas_kortilla_onnistuu(self):
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertTrue(onnistui)
        self.assertEqual(self.maksukortti.saldo, 760)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_lounas_kortilla_ei_onnistu_jos_saldo_ei_riita(self):
        kortti = Maksukortti(200)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertFalse(onnistui)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_lounas_kortilla_onnistuu(self):
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertTrue(onnistui)
        self.assertEqual(self.maksukortti.saldo, 600)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_lounas_kortilla_ei_onnistu_jos_saldo_ei_riita(self):
        kortti = Maksukortti(300)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertFalse(onnistui)
        self.assertEqual(kortti.saldo, 300)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # Rahan lataaminen

    def test_rahan_lataaminen_kortille_kasvattaa_saldoa_ja_kassan_rahoja(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)

        self.assertEqual(self.maksukortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100500)

    def test_negatiivisen_summan_lataaminen_ei_muuta_tilannetta(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)

        self.assertEqual(self.maksukortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassassa_rahaa_euroina_palautuu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)