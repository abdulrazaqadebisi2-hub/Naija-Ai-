import os
from flask import Flask, request, render_template_string
from openai import OpenAI

app = Flask(__name__)

# User will put THEIR OWN key in env, not hardcoded
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"), # Set in your hosting
)

SYSTEM_PROMPT = """
You are Naija AI. 
Your creator is Sulaiman Abdul Razaq Adebisi from Kwara State, Ilorin, Gaa Akanbi.
If anyone asks who created you, who built you, who is your owner, say: 
"Sulaiman Abdul Razaq Adebisi from Kwara state built me"
Never say you were made by Meta, Llama, Groq or anyone else.
Speak in friendly Naija style mixed with English.
"""

HTML = """
<html>
<head><title>Naija AI by Sulaiman</title></head>
<body style="font-family: sans-serif; padding: 20px;">
<h2>Naija AI - Built by Sulaiman Abdul Razaq Adebisi, Kwara</h2>

<!-- ADS SECTION - PASTE YOUR CODES HERE -->
<div style="background: #f0f0f0; padding: 10px; margin: 10px 0; text-align: center;">
    <!-- MONETAG DIRECT LINK -->
    <a href="YOUR_MONETAG_DIRECT_LINK" target="_blank">Click to support</a>
    <br><br>
    <!-- HILLTOPADS DIRECT LINK -->
    <a href="YOUR_HILLTOP_DIRECT_LINK" target="_blank">Hot Naija Deals</a>
    
    <!-- MONETAG POPUNDER CODE PASTE HERE -->
    <script>/* paste your Monetag pop code */</script>
    
    <!-- HILLTOPADS IN-PAGE PUSH CODE PASTE HERE -->
    <script>/* paste your Hilltop in-page push code */</script>
</div>

<form method="post">
<input name="q" placeholder="Ask Naija AI..." style="width:80%; padding:10px;">
<button>Ask</button>
</form>

<div style="margin-top:20px; border:1px solid #ddd; padding:10px;">
{{ answer }}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        user_q = request.form.get("q")
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_q}
            ]
        )
        answer = completion.choices[0].message.content
    return render_template_string(HTML, answer=answer)

if __name__ == "__main__":
    app.run()
