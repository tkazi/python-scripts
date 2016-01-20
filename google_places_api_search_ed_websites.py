## script uses google places api to search for education related keywords in a city, and collect websites


import csv
from googleplaces import GooglePlaces, types, lang

with open('filename.csv', 'rU') as f:
    c = csv.reader(f)
    cities = list(c)


export=open("filename.csv","wb");
output=csv.writer(export, lineterminator='\n')

api_key = ''

google_places = GooglePlaces(api_key)


search = ['school','schools','elementary school','middle school','high school','charter','charter school','private school',
          'catholic school','montessori','kindergarten','pre k','pre-k','after school','tutor','tutoring','education','teacher',
          'Non For Profit','Non Profit','Non-Profit','k12','k 12','k-12','special education','autism','deaf','blind','education','kumon']

# search = ['clinic','private physician','health clinic','PCP', 'IPA', 'private healthcare']

# search = ['Non For Profit','Non Profit','Non-Profit']

# location = ['Newyork, Newyork', 'Teacneck, New Jersey', 'Baltimore, Maryland', 'Palo Alto, California', 'Mountain View, California']

archive_results = []
for city in cities:
    print city[0]
    output.writerow(city)
    n = 0
    while n < len(search):
        print search[n]
        output.writerow([search[n]])
        # You may prefer to use the text_search API, instead.
        query_result = google_places.nearby_search(
                location=city[0], keyword=search[n],
                radius=50000, )

        if query_result.has_attributions:
            print query_result.html_attributions

        for place in query_result.places:
            results = []
            row = ''
            # Returned places from a query are place summaries.
            # print place.name
            # row = str(place.name)
            row = u''.join((place.name)).encode('utf-8').strip()
            # The following method has to make a further API call.
            place.get_details()
            
            # Referencing any of the attributes below, prior to making a call to
            # get_details() will raise a googleplaces.GooglePlacesAttributeError.
            # print place.website
            row += ": " + str(place.website)
            # row += u''.join((place.website)).encode('utf-8').strip()
            if row not in archive_results:
                print row
                archive_results.append(row)
                results.append(row)
                output.writerow(results)
            else:
                print "--"*20
        n = n + 1




    