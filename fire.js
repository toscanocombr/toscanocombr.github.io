import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js'
import { getFirestore, collection, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'

// import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js'
// TODO: Replace the following with your app's Firebase project configuration

const firebaseConfig = {
  apiKey: "AIzaSyBif4hFKR4_D5iv62H_36ENUotecTe0cy0",
  authDomain: "pulsiveapp.firebaseapp.com",
  projectId: "pulsiveapp",
  storageBucket: "pulsiveapp.appspot.com",
  messagingSenderId: "487759123498",
  appId: "1:487759123498:web:e9eef1a827ffecdd095f53",
  measurementId: "G-1FVM76L0BJ"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);



// Get a list of cities from your database
async function getCities(db) {
  const citiesCol = collection(db, 'site');
  const citySnapshot = await getDocs(citiesCol);
  const cityList = citySnapshot.docs.map(doc => doc.data());
  return cityList;
}
var sites = getCities(db)

console.log(sites)
console.log('teste')





function openModal() {

  var clickedImageSrc = this.src;
  var modalImage = document.querySelector("#myModal img");
  var modal = document.getElementById("myModal");
  
  modalImage.src = clickedImageSrc;
  modal.style.display = "block";
  modal.style.display = "block";
}

var images = document.querySelectorAll("#insta-pulsive img");
images.forEach(function(image) {
  image.addEventListener("click", openModal);
});

document.addEventListener("keydown", function(event) {
  if (event.key === "Escape") {
      var modal = document.getElementById("myModal");
      modal.style.display = "none";
  }
});