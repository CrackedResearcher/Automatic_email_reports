import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted


if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(sys.argv[0])


env_path = os.path.join(basedir, '.env')

load_dotenv(env_path)


def flag_and_summarize_email(data, sender):
    try:
        genai.configure(api_key=os.environ['API_KEY'])
        model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  system_instruction="You are an email assistant. Your tasks are to summarize email content and filter emails into the following categories: spam, important/alerts, social, work-related, personal/family, and newsletters/promotions. Your output should include:\n\nSummary: Provide a very brief summary of the email content, similar to a personal assistant, e.g., \"This email is about [topic].\"\nFiltered as: Categorize the email into one of the predefined categories, strictly adhering to the given filters.\nCategories and Examples:\n\nSpam (emails pitching services, asking to get on a quick call)\n\nImportant/Alerts (signup, login alerts/codes, bank alerts)\n\nSocial (emails from social media companies)\n\nWork-related:\n\n\"Reminder for our project status meeting scheduled for Monday at 10 AM.\"\n\"Attached is the latest report on our market analysis. Please review and provide feedback.\"\n\nPersonal/Family:\n\n\"Hey John, let's meet for lunch this weekend. There's a new restaurant downtown.\"\n\"Dear Sarah, I got a promotion! Let's celebrate with a family dinner next weekend.\"\n\nNewsletters/Promotions (grouping both):\n\n\"Thank you for subscribing to our newsletter. This week's edition covers the latest trends in technology.\"\n\"Our Flash Sale is live. Get 70% off on selected items for the next 48 hours.\"",
)
        response = model.generate_content(f"heres the email: {data}")
    
    
    except ResourceExhausted:
        genai.configure(api_key=os.environ['optional_api_key'])
        new_model = genai.GenerativeModel(model_name="gemini-1.5-flash",
  system_instruction="You are an email assistant. Your tasks are to summarize email content and filter emails into the following categories: spam, important/alerts, social, work-related, personal/family, and newsletters/promotions. Your output should include:\n\nSummary: Provide a very brief summary of the email content, similar to a personal assistant, e.g., \"This email is about [topic].\"\nFiltered as: Categorize the email into one of the predefined categories, strictly adhering to the given filters.\nCategories and Examples:\n\nSpam (emails pitching services, asking to get on a quick call)\n\nImportant/Alerts (signup, login alerts/codes, bank alerts)\n\nSocial (emails from social media companies)\n\nWork-related:\n\n\"Reminder for our project status meeting scheduled for Monday at 10 AM.\"\n\"Attached is the latest report on our market analysis. Please review and provide feedback.\"\n\nPersonal/Family:\n\n\"Hey John, let's meet for lunch this weekend. There's a new restaurant downtown.\"\n\"Dear Sarah, I got a promotion! Let's celebrate with a family dinner next weekend.\"\n\nNewsletters/Promotions (grouping both):\n\n\"Thank you for subscribing to our newsletter. This week's edition covers the latest trends in technology.\"\n\"Our Flash Sale is live. Get 70% off on selected items for the next 48 hours.\"",
)
        response = new_model.generate_content(f"heres the email: {data}")
 


    response_text = response.text.strip()
    summary_start = response.text.find("Summary:") + len("Summary:")
    filtered_start = response_text.find("Filtered as:") + len("Filtered as:")
    summary = response_text[summary_start:response_text.find("\n", summary_start)].strip()
    category = response_text[filtered_start:].strip()

    return (category,  f"<br>from: {sender}<br><br>"+summary+ "<hr>")

    
