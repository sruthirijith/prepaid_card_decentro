from fastapi import FastAPI
import datetime
import json
import requests
from fastapi import APIRouter


router = FastAPI()



#-------------------------------------------------------------#
#------------------- DECENTRO API  ----------------#



# ----------------------create virtual account --------------------------------#

@router.post("/Virtualaccount")
async def Decentro_Create_Virtual_Account(bank_code:str,name:str,pan:str,email:str,
                                          mobile:str,address:str,kyc_verified:int,kyc_check:int,min_balance:int,
                                          transaction_limit:int,customer_id:str):
    
    """This API allows you to create a virtual account with single/multi provider feature for a consumer or business in real-time."""
    
    url = "https://in.staging.decentro.tech/v2/banking/account/virtual"

    payload = json.dumps({
        "bank_codes": [
            bank_code
        ],
        "name": name,
        "pan": pan,
        "email":email ,
        "mobile": mobile,
        "address": address,
        "kyc_verified": kyc_verified,
        "kyc_check_decentro": kyc_check ,
        "minimum_balance": min_balance,
        "transaction_limit": transaction_limit,
        "customer_id": customer_id,
        "virtual_account_balance_settlement": "disabled",
        "upi_onboarding": False
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'lAiW0MzBC4tElarRekM8K1S7Op0rMDEJ',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    x = response.json()
    if x['status'] == 'SUCCESS':

        print(x)

        return x

    else:
        print(x)
        return {"status":x['status'],"message" : x['message']}


#----------------------------Fetch virtual account details ----------------------------#

@router.get("/accountdetails")
async def Decentro_Virtual_Account_Details(account_number:str):
    
    """"This API allows you to fetch the account details of a specific account that have been created or linked by your consumer/business via your platform"""
    
    url = "https://in.staging.decentro.tech/core_banking/account_information/fetch_details?type=virtual&account_number={}&qr_requested=1".format(account_number)

    payload = {}
    files = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'lAiW0MzBC4tElarRekM8K1S7Op0rMDEJ',
        'provider_secret': 'Mj4IkIITMoIHIRl0JNaBc5BDWFjJQGos',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    res = response.json()
    if res['status'] == 'success':
        print(res)
        details = res["accounts"]
        output = details[0]
        return {
            "status":res['status'],"Account_type":output['type'],"Account_number":output['accountNumber'],
            "IFSC code":output['ifscCode'],"Allowed_methods":output['allowedMethods'],"currency":output['currency'],
            "transaction_limit":output['transactionLimit'],"Mininum_Balance":output['minimumBalance'],
            "Customer_id":output['customerId'],"mobile":output['mobile'],"UPLI_id" :output['upiId']
        }

    else:
        print(res)
        return {"status":400,"Message":res["message"]}



# -------------get balance --------------------------------#

@router.get("/getbalanace")
async def Decentro_Virtual_Account_Balance(account_number:str,phone:str):
    
    """This API is used to retrieve the latest balance in the created virtual account"""
    
    url = "https://in.staging.decentro.tech/core_banking/money_transfer/get_balance?account_number={0}&customer_id=cust_0003&mobile_number={1}".format(account_number,phone)

    payload = ""
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'lAiW0MzBC4tElarRekM8K1S7Op0rMDEJ',
        'provider_secret': 'Mj4IkIITMoIHIRl0JNaBc5BDWFjJQGos',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.json()

    return res


#------------------Get virtual account statement ---------------------------#

@router.get('/accountstatement')
async def Decentro_Virtual_Account_Statement(from_date: datetime.date,to_date:datetime.date,customer_id:str,account_number:str,phone:str):
    
    """To retrieve the detailed transaction statement for the requested account number, 10 records at a time,"""
    
    url = "https://in.staging.decentro.tech/core_banking/money_transfer/get_statement?from={0}&to={1}&account_number={2}&customer_id={3}&mobile_number={4}&page=1".format(from_date,to_date,account_number,customer_id,phone)

    payload = ""
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'lAiW0MzBC4tElarRekM8K1S7Op0rMDEJ',
        'provider_secret': 'Mj4IkIITMoIHIRl0JNaBc5BDWFjJQGos',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.json()


#----------------------- Fetch Consolidated Statement ---------------------------------------------#

@router.get("/virtualconsolidate")
async def Virtual_account_Fetch_Consolidated_Statement(From_date:datetime.date,To_date:datetime.date):

    url = "https://in.staging.decentro.tech/v2/banking/account/virtual/consolidated_account_statement?from={0}&to={1}".format(From_date,To_date)

    payload = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'lAiW0MzBC4tElarRekM8K1S7Op0rMDEJ',
        'provider_secret': 'Mj4IkIITMoIHIRl0JNaBc5BDWFjJQGos'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


#----------------------- Create MIN KYC Wallet(Request for OTP) ------------------------------#

@router.post("/createwallet")
async def Decentro_Wallet_CreateWallet(reference_id:str,mobile:str,document_type:str,document_id:str,
                                      first_name:str,middle_name:str,last_name:str,DOB:str,gender:str,address:str,
                                      pin_code:str,email:str,city:str,state_code:int,virtual_card_count:int,address_type:str):
    
    """This API is used to initiate the creation of a MIN KYC wallet using Mobile OTP. If the request is successful, please complete the wallet creation using the Wallet Creation API."""
    
    url = "https://in.staging.decentro.tech/v2/prepaid/consumer"

    payload = json.dumps({
      "reference_id": reference_id,
      "purpose": "test_purpose",
      "mobile": mobile,
      "consent": True,
      "document_type": document_type,
      "document_identifier": document_id,
      "name": {
        "first": first_name,
        "middle": middle_name,
        "last": last_name
      },
      "date_of_birth": DOB,
      "gender": gender,
      "address": address,
      "pin_code": pin_code,
      "provider_params": {
        "email": email,
        "city": city,
        "state_code": state_code,
        "address_type": address_type,
        "virtual_card_count": virtual_card_count
      }
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.json()


#-----------------Confirm MIN KYC Wallet (Verify OTP) -----------------------------#

@router.post('/confirmwallet')
async def Decentro_Wallet_ConfirmWallet(reference_id:str,transaction_id:str,otp:str):
    
    """This API allows for the verification of user registration via an OTP sent to the specified mobile. The mobile number will be the same as the one passed during the time of creating the wallet."""
    
    url = "https://in.staging.decentro.tech/v2/prepaid/consumer/9526621880/verify"

    payload = json.dumps({
        "reference_id": reference_id,
        "original_transaction_id": transaction_id,
        "purpose": "test_purpose",
        "consent": True,
        "otp": otp
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.json()


#-------------------- Get Wallet Details ----------------------#

@router.get("/walletdetails")
async def Decentro_Wallet_Get_Wallet_Details(mobile:str):
    
    """This API allows fetching the details of the wallet associated with the specified mobile."""
    
    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{}".format(mobile)

    payload = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


# ---------------------- get wallet statement ----------------------------------------#

@router.get('/walletstatement')
async def Decentro_wallet_Get_Wallet_Statement(mobile:str,date_from:datetime.date,date_to:datetime.date,page:int):
    
    """This API allows fetching the statement of the wallet associated with the specified mobile. This API will return all the successful transactions that take place through the wallet."""
    
    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{0}/statement?from={1}&to={2}&page={3}".format(mobile,date_from,date_to,page)

    payload = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()



#------------------------------get consolidated details ---------------------#

@router.get('/consolidateddetails')
async def Decentro_Wallet_Consolidated_Details():
    
    """This API allows fetching the consolidated details of all the wallets linked with the company"""
    
    url = "https://in.staging.decentro.tech/v2/prepaid/wallet?fetch_consumer_details=1&status=active&kyc=min&type=VANILLA"

    payload = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

# ---------------------- Update wallet status -------------------------------#

@router.put("/updatewallet")
async def Decentro_Wallet_Update_Wallet_Status(phone:str,ref_id :str,purpose:str,action:str):

    """purpose : wallet lock / wallet unlock
      **  action : lock / unlock """

    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{}".format(phone)

    payload = json.dumps({
        "reference_id": ref_id,
        "purpose": purpose,
        "action": action,
        "consent": True
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)


#------------------------- request prepaid card---------------------------------#

@router.post('/requestcard')
async def Decentro_Card_Request_Prepaid_Card(phone:str,ref_id:str,kit_number:str,address:str,pin_code:str,city:str,state_code:int):
    
    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{}/virtual/request".format(phone)

    payload = json.dumps({
        "reference_id": ref_id,
        "purpose": "test_purpose",
        "consent": True,
        "kit_number": kit_number,
        "address_information": {
            "address": address,
            "pin_code": pin_code,
            "city": city,
            "state_code": state_code
        }
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


#------------------------------- Set Card PIN ---------------------------------------#

@router.put('/setpin')
async def decentro_Card_Set_Card_Pin(phone:str,ref_id:str,kit_number:str):
    
    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{}/card/pin".format(phone)

    payload = json.dumps({
        "reference_id": ref_id,
        "purpose": "Setting the physical PIN for my card",
        "consent": True,
        "kit_number": kit_number
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()



# ----------------- Get card details ----------------------------------#

@router.get('/carddeatils')
async def Decentro_Card_Details(phone:str,card_type:str,kit_number:str,sub_type:str):

    """card_type (optional) : physical,virtual,None
    ** kit_number(Optional)
    ** sub_type (optional) : values: Vanilla, Parent, Child or None"""

    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{0}/card?type={1}&kit_number={2}&sub_type={3}".format(phone,card_type,kit_number,sub_type)

    payload = {}
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


# ---------------------- Update Physical Card -------------------------------------#
@router.put('/updatecard')
async def Decentro_Card_Update_Card(phone:str,ref_id:str,purpose:str,action:str):

    """This API allows to lock/ unlock a virtual card associated with the specified mobile.
        ** purpose : eg: Physical card lock / Physical card unlock
        action : lock / unlock """

    url = "https://in.staging.decentro.techv2/prepaid/wallet/{}/physical".format(phone)

    payload = json.dumps({
        "reference_id": ref_id,
        "purpose": purpose,
        "action": action,  # lock , unlock
        "consent": True
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()



#------------------------ add Card ---------------------------------------------#

@router.post("/addcard")
async def Decentro_Card_Add_Card(phone:str,ref_id:str,kit_number:str,card_number_last_4_digits:str,card_type:str):

    """ This API allows to activate an additional card against the wallet associated with the specified mobile. The card to be activated can be virtual or physical
        card_type: physical / virtual """



    url = "https://in.staging.decentro.tech/v2/prepaid/wallet/{}/card".format(phone)

    payload = json.dumps({
        "reference_id": ref_id,
        "purpose": "Activating my card",
        "consent": True,
        "kit_number": kit_number,
        "provider_params": {
            "card_number_last_4_digits": card_number_last_4_digits,
            "type": card_type
        }
    })
    headers = {
        'client_id': 'xpayback_staging',
        'client_secret': 'm2IR43mFWlkcZ1TYxoVfFloPXJNiLSCG',
        'module_secret': 'k0a4IzGRmKMQYAaRDbxWFKrhxDY0En04',
        'provider_secret': 'C0mqoMux62KjmKNuwMHQmXTBcOAIEuI7',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
