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
  
  // Reference the signup collection in Firebase Realtime Database
  const signupdb = firebase.database().ref('signup');
  
  // Event listener for form submission
  document.getElementById('signupForm').addEventListener("submit", submitForm);
  
  function submitForm(e) {
    e.preventDefault(); // Prevent default form submission
  
    // Get form values
    var email = getElementVal("email");
    var password = getElementVal("password");
  
    // Check if the email already exists in the database
    checkIfEmailExists(email, password);
  }
  
  function checkIfEmailExists(email, password) {
    signupdb.orderByChild("email").equalTo(email).once("value", snapshot => {
        if (snapshot.exists()) {
            // Email already exists
            alert("Email already exists. Please use a different email.");
        } else {
            // Email does not exist, save the data
            saveMessages(email, password);
  
            // Alert user and redirect to profile page
            alert("Sign Up Successful!");
            window.location.href = "/profile";  // Redirect to profile page
        }
    });
  }
  
  const saveMessages = (email, password) => {
    var newSignupEntry = signupdb.push();
    newSignupEntry.set({
        email: email,
        password: password
    });
  };
  
  const getElementVal = (id) => {
    return document.getElementById(id).value;
  };
  
  