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
  
  // Reference to the profiles database
  const profiledb = firebase.database().ref("profiles");
  
  // Form Submission Event
  document.getElementById("profileForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from reloading the page
  
    // Retrieve form values
    //const userid = document.getElementById("userid").value.trim();
    const username = document.getElementById("username").value.trim();
    const dob = document.getElementById("dob").value;
    const email=document.getElementById("email").value.trim();
  
    // Input validation
    if (!username || !dob || !email) {
      alert("All fields are required!");
      return;
    }
  
    // Check if User ID already exists in the database
    profiledb.orderByChild("username").equalTo(username).once("value", (snapshot) => {
      if (snapshot.exists()) {
        alert("User Name already exists! Please choose a different Name.");
      } else {
        // Push new profile to Firebase
        profiledb.push({ username, dob, email})
          .then(() => {
            // Save the username in local storage
            localStorage.setItem("username", username);
  
            // Notify the user and redirect
            alert("Profile created successfully!");
            window.location.href = "/homepage"; // Redirect to the home page
          })
          .catch((error) => {
            console.error("Error creating profile:", error);
            alert("An error occurred while creating the profile. Please try again.");
          });
      }
    });
  });
  