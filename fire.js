<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCscPJ_aIJ7EUkLqJEQlAQa5SmcEr22Mzc",
    authDomain: "toscanocombr-1d11f.firebaseapp.com",
    projectId: "toscanocombr-1d11f",
    storageBucket: "toscanocombr-1d11f.firebasestorage.app",
    messagingSenderId: "929855621300",
    appId: "1:929855621300:web:7a60af14894cc89807efe1",
    measurementId: "G-9CQ1BV23PE"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>