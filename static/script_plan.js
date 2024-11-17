async function sendGetRequest() {

    const response = await fetch("/plan_v", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify()
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}