from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import datetime

# Create your views here.

MAIL_SERVICE_ROUTE = r"https://tema4-send-email.azurewebsites.net/api/HttpTrigger1?code=jSw3kMS4yV50NE8clvBMCAOY72Ak6tctIu/PNLAatQ/Fd5HzRHo1BA=="
DATABASE_URL = r"https://datastore-project-236517.appspot.com"

	
def remind(request):
	req = requests.get(DATABASE_URL + "/reservations")
	req_json = req.json()

	print(req_json)

	for reservation_json in req_json:
		from_date_timestamp = int(reservation_json["fromDateTimestamp"])
		to_date_timestamp = int(reservation_json["toDateTimestamp"])
		diff_check = int(reservation_json["nrRemindHours"])
		wasReminded = reservation_json["wasReminded"]

		if not wasReminded and reservation_json['status'] == "approved":
				current_date_obj = datetime.datetime.now()
				from_date_obj = datetime.datetime.fromtimestamp(from_date_timestamp)

				diff = from_date_obj - current_date_obj
				days, seconds = diff.days, diff.seconds

				print(from_date_obj)
				print(current_date_obj)

				diff_hours = days * 24 + seconds // 3600 

				print(diff_hours)

				if diff_hours <= diff_check and diff_hours >= 0:
					client_email = reservation_json["email"]
					placeURLRequest = "{}/places/{}".format(DATABASE_URL, reservation_json['placeId'])
					#roomURLRequest = "{}/rooms/{}".format(DATABASE_URL, reservation_json['roomId'])

					print(placeURLRequest)
					#print(roomURLRequest)

					print("Before placeinfo")

					placeInfo = requests.get(placeURLRequest).json()
					#roomInfo = requests.get(roomURLRequest).json()

					email_message = "Va reamintim ca in aproximativ {} ore aveti rezervare la {}, \
					camera NU_MERGHE_ROOM".format(reservation_json['nrRemindHours'], placeInfo['name'])

					mail_data = {
									"to": client_email,
									"subject": "Reservation",
									"mess": email_message
								}

					print("Before mail")

					requests.post(MAIL_SERVICE_ROUTE, json=mail_data)
					
					reservation_json["wasReminded"] = True
					updateURL = "{}/reservations/{}".format(DATABASE_URL, reservation_json['id'])			

					print("Before update")

					requests.put(updateURL, json=reservation_json)

		print("Handled reservation!")
	return HttpResponse(status=200)


def statistics(request):
	places_request = "{}/places".format(DATABASE_URL)
	places_list = requests.get(places_request).json()
	places_list = [elem for elem in places_list if "nrSearch" in elem]
	places_list.sort(key=lambda elem: int(elem["nrSearch"]), reverse=True)

	if len(places_list) > 10:
		places_list = places_list[:10]

	return HttpResponse(json.dumps(places_list))