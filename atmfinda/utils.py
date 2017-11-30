"""Reusable functions to avoid polluting app.py"""


def transform_google_results(google_results):
    """Transforms results from google's places API to our format"""

    results = []

    if google_results['status'].lower() == 'ok':
        for atm in google_results['results']:
            data = {
                'name': atm['name'], 'address': atm['vicinity'],
                'photo_reference': atm['photos'][0]['photo_reference'],
                'location': {
                    'latitude': atm['geometry']['location']['lat'],
                    'longitude': atm['geometry']['location']['lat']
                }
            }

            results.append(data)

    return results
