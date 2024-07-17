# BIT-Voice-Assistant



Step 1: Set Up Firebase Project
1). Go to the Firebase Console.
2). Click on "Add Project" and follow the setup instructions.
3). Once the project is created, click on "Project Settings" and go to the "Service accounts" tab.
4). Generate a new private key and download the JSON file containing your credentials.

Step 2: Install Firebase Admin SDK
In your terminal or command prompt, install the Firebase Admin SDK:
pip install firebase-admin

Step 3: Initialize Firebase in Your Code
In your Python code, initialize Firebase using the credentials file you downloaded in Step 1:

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project-id.firebaseio.com'
})

Replace "path/to/your/firebase/credentials.json" with the path to your Firebase Admin SDK credentials file, and 'https://your-firebase-project-id.firebaseio.com' with your actual Firebase database URL.

Step 4: Store Data in Firebase
Modify your code to store data in Firebase. For example, to store user commands:

def store_command(question, language_choice, voice_gender):
    # Get a reference to the database
    ref = db.reference('/voice_commands')

    # Push the voice command data to the database
    ref.push({
        'question': question,
        'language_choice': language_choice,
        'voice_gender': voice_gender
    })

Step 5: Run Your Application
Run your Python application. Make sure it's properly configured to use the Firebase Admin SDK. When the store_command function is called, it will push data to your Firebase Realtime Database.

Step 6: Check Firebase Console
Go to the Firebase Console, navigate to your project, and check the Realtime Database section. You should see data being added under the /voice_commands node.



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.





