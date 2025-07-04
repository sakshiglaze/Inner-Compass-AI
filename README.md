# Inner-Compass-AI

Inner Compass AI is an interactive web application designed to provide mental health support through empathetic AI conversations, guided meditations, and stress-relief games. The application aims to create a safe space for users to explore their feelings and find personalized coping strategies. URL : https://inner-compass-ai.streamlit.app/

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Features

- *AI-Powered Chat*: Engage in empathetic conversations with an AI assistant that responds based on user input and provides tailored advice.
- *Guided Meditation*: Follow structured meditative practices to help reduce stress and anxiety.
- *Stress-Relief Games*: Access a variety of relaxing games to unwind and enjoy.
- *Personalized Daily Planner*: Receive a custom daily planner with activities and motivational quotes to enhance your mental well-being.
- *Session Timer*: Keep track of your session duration, ensuring that you are aware of your time spent on self-care.

## Technologies Used

- *Streamlit*: For building the web application interface.
- *LangChain*: To manage conversation memory and context.
- *Google Generative AI*: For generating responses and personalized content.
- *Plotly*: For visualizing data and displaying radar charts.
- *HTML/CSS*: For custom styling of the application.
![image](https://github.com/user-attachments/assets/d3dbea5e-faff-429b-9a69-e4a690bf3cf1)


## Installation

To run the application locally, follow these steps:

1. *Clone the repository:*
   ```bash
   git clone https://github.com/yourusername/inner-compass-ai.git
   cd inner-compass-ai

2. *Set up a virtual environment (optional but recommended):*
   '''bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate

3. *Install the required packages:*
   '''bash
   pip install -r requirements.txt

4. *Set your Google API key:*
   Create a .env file in the root directory and add your API key:
      GOOGLE_API_KEY=YOUR_API_KEY
   
6. *Run the application:*
   streamlit run app.py

## Usage

- Navigate through the application using the provided buttons and links.
- Start a conversation with the AI assistant by clicking "Start Sharing."
- Choose options for meditation or games on the second page.
- Use the chat feature to discuss your feelings and receive guidance.

## Disclaimer
This AI assistant is not a substitute for professional mental health care. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
