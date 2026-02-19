import datetime
from integration.utility.aes256_hmac_sha384_hex import AES256HMACSHA384HEX

class PgService:
    def __init__(self,
                 client_code="DJ020",
                 trans_user_name="DJL754@sp",
                 trans_user_password="4q3qhgmJNM4m",
                 auth_key="ISTrmmDC2bTvkxzlDRrVguVwetGS8xC/UFPsp6w+Itg=",
                 auth_iv="M+aUFgRMPq7ci+Cmoytp3KJ2GPBOwO72Z2Cjbr55zY7++pT9mLES2M5cIblnBtaX",
                 call_back_url="http://127.0.0.1:8000/pg/response/",
                 sp_domain="https://stage-securepay.sabpaisa.in/SabPaisa/sabPaisaInit?v=1"
    ):
        self.client_code = client_code
        self.trans_user_name = trans_user_name
        self.trans_user_password = trans_user_password
        self.call_back_url = call_back_url
        self.sp_domain = sp_domain

        
        self.crypto = AES256HMACSHA384HEX(auth_key, auth_iv)

    def request(self):
        payer_name = 'vimal'
        payer_mobile = '1234567891'
        payer_email = 'test@gmail.com'

        client_txn_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        amount = '10'
        amount_type = 'INR'
        channel_id = 'W'

    

        url = (
            f"payerName={payer_name}"
            f"&payerEmail={payer_email}"
            f"&payerMobile={payer_mobile}"
            f"&clientTxnId={client_txn_id}"
            f"&amount={amount}"
            f"&clientCode={self.client_code}"
            f"&transUserName={self.trans_user_name}"
            f"&transUserPassword={self.trans_user_password}"
            f"&callbackUrl={self.call_back_url}"
            f"&amountType={amount_type}"
            f"&channelId={channel_id}"
        
        )

        encrypted = self.crypto.encrypt(url).strip()
        return encrypted

    def res(self, enc_response):
        decrypted = self.crypto.decrypt(enc_response.strip())
        return decrypted.split("&")
