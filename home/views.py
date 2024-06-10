from django.shortcuts import render, HttpResponse, redirect
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import PyPDF2
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

import os
from django.conf import settings

# Load model and tokenizer
model_name = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
text2text = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=80)

# Extract text from PDF for context
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

pdf_file_path = r'C:\Users\Kanika\OneDrive\Desktop\llm - Copy\hello\static\Sure trust (1).pdf'
context = extract_text_from_pdf(pdf_file_path)

def split_text_into_chunks(text, chunk_size):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def get_bot_response(message):
    question = message
    chunk_size = 450  # Adjust the chunk size based on your needs
    input_texts = split_text_into_chunks(context, chunk_size)

    # Collect responses from each chunk
    responses = []
    for input_text in input_texts:
        input_with_question = f"question: {question} context: {input_text}"
        outputs = text2text(input_with_question)
        if outputs:
            responses.append(outputs[0]['generated_text'])
    
    # Combine responses if necessary
    combined_response = " ".join(responses)
    return combined_response if combined_response else "Sorry, I couldn't understand your question."

def registration(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        Course = request.POST["Course"]

        # Define the path to the text file in the templates folder
        directory = os.path.join(settings.BASE_DIR, 'home', 'templates')
        file_path = os.path.join(directory, 'registration.txt')

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            # Write the registration data to the text file
            with open(file_path, 'a') as file:
                file.write(f"Name: {name}, Email: {email}, Mobile Number: {mobile}, Course: {Course}\n")
            print(f"Successfully wrote to {file_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")
            return HttpResponse(f"Error: {e}")

        return redirect('home')  # Redirect to the same page or another page after registration

    return render(request, 'registration.html')

@csrf_exempt
def submit_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('input')
        bot_response = get_bot_response(user_message)
        return JsonResponse({'response': bot_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    context = {"variable1": "kanika is great"}
    return render(request, "index4.html", context)

def service(request):
    return HttpResponse("this is service page")

def about(request):
    return HttpResponse("this is about page")






