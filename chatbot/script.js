const botData = {
    "responses": [
        {
            "patterns": ["college fees", "bannari amman institute of technology"],
            "response": "The college fees for Bannari Amman Institute of Technology depend on the course the student has selected."
        },
        {
            "patterns": ["college fees"],
            "response": "College fees can vary based on the institute and the course. For specific details about college fees, please provide the name of the institute."
        },
        {
            "patterns": ["campus review", "bannari amman institute of technology"],
            "response": "Bannari Amman Institute of Technology has a sprawling campus with state-of-the-art facilities. The campus provides a conducive environment for learning and offers various amenities to students."
        },
        {
            "patterns": ["campus review"],
            "response": "The institute's expansive grounds encompass cutting-edge infrastructure, fostering an ideal atmosphere for academic pursuits, and presenting a multitude of amenities for students."
        },
        {
            "patterns": ["testimonials", "bannari amman institute of technology"],
            "response": "Bannari Amman Institute of Technology has received positive testimonials from many students and alumni. They appreciate the quality of education, supportive faculty, and the opportunities provided for overall development."
        },
        {
            "patterns": ["testimonials"],
            "response": "The vibrant campus life at Bannari Amman Institute of Technology fosters a sense of community, encouraging students to engage in various extracurricular activities and collaborative projects."
        },
        {
            "patterns": ["ratings", "bannari amman institute of technology"],
            "response": "BIT has been rated highly by various ranking agencies and students. It is known for its academic excellence, infrastructure, and placement opportunities."
        },
        {
            "patterns": ["ratings"],
            "response": "Renowned for its commitment to academic excellence, impressive infrastructure, and remarkable placement opportunities, BIT stands out as a top-rated institution according to both ranking agencies and student testimonials."
        },
        {
            "patterns": ["achievements", "bannari amman institute of technology"],
            "response": "Bannari Amman Institute of Technology has achieved several accolades in the field of technical education. They have excelled in areas like research, innovation, and industry collaborations."
        },
        {
            "patterns": ["achievements"],
            "response": "Bannari Amman Institute of Technology stands as a beacon of educational excellence, garnering accolades for its noteworthy achievements in research, innovation, and impactful industry collaborations."
        },
        {
            "patterns": ["nirf ranking", "bannari amman institute of technology"],
            "response": "As of my knowledge cutoff in September 2021, Bannari Amman Institute of Technology was ranked among the top engineering institutes in India by the National Institutional Ranking Framework (NIRF). For the latest ranking information, I recommend checking the NIRF official website."
        },
        {
            "patterns": ["nirf ranking"],
            "response": "As of my last update in September 2021, Bannari Amman Institute of Technology held a position among the top engineering institutes in India according to the National Institutional Ranking Framework (NIRF). To access the most recent ranking information, I suggest visiting the official NIRF website."
        },
        {
            "patterns": ["infrastructure", "bannari amman institute of technology"],
            "response": "BIT boasts a modern infrastructure with well-equipped laboratories, libraries, sports facilities, hostels, and more. The campus provides a comfortable and conducive environment for learning and extracurricular activities."
        },
        {
            "patterns": ["infrastructure"],
            "response": "Bannari Amman Institute of Technology features state-of-the-art infrastructure, including well-equipped laboratories, libraries, sports facilities, hostels, and more. The campus offers a comfortable and enriching environment for academic pursuits and extracurricular activities."
        },
        {
            "patterns": ["location", "bannari amman institute of technology"],
            "response": "Bannari Amman Institute of Technology is located in Sathyamangalam, Erode district, Tamil Nadu, India. The campus is situated in a serene and scenic environment, offering a peaceful atmosphere for students."
        },
        {
            "patterns": ["location"],
            "response": "Bannari Amman Institute of Technology resides in the tranquil town of Sathyamangalam, nestled within the picturesque landscapes of Erode district, Tamil Nadu, India. The campus, surrounded by a serene and scenic environment, provides students with a peaceful and harmonious atmosphere for their academic journey."
        }
    ],
    "default_response": "I'm sorry, I don't have the ability to answer that question yet."
};

const sendButton = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBody = document.getElementById('chat-body');

sendButton.addEventListener('click', () => {
    const userText = userInput.value.trim();
    if (userText !== "") {
        displayMessage(userText, 'user-message');
        getBotResponse(userText);
        userInput.value = '';
    }
});

function displayMessage(message, className) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add(className);
    
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerText = message;
    
    messageContainer.appendChild(messageElement);
    chatBody.appendChild(messageContainer);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function getBotResponse(userMessage) {
    const botResponse = findResponse(userMessage.toLowerCase());
    displayMessage(botResponse, 'bot-message');
}

function findResponse(userMessage) {
    for (let i = 0; i < botData.responses.length; i++) {
        for (let j = 0; j < botData.responses[i].patterns.length; j++) {
            if (userMessage.includes(botData.responses[i].patterns[j].toLowerCase())) {
                return botData.responses[i].response;
            }
        }
    }
    return botData.default_response;
}

document.getElementById('clear-btn').addEventListener('click', () => {
    const chatBody = document.getElementById('chat-body');
    chatBody.innerHTML = ''; // Clear all chat messages
});
