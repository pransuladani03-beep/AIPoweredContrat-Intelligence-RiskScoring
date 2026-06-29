def score_contract_risk(extracted_text, clause_category, ai_confidence):
    """
    Takes the raw text found by RoBERTa and applies business compliance rules.
    """
    # 1. Reject anything below 85% confidence
    if ai_confidence < 0.85:
        return {"status": "REJECTED", "reason": f"Low confidence ({ai_confidence * 100}%)"}
        
    alerts = []
    text_clean = extracted_text.lower()
    
    # 2. Risk Rule: Check for unwanted automatic renewals
    if clause_category == "Renewal Term" and ("automatic" in text_clean or "auto-renew" in text_clean):
        alerts.append("HIGH RISK: Auto-renewal clause detected. Requires manual end-date tracking.")
        
    # 3. Risk Rule: Check for unlimited financial damage
    if clause_category == "Liability" and ("unlimited" in text_clean or "without cap" in text_clean):
        alerts.append("CRITICAL RISK: Financial liability is completely uncapped!")
        
    return {
        "status": "APPROVED",
        "clause_type": clause_category,
        "extracted_text": extracted_text.strip(),
        "risk_level": "FLAGGED" if alerts else "SAFE",
        "compliance_alerts": alerts
    }

# Test your risk scoring engine directly
test_prediction = "The agreement will automatically renew for consecutive 2-year terms."
result = score_contract_risk(test_prediction, clause_category="Renewal Term", ai_confidence=0.92)

print("Compliance Risk Report:")
for key, value in result.items():
    print(f"**{key}**: {value}")
