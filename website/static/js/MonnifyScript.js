function payWithMonnify(
    price_amount,
    first_name,
    last_name,
    email,
    API_KEY,
    CONTRACT_CODE,
    description,
    tier,
    user_id

    ) {
    try {
        MonnifySDK.initialize({
            amount: parseInt(price_amount),
            currency: "NGN",
            reference: new String((new Date()).getTime()),
            customerFullName: `${first_name} ${last_name}`,
            customerEmail: `${email}`,
            apiKey: `${API_KEY}`,
            contractCode: `${CONTRACT_CODE}`,
            paymentDescription: `${description}`,
            metadata: {
                "name": `${first_name}`,
                "tier": `${tier}`
            },
            // incomeSplitConfig: [{
            //     "subAccountCode": "MFY_SUB_342113621921",
            //     "feePercentage": 50,
            //     "splitAmount": 1900,
            //     "feeBearer": true
            // }, {
            //     "subAccountCode": "MFY_SUB_342113621922",
            //     "feePercentage": 50,
            //     "splitAmount": 2100,
            //     "feeBearer": true
            // }],
            onLoadStart: () => {
                console.log("loading has started");
            },
            onLoadComplete: () => {
                console.log("SDK is UP");
            },
            onComplete: function(response) {
                //Implement what happens when the transaction is completed.
                console.log(response['status']);

                form_data = new FormData()
                form_data.append('amount', `${price_amount}`)
                form_data.append('user_id', user_id)
                form_data.append('status', response['status'])
                fetch('/update-user-details', {
                    method: 'POST',
                    body: form_data
                })
                .then(response => response.text())
                .then((data) => {
                    try {
                        if (data == "Success") {
                            ModalFlashShow("Voho Subscription", "Subscription successful!", "success")
                            setTimeout(()=>{
                                ModalFlashHide()
                                location.href = '/dashboard/3'
                            } , 3000)
                        } if (data == "cancelled") {
                            ModalFlashShow("Voho Subscription", "Subscription cancelled!", "error")
                            setTimeout(()=>{
                                ModalFlashHide()
                                location.href = '/dashboard/6'
                            } , 3000)
                        } if (data == "failed") {
                            console.log(`Data------> ${data}\nResponse-Status: ${response['status']}`)
                            ModalFlashShow("Voho Subscription", "Snap! Something went wrong, try again.", "error")
                            setTimeout(()=>{
                                ModalFlashHide()
                                location.href = '/dashboard/6'
                            } , 3000)
                        } 
                    } catch(e) {
                        console.log(e);
                        console.log(data);
                        ModalFlashShow("Voho Subscription", "Snap! Something went wrong, try again.", "error")
                        setTimeout(()=>{
                            ModalFlashHide()
                            location.href = '/dashboard/6'
                        } , 3000)
                        
                    }
                })
            },
            onClose: function(data) {
                //Implement what should happen when the modal is closed here
                console.log(data);   
            }
        });
    } catch(e) {
        // statements
        ModalFlashShow("Voho Subscription", "Check your internet connection and try again!", "error")
        // setTimeout(()=>{
        //     ModalFlashHide()
        // } , 30000)
        console.log(e);
    }
}