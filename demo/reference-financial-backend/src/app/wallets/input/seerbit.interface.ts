export interface nameEnquiry {
  accountnumber: string;
  bankcode: string;
}

export interface getOtpResponse {
  responseCode: string;
  message: string;
  data: {
    otp: string;
    category: string;
    expires: string;
  };
}

export interface transferFunds {
  reference?: string;
  amount: string;
  currency?: string;
  description: string;
  accountNumber: string;
  bankCode: string;
  actionType?: string;
  passKey?: string;
  transactionPin?: string;
}

export interface signatureResponse {
  responseCode: '00';
  message: 'Success';
  data: {
    signature: string;
  };
  input: transferFunds;
}

export interface initialFundTransfer {
  responseCode: string;
  message: string;
  data: {
    reference: string;
    linkingreference: string;
  };
}
