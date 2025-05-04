from groq import Groq
from dotenv import load_dotenv
import os
import re
from image_gen import generate_image

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


output_dir = "./static"
os.makedirs(output_dir, exist_ok=True)


def split_content(content, max_length=4000):
    split_list = [content[i:i+max_length] for i in range(0, len(content), max_length)]
    return split_list


def summarize_chunks(content_chunks):
    summarize_chunks = []
    for chunk in content_chunks:
        prompt = [
            {
                "role": "user",
                "content": (
                    f"Imagine you're an expert in summarizing research content. "
                    f"I'll provide you with a research text, formatted as: {chunk}. "
                    "Your task is to summarize it as though explaining to someone with basic knowledge. "
                    "Keep technical terms, but make each one understandable with relatable analogies. "
                    "Use your own examples and explanations. Avoid adding introductions or conclusions."
                )
            }
        ]
        
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=prompt,
                model="llama3-8b-8192"
            )
            summarize_chunks.append(chat_completion.choices[0].message.content.strip())
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

    return " ".join(summarize_chunks)


def final_summary(summarized_content):
    n = len(summarized_content.split())
    prompt = [
        {
            "role": "user",
            "content": (
                f"Imagine you're an expert in summarizing research content, the summarized content has to be strictly {n} words. I'll provide research text in the format: {summarized_content}. STRICTLY FOLLOW THE FOLLOWING: Your task is to create a summary that retains all key details, aiming to explain it as though speaking to someone with only basic knowledge of the topic. Include the mathematical equations (if required). Keep all technical terms, carefully explaining each one without oversimplifying. The summary should be around half the length of the original content, neither too concise nor overly condensed. Use technical terms, explained with clarity and precision, to ensure full understanding, and feel free to draw on examples or explanations where helpful, staying closely aligned with the research study's context. Each paragraph in the generated summary should begin with four asterisks (****). Avoid adding extra introductions or conclusions responses by your side."
            )
        }
    ]

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=prompt,
            model="llama3-8b-8192"
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error creating final summary: {e}")
        return ""


def generate_image_prompts(summarized_content):
    prompt = [
        {
            "role": "user",
            "content": (
                f"Consider yourself an expert in crafting image prompts. This is the content: {summarized_content}, where strings starting with four asterisks indicate a new paragraph. Generate appropriate image prompts for each paragraph in this format: 'Generate an image of ....'. Do not generate the image prompts for exactly what is in the para but, visualize and represent the images with examples. The number of image prompts generated should be strictly equal to number of paras.Each prompt should be in single quotes and separated by a semicolon. The number of image prompts should be equal to number of paragraphs. Do not include any introductory or concluding remarks."
            )
        }
    ]

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=prompt,
            model="llama3-8b-8192"
        )
        prompts_text = chat_completion.choices[0].message.content.strip()
        file_path = os.path.join(output_dir, "image_prompts.txt")
        with open(file_path, 'w') as file:
            file.write(prompts_text)
    except Exception as e:
        print(f"Error generating image prompts: {e}")


def llm_infer(research_content):
    content_chunks = split_content(research_content)
    summarized_chunks = summarize_chunks(content_chunks)
    final_response = final_summary(summarized_chunks)

    # Save summarized content to file
    with open(os.path.join(output_dir, "summ_content.txt"), 'w') as file:
        file.write(final_response)

    # Generate image prompts
    generate_image_prompts(final_response)


with open ("parsed_content.txt", 'r') as file:
    content = file.read()
    llm_infer(content)
    generate_image_prompts(content)
    

file_path = os.path.join(output_dir, "image_prompts.txt")
with open (file_path, 'r') as file:
    content = file.read()
    prompts = re.findall(r"'Generate an image[^']*'", content)

for index, prompt in enumerate(prompts):
    generate_image(prompt, index)


