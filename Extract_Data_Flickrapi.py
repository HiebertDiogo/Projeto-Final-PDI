from pathlib import Path
import flickrapi
import json
import os

filename = "credential.json"
current_dir = Path.cwd() 
credentials_path = os.path.join(current_dir, 'credentials', filename)

with open(credentials_path, 'r') as file:
    data = json.load(file)

    api_key = data["CHAVE"]
    api_secret = data["SEGREDO"]


raw_file = open("raw_data.csv", "a")    # where your datapoints will be stored at
history = open("done_ids.txt", "r")     # all photo_ID's that have been added in the past.

donepre = history.readlines()           # Preventing adding the same photo twice.
history.close()

done = []
for item in donepre:
    item = item.strip()
    done.append(item)

donepids = open("done_ids.txt", "a")

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
flickr.authenticate_via_browser(perms='read')                       

add_data = True                        

TenDays = 259200                        # Unixtime for 10 days == 60seconds *60minutes *24hours * 10;
firstdate = 1017630000                  # Date: 01/04/2002.Bottom time limit, we shall call for all photo's that are uploaded after this timepoint.
finaldate = firstdate + TenDays         # Upper time limit for our small call, the while loop will keep using this untill it reaches the enddate.)

limitDate = 1711940400                  # Date:  01/04/2024. Last date available

# City variables: Latitude, Longitude, radius(in KM) - João Pessoa (Mata do Buraquinho)
latitude = "-7.144126"
longitude = "-34.857480"
rad = "8"

while add_data:

    page = 1
    startdate = str(firstdate)
    enddate = str(finaldate)
    shots = flickr.photos.search(page=str(page),
                                 has_geo="1",
                                 extras="geo, owner_name, date_taken, date_upload",
                                 privacy_filter="1",
                                 per_page="250",
                                 min_upload_date=startdate,
                                 max_upload_date=enddate,
                                 radius_units="km",
                                 radius=rad,
                                 lat=latitude,
                                 lon=longitude)
    
    parsed = json.loads(shots.decode('utf-8'))   
    for key in parsed:
        part = parsed["photos"]
        total_pages =  part["pages"]

    print ("There are %s pages returned by flickr" %(total_pages))
    while page <= total_pages:
        shots = flickr.photos.search(page=str(page),
                                     has_geo="1",
                                     extras="geo, owner_name, date_taken, date_upload",
                                     privacy_filter="1",
                                     per_page="250",
                                     min_upload_date=startdate,
                                     max_upload_date=enddate,
                                     radius_units="km",
                                     radius=rad,
                                     lat=latitude,
                                     lon=longitude)
        
        parsed = json.loads(shots.decode('utf-8'))
        for key in parsed:
            if isinstance(parsed[key], dict): 
                x = type(parsed[key])
                newdict = parsed[key]
                for key in newdict:
                    y = type(newdict[key])
                    if isinstance(newdict[key], list): 
                        print(newdict[key])
                        for item in newdict[key]:
                            for key in item:
                                photo_id = str(item["id"].encode("utf-8"))[2:][:-1]
                            if photo_id not in done:
                                done.append(photo_id)
                                longt = str(item["longitude"])
                                lat = str(item["latitude"])
                                user_internal_id = str(item["owner"].encode("utf-8"))[2:][:-1]
                                user_name = str(item["ownername"].encode("utf-8"))[2:][:-1]
                                date_taken = str(item["datetaken"].encode("utf-8"))[2:][:-1]
                                date_upload = str(item["dateupload"].encode("utf-8"))[2:][:-1]
                                visit = "https://www.flickr.com/photos/" + user_internal_id + "/" + photo_id
                                raw_file.write(
                                    '"' + photo_id + '";"' + user_internal_id + '";"' + user_name + '";"' + lat + '";"' + longt + '";"' + date_taken + '";"' + date_upload + '";"' +  visit + '"\n')
                                donepids.write(photo_id + "\n")
                            else:
                                pass

        print(str(page) + " of " + str(total_pages) + " is done.")
        page = page + 1

    firstdate = firstdate + TenDays
    finaldate = finaldate + TenDays
    print (finaldate)

    if limitDate < firstdate:
        add_data = False

    # if firstdate * TenDays * 5 < firstdate:
    #     add_data = False

raw_file.close()                            # Closing the CSV file
donepids.close()                            # Closing the progress tracker file

print ("Process complete")

