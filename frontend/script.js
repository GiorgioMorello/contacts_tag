

let tagText;
let data;
const consultBtn = document.getElementById("consultBtn")



function showContacts(contacts) {

     const tbody = document.getElementById("contactsTableBody");
     

    // limpa tabela antes de renderizar
    tbody.innerHTML = "";

    contacts.forEach(item => {
        const row = document.createElement("tr");

        const nomeTd = document.createElement("td");
        nomeTd.textContent = item.Contato;

        const contatoTd = document.createElement("td");
        contatoTd.textContent = item.Número;

        const tagTd = document.createElement("td");
        tagTd.textContent = item.Tag;

        row.appendChild(nomeTd);
        row.appendChild(contatoTd);
        row.appendChild(tagTd);

        tbody.appendChild(row);
    });

}


function onChangeTagText() {
   const tag = document.getElementById("tagText").value
   tagText = tag
   console.log(tag)
}




async function makeRequest(url) {
    const resp = await fetch(url)
    return await resp.json()
}


async function getContacts() {

    const url = `http://127.0.0.1:8000/contact-tag${tagText ? `?tag_name=${tagText}` : ''}`
    console.log(url)
    data = await makeRequest(url)

    

    if (data) {
        showContacts(data)
    }
    
    
    
}

document.getElementById("tagText").addEventListener("change", onChangeTagText)
consultBtn.addEventListener("click", getContacts)






