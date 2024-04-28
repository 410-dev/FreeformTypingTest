import requests
import google.generativeai as genai
import time
import json
import traceback


def fetchApiKey(authToken):
    url = "https://hysong.dev/keystore/api/labs/google-gemini/api-1.0-key-240429"
    response = requests.post(url, data={"auth": authToken})
    return response.text.strip()


def generate(userContent, apiKey):
    genai.configure(api_key=apiKey)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(userContent)
    return response.text


def readPromptFromFile():
    with open("llm-instruction-prompt.txt", "r") as file:
        return file.read()


def main(debugMode=False):
    print("TypingSpeedTester with LLM v0.1 alpha")
    print("=" * 30)
    authToken = "1234"
    apiKey = fetchApiKey(authToken)
    instructionPrompt = readPromptFromFile()

    print(f"API Key: {apiKey}")
    print("LLM Version: Gemini 1.0")
    print("Debug Mode: " + ("On" if debugMode else "Off"))
    print("=" * 30)
    input("Press enter key to begin testing. To end the test, press the enter key three times.")

    content = instructionPrompt + " "
    enterCount = 0
    startTime = time.time()

    while enterCount < 3:
        userInput = input("> ")
        if userInput == "":
            enterCount += 1
        else:
            enterCount = 0
            content += userInput + " "

    endTime = time.time()
    timeTaken = endTime - startTime
    charCount = len(content)
    words = content.split()
    wordCount = len(words)
    wordsPerMinute = (wordCount / timeTaken) * 60

    try:
        generatedResponse = generate(content, apiKey)
        jsonResponse = json.loads(generatedResponse)
        isValid = jsonResponse["valid"]
        reasoning = jsonResponse["reasoning"]

        # Show reasoning regardless of validation success
        print(f"LLM Reasoning: {reasoning}")

        if isValid:
            print("Validation Successful. Your typing results:")
            print(f"Time Taken: {timeTaken:.2f} seconds")
            print(f"Characters Written: {charCount}")
            print(f"Words per Minute: {wordsPerMinute:.2f}")
        else:
            print("Invalid input according to LLM.")
    except Exception as e:
        if debugMode:
            print("An error occurred:")
            traceback.print_exc()
            print("AI Generated Response (if available):")
            print(generatedResponse)
        else:
            print("An error occurred during validation. Showing results regardless:")
        print(f"Time Taken: {timeTaken:.2f} seconds")
        print(f"Characters Written: {charCount}")
        print(f"Words per Minute: {wordsPerMinute:.2f}")


if __name__ == "__main__":
    debug = input("Enable Debug Mode? (yes/no): ").lower() == "yes"
    main(debug)