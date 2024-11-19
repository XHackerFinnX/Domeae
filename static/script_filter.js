async function sendPostToday(section) {
    const contentData = {
        option: section
    };

    const response = await fetch("/filter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function sendPostPriority(section) {
    const contentData = {
        option: section
    };

    const response = await fetch("/filter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function sendPostUser(section) {
    const contentData = {
        option: section
    };

    const response = await fetch("/filter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function sendPostCompleted(section, name) {
    const contentData = {
        option: section,
        name: name
    };

    const response = await fetch("/filter_completed", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}

async function sendPostDeleteFilter(section) {
    const contentData = {
        option: section
    };

    const response = await fetch("/filter_delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(contentData)
    });
    
    const result = await response.json();

    if (response.ok){
        window.location.href = result.data;
    }
}