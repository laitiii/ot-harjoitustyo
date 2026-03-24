import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_kortti_latautuu_oikein(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_kortilta_veloitetaan_oikein(self):
        self.maksukortti.ota_rahaa(200)
        self.assertEqual(self.maksukortti.saldo, 800)

    def test_kortilta_veloitetaan_liikaa(self):
        self.maksukortti.ota_rahaa(1200)
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_kortti_ilmoittaa_tapahtuman_onnistumisesta(self):
        self.assertTrue(self.maksukortti.ota_rahaa(500))
        self.assertFalse(self.maksukortti.ota_rahaa(600))
