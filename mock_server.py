from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from datetime import date
app = FastAPI(title="Kapture Finance Vapi Mock Tools")

ACCOUNTS = {"rahul_demo": {"verified_value":"1998", "amount":8499, "dpd":12, "loan_type":"personal loan"}}

@app.post("/vapi/tools")
async def tools(payload: dict[str, Any]):
    msg=payload.get("message", payload)
    calls=msg.get("toolCallList", [])
    results=[]
    for c in calls:
        name=c.get("name") or c.get("function",{}).get("name")
        p=c.get("parameters",{})
        if name=="verify_customer":
            a=ACCOUNTS.get(p.get("customer_ref"))
            ok=bool(a and p.get("verification_value")==a["verified_value"])
            results.append({"toolCallId":c.get("id"),"name":name,"result":{"verified":ok}})
        elif name=="log_promise_to_pay":
            results.append({"toolCallId":c.get("id"),"name":name,"result":{"status":"recorded","ptp_id":"PTP-DEMO-001"}})
        elif name=="send_payment_link":
            results.append({"toolCallId":c.get("id"),"name":name,"result":{"status":"sent","link":"https://pay.example.invalid/demo"}})
        elif name=="mark_disposition":
            results.append({"toolCallId":c.get("id"),"name":name,"result":{"status":"logged"}})
        elif name=="escalate_to_agent":
            results.append({"toolCallId":c.get("id"),"name":name,"result":{"status":"queued","ticket_id":"CASE-DEMO-001"}})
        else:
            results.append({"toolCallId":c.get("id"),"result":{"error":"unknown_tool"}})
    return {"results":results}
