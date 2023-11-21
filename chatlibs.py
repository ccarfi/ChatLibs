import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
imageModel = "dall-e-3"
chatModel = "gpt-4"

# Generate the initial story based on the topic
def gpt4_generate_story(topic):

    prompt = f"Write a creative, silly 75-word children's story about {topic}. Include characters, a conflict, rising action, a surprising resolution, and a piece of short dialogue."
    response = openai.ChatCompletion.create(
        model=chatModel,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']


# Generate a title for the story
def gpt4_generate_title(story):

    prompt = f"Create a catchy and creative title for this children's story: {story}"

    response = openai.ChatCompletion.create(
        model=chatModel,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']


# Ask the user for words to fill in the placeholders
def fill_in_blanks_with_user_input(blank_story):
    placeholders = ['an adjective', 'a noun', 'a verb', 'another adjective', 'one more adjective', 'another noun', 'a final adjective']
    user_inputs = {}

    for placeholder in placeholders:
        user_input = input(f"Enter {placeholder.strip('[]')}: ")
        user_inputs[placeholder] = user_input

# debugging rows
#    print("Story with placeholders:", blank_story)
#    print("User inputs:",user_inputs)

    print("Filling in the blanks in your story...")

    # Constructing the prompt
    prompt = (f"Integrate the replacement values included below into this original story. \n\nOriginal Story:\n{blank_story}\n"
             f"Replacement values to add into the story:\n{user_inputs}\n\n"
             f"Updated story that includes all the replacement values:")

    response = openai.ChatCompletion.create(
        model=chatModel,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']



# Generate an image based on the story
def dalle_generate_image(story):

    PROMPT = (f"Please create an photorealistic image based on this narrative:\n\n{story}\n")
    response = openai.Image.create(
        model=imageModel,
        prompt=PROMPT,
        n=1,
        size="1024x1024",
    )
    return(response["data"][0]["url"])



# Main program
def main():
    topic = input("Enter a topic for the story: ")
    print ("Thinking about that topic...")
    story = gpt4_generate_story(topic)
    title = gpt4_generate_title(story)
    print("Story Title:", title)
    completed_story = fill_in_blanks_with_user_input(story)
    print("Here is your story!\n\n", completed_story)

    print("\n\nCreating image for the story...\n")
    image = dalle_generate_image(completed_story)
    print(image)

if __name__ == "__main__":
    main()