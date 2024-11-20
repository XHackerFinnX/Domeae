document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.icon-bin').forEach(bin => {
        bin.addEventListener('click', async (event) => {
            const taskItem = bin.closest('.task-item');
            
            const pContent = taskItem.querySelector('p')?.innerText || '';
            const spanAssigned = taskItem.querySelector('span:not(b span)')?.innerText || '';
            const spanPrice = taskItem.querySelector('b > span')?.innerText || '';

            console.log(pContent, spanAssigned, spanPrice ? spanPrice : '');

            await DeleteCompleted(pContent, spanAssigned, spanPrice ? spanPrice : '');
        });
    });
});

async function DeleteCompleted(pcontent, sassigned, sprice) {
    const contentData = {
        pcontent: pcontent,
        sassigned: sassigned,
        sprice: sprice
    };

    const response = await fetch("/delete_completed", {
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