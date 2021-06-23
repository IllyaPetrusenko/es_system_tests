import uuid

cancel_tender_payload_full_data_model = {
    "amendments": [
        {
            "rationale": "cancel_tender: amendments[0].rationale",
            "description": "cancel_tender: amendments[0].description",
            "documents": [
                {
                    "documentType": "cancellationDetails",
                    "id": "{{Document_1}}",
                    "title": "cancel_tender: amendments[0].documents[0].title",
                    "description": "cancel_tender: amendments[0].documents[0].description"
                }
            ],
            "id": str(uuid.uuid4())
        }
    ]
}

cancel_tender_payload_obligatory_data_model = {
    "amendments": [
        {
            "rationale": "cancel_tender: amendments[0].rationale",
            "id": str(uuid.uuid4())
        }
    ]
}