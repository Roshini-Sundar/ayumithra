const firebaseConfig = {
    apiKey: "AIzaSyCEYJc7AgJg1HbLLDKAoTOm9No7jEoTmOw",
    authDomain: "ayumithra-b2ab1.firebaseapp.com",
    databaseURL: "https://ayumithra-b2ab1-default-rtdb.firebaseio.com",
    projectId: "ayumithra-b2ab1",
    storageBucket: "ayumithra-b2ab1.firebasestorage.app",
    messagingSenderId: "464837414960",
    appId: "1:464837414960:web:b4e5a19c7aea272f1c5df5"
  };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    
    // Reference to the signup database
    const signupdb = firebase.database().ref("signup");
    
    // Form Submission Event
    document.getElementById("signupForm").addEventListener("submit", function (e) {
      e.preventDefault();
    
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
    
      // Check if email exists
      signupdb.orderByChild("email").equalTo(email).once("value", (snapshot) => {
        if (snapshot.exists()) {
          alert("Email already exists!");
        } else {
          signupdb.push({ email, password });
          alert("Sign-Up Successful!");
          window.location.href = "/profile";
        }
      });
    });
    