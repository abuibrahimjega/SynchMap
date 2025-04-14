import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Adjust speaking rate
rate = engine.getProperty('rate')
print(f'Current speaking rate: {rate}')
engine.setProperty('rate', 125)

# Adjust volume
volume = engine.getProperty('volume')
print(f'Current volume level: {volume}')
engine.setProperty('volume', 1.0)

# Change voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Selecting a female voice

# Make the engine speak
engine.say("Hello World!")
engine.say(f'My current speaking rate is {rate}')
engine.runAndWait()

# Create a new engine instance for saving to file
file_engine = pyttsx3.init()
file_engine.setProperty('rate', 125)
file_engine.setProperty('volume', 1.0)
file_engine.setProperty('voice', voices[1].id)

# Save to a file
#file_engine.save_to_file('Hello World', 'test.mp3')
file_engine.runAndWait()

# Stop the engines
engine.stop()
file_engine.stop()

if engine._inLoop:
    engine.endLoop()

if file_engine._inLoop:
    file_engine.endLoop()
