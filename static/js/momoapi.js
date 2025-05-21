document.addEventListener("DOMContentLoaded", function () {
  // Appel de ta fonction ici
  verifierPaiement();
});

let essais = 0;
const delai = 5000; // 5 secondes

function verifierPaiement() {
  const access_token = document.getElementById("access_token").value;
  const apiuser = document.getElementById("apiuser").value;

  fetch("/momopay/paymentstatus/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ apiuser: apiuser, access_token: access_token }),
  })
    .then((res) => res.json())
    .then((data) => {
      const statut = data.status;
      if (statut === "PENDING" && essais < 10) {
        essais++;
        document.getElementById("resultat").innerText =
          "Statut du paiement : " + statut;
        setTimeout(() => verifierPaiement(), delai);
      } else {
        document.getElementById("resultat").innerText =
          "Statut du paiement : " + statut;
      }
    })
    .catch((error) => {
      // console.error(error);
      if (essais < 10) {
        essais++;
        setTimeout(() => verifierPaiement(), delai);
      } else {
        document.getElementById("resultat").innerText =
          "Erreur : impossible de vérifier.";
      }
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
