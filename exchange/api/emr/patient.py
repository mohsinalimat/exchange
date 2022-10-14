import frappe
from exchange.api.shr_fhir.patient import shr_post_patient
from exchange.api.client_registry.utils import post_client

@frappe.whitelist()
def post_patient(payload):
	"""
		provider_id,
		facility_id,
		client_id = None,
		facility_client_id= None,
		first_name = None,
		last_name = None,
		middle_name = None,
		gender = None,
		date_of_birth = None,
		phone = None,
		email = None,
		national_id = None,
		huduma_no = None,
		passport_no = None,
		birth_cert_no = None,
		birth_notification_no = None
	"""
	payload = frappe._dict(payload)
	#VALIDATE PAYLOAD. TO BE MOVED TO ITS OWN FUNCTION ONCE WE IMPLEMENT ONE PAYLOAD FROM CLIENT.
	_validate_patient_payload(payload)
	#PUSH TO THE CLIENT REGISTRY AND RETURN PATIENT ID IF NONE EXISTED
	client_registry_patient = post_client(payload)
	shr_patient = shr_post_patient(client_registry_patient)
	return shr_patient

def _validate_patient_payload(payload):
	national_id, huduma_no, passport_no, birth_cert_no, birth_notification_no = payload.get("national_id"), payload.get("huduma_no"), payload.get("passport_no"), payload.get("birth_cert_no"), payload.get("birth_notification_no")
	if national_id == huduma_no == passport_no == birth_cert_no == birth_notification_no == None:
		frappe.throw("You have to provide at lease one of: National ID, Huduma No, Passport No, Birth Certificate No or Birth Nofitificaiton No.")