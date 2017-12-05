"""Tests for utilities and helper functions."""

import unittest
import importlib
from os import environ
from json import dumps, loads

from itsdangerous import URLSafeSerializer

from atmfinda.models import db, ATM
from atmfinda.utils import (
    transform_google_results, create_atms, deserialize_atms, deserialize_atm,
    validate_token
)

CONFIG = environ.get('FLASK_CONFIG', 'atmfinda.config.local_test')
CONFIG = importlib.import_module(CONFIG)

results = {
   "html_attributions": [],
   "results": [
      {
         "geometry": {
            "location": {
               "lat": -33.870775,
               "lng": 151.199025
            }
         },
         "icon": "http://maps.gstatic.com/mapfiles/place_api/icons/travel_agent-71.png",
         "id": "21a0b251c9b8392186142c798263e289fe45b4aa",
         "name": "Rhythmboat Cruises",
         "opening_hours": {
            "open_now": True
         },
         "photos": [
            {
               "height": 270,
               "html_attributions": [],
               "photo_reference": "CnRnAAAAF-LjFR1ZV93eawe1cU_3QNMCNmaGkowY7CnOf-kcNmPhNnPEG9W979jOuJJ1sGr75rhD5hqKzjD8vbMbSsRnq_Ni3ZIGfY6hKWmsOf3qHKJInkm4h55lzvLAXJVc-Rr4kI9O1tmIblblUpg2oqoq8RIQRMQJhFsTr5s9haxQ07EQHxoUO0ICubVFGYfJiMUPor1GnIWb5i8",
               "width": 519
            }
         ],
         "place_id": "ChIJyWEHuEmuEmsRm9hTkapTCrk",
         "scope": "GOOGLE",
         "alt_ids": [
            {
               "place_id": "D9iJyWEHuEmuEmsRm9hTkapTCrk",
               "scope": "APP"
            }
         ],
         "reference": "CoQBdQAAAFSiijw5-cAV68xdf2O18pKIZ0seJh03u9h9wk_lEdG-cP1dWvp_QGS4SNCBMk_fB06YRsfMrNkINtPez22p5lRIlj5ty_HmcNwcl6GZXbD2RdXsVfLYlQwnZQcnu7ihkjZp_2gk1-fWXql3GQ8-1BEGwgCxG-eaSnIJIBPuIpihEhAY1WYdxPvOWsPnb2-nGb6QGhTipN0lgaLpQTnkcMeAIEvCsSa0Ww",
         "types": ["travel_agency", "restaurant", "food", "establishment"],
         "vicinity": "Pyrmont Bay Wharf Darling Dr, Sydney"
      },
      {
         "geometry": {
            "location": {
               "lat": -33.866891,
               "lng": 151.200814
            }
         },
         "icon": "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id": "45a27fd8d56c56dc62afc9b49e1d850440d5c403",
         "name": "Private Charter Sydney Habour Cruise",
         "photos": [
            {
               "height": 426,
               "html_attributions": [],
               "photo_reference": "CnRnAAAAL3n0Zu3U6fseyPl8URGKD49aGB2Wka7CKDZfamoGX2ZTLMBYgTUshjr-MXc0_O2BbvlUAZWtQTBHUVZ-5Sxb1-P-VX2Fx0sZF87q-9vUt19VDwQQmAX_mjQe7UWmU5lJGCOXSgxp2fu1b5VR_PF31RIQTKZLfqm8TA1eynnN4M1XShoU8adzJCcOWK0er14h8SqOIDZctvU",
               "width": 640
            }
         ],
         "place_id": "ChIJqwS6fjiuEmsRJAMiOY9MSms",
         "scope": "GOOGLE",
         "reference": "CpQBhgAAAFN27qR_t5oSDKPUzjQIeQa3lrRpFTm5alW3ZYbMFm8k10ETbISfK9S1nwcJVfrP-bjra7NSPuhaRulxoonSPQklDyB-xGvcJncq6qDXIUQ3hlI-bx4AxYckAOX74LkupHq7bcaREgrSBE-U6GbA1C3U7I-HnweO4IPtztSEcgW09y03v1hgHzL8xSDElmkQtRIQzLbyBfj3e0FhJzABXjM2QBoUE2EnL-DzWrzpgmMEulUBLGrtu2Y",
         "types": ["restaurant", "food", "establishment"],
         "vicinity": "Australia"
      },
      {
         "geometry": {
            "location": {
               "lat": -33.870943,
               "lng": 151.190311
            }
         },
         "icon": "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png",
         "id": "30bee58f819b6c47bd24151802f25ecf11df8943",
         "name": "Bucks Party Cruise",
         "opening_hours": {
            "open_now": True
         },
         "photos": [
            {
               "height": 600,
               "html_attributions": [],
               "photo_reference": "CnRnAAAA48AX5MsHIMiuipON_Lgh97hPiYDFkxx_vnaZQMOcvcQwYN92o33t5RwjRpOue5R47AjfMltntoz71hto40zqo7vFyxhDuuqhAChKGRQ5mdO5jv5CKWlzi182PICiOb37PiBtiFt7lSLe1SedoyrD-xIQD8xqSOaejWejYHCN4Ye2XBoUT3q2IXJQpMkmffJiBNftv8QSwF4",
               "width": 800
            }
         ],
         "place_id": "ChIJLfySpTOuEmsRsc_JfJtljdc",
         "scope": "GOOGLE",
         "reference": "CoQBdQAAANQSThnTekt-UokiTiX3oUFT6YDfdQJIG0ljlQnkLfWefcKmjxax0xmUpWjmpWdOsScl9zSyBNImmrTO9AE9DnWTdQ2hY7n-OOU4UgCfX7U0TE1Vf7jyODRISbK-u86TBJij0b2i7oUWq2bGr0cQSj8CV97U5q8SJR3AFDYi3ogqEhCMXjNLR1k8fiXTkG2BxGJmGhTqwE8C4grdjvJ0w5UsAVoOH7v8HQ",
         "types": ["restaurant", "food", "establishment"],
         "vicinity": "37 Bank St, Pyrmont"
      },
      {
         "geometry": {
            "location": {
               "lat": -33.867591,
               "lng": 151.201196
            }
         },
         "icon": "http://maps.gstatic.com/mapfiles/place_api/icons/travel_agent-71.png",
         "id": "a97f9fb468bcd26b68a23072a55af82d4b325e0d",
         "name": "Australian Cruise Group",
         "opening_hours": {
            "open_now": True
         },
         "photos": [
            {
               "height": 242,
               "html_attributions": [],
               "photo_reference": "CnRnAAAABjeoPQ7NUU3pDitV4Vs0BgP1FLhf_iCgStUZUr4ZuNqQnc5k43jbvjKC2hTGM8SrmdJYyOyxRO3D2yutoJwVC4Vp_dzckkjG35L6LfMm5sjrOr6uyOtr2PNCp1xQylx6vhdcpW8yZjBZCvVsjNajLBIQ-z4ttAMIc8EjEZV7LsoFgRoU6OrqxvKCnkJGb9F16W57iIV4LuM",
               "width": 200
            }
         ],
         "place_id": "ChIJrTLr-GyuEmsRBfy61i59si0",
         "scope": "GOOGLE",
         "reference": "CoQBeQAAAFvf12y8veSQMdIMmAXQmus1zqkgKQ-O2KEX0Kr47rIRTy6HNsyosVl0CjvEBulIu_cujrSOgICdcxNioFDHtAxXBhqeR-8xXtm52Bp0lVwnO3LzLFY3jeo8WrsyIwNE1kQlGuWA4xklpOknHJuRXSQJVheRlYijOHSgsBQ35mOcEhC5IpbpqCMe82yR136087wZGhSziPEbooYkHLn9e5njOTuBprcfVw",
         "types": ["travel_agency", "restaurant", "food", "establishment"],
         "vicinity": "32 The Promenade, King Street Wharf 5, Sydney"
      }
   ],
   "status": "OK"
}


class UtilsTestCase(unittest.TestCase):
    """Tests for helper functions."""
        
    def setUp(self):
        """Setup run before each test fixture."""
        self.client = self.app.test_client()  # Use a fresh client for each test

    def test_transform_google_results(self):
        """Test if the function returns the format we expect."""
        # result = transform_google_results(results)
  
    def test_create_atms(self):
        """Test if ATMS were succesfully created."""
        with self.app.app_context():
            atms = transform_google_results(results)
            create_atms(atms)

    def test_deserialize_atm(self):
        """Test deserialization of a single ATM."""
        atm = ATM(
            name='ATM', address='address1', photo_reference='ref',
            place_id='xy23lkds', location='POINT(3.01 3.5)', status=True
        )

        with self.app.app_context():
            db.session.add(atm)
            db.session.commit()
            db.session.refresh(atm)

        deserialized_atm = deserialize_atm(atm)

        self.assertEqual(deserialized_atm, {
            'id': atm.id, 'name': 'ATM', 'address': 'address1',
            'photo': '', 'photo_reference': 'ref',
            'place_id': 'xy23lkds',
            'location': {
                'latitude': 3.5, 'longitude': 3.01
            },
            'status': True,
            'date_modified': atm.date_modified
        })
    
    def test_deserialize_atms(self):
        """Test Deserialization of atms."""
        atm1 = ATM(
            name='ATM1', address='address1', photo_reference='reference1',
            place_id='place_id1', location='POINT(3.0 3.5)', status=True
        )
        atm2 = ATM(
            name='ATM2', address='address2', photo_reference='reference2',
            place_id='place_id2', location='POINT(4.0 4.5)', status=True
        )

        atms = (atm1, atm2)

        with self.app.app_context():
            db.session.add_all(atms)
            db.session.commit()
            db.session.refresh(atm1)
            db.session.refresh(atm2)

        deserialized_atms = deserialize_atms(atms)

        self.assertEqual(deserialized_atms, [
            {
                'id': atm1.id, 'name': 'ATM1', 'address': 'address1',
                'photo': '', 'photo_reference': 'reference1',
                'place_id': 'place_id1',
                'location': {
                    'latitude': 3.5, 'longitude': 3.0
                },
                'status': True,
                'date_modified': atm1.date_modified
            },
            {
                'id': atm2.id, 'name': 'ATM2', 'address': 'address2',
                'photo': '', 'photo_reference': 'reference2',
                'place_id': 'place_id2',
                'location': {
                    'latitude': 4.5, 'longitude': 4.0
                },
                'status': True,
                'date_modified': atm2.date_modified
            }
        ])

    def test_validate_token(self):
        """Test if we can validate a token and get the data succesfully."""
        # Generate token and compare with the one returned by the API.
        s = URLSafeSerializer(CONFIG.SECRET_KEY)
        token = s.dumps('abc@gmail.com')

        data = validate_token(token)

        self.assertEqual(data, 'abc@gmail.com')

    def test_deserialize_token_failure(self):
        """test if the validate token method returns False for a bad token."""
        s = URLSafeSerializer('Fake key')
        token = s.dumps('abc@gmail.com')

        data = validate_token(token)

        self.assertEqual(data, False)
        

if __name__ == '__main__':
    unittest.main()
