# step3_generate_report.py - HTML report generate karo

import json
from datetime import datetime

print("📊 Report generate kar rahe hain...\n")

# Results load karo
with open("results.json", "r") as f:
    data = json.load(f)

overall = data['overall_accuracy']
results = data['results']

# HTML report create karo
html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Answer Evaluation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }}
        .timestamp {{
            text-align: center;
            color: #999;
            margin-bottom: 30px;
        }}
        .score-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            margin: 30px 0;
        }}
        .big-number {{
            font-size: 5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .question {{
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
            border-radius: 5px;
        }}
        .progress-bar {{
            width: 100%;
            height: 15px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }}
        .interpretation {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 20px;
            margin: 30px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Answer Evaluation Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}</div>
        
        <div class="score-box">
            <h2>Overall Accuracy Score</h2>
            <div class="big-number">{overall:.1f}%</div>
            <p>Based on {len(results)} evaluated questions</p>
        </div>
        
        <div class="interpretation">
            <h3>📝 Interpretation</h3>
            <p>"""

if overall >= 90:
    html += "🌟 Excellent! Outstanding understanding of the material."
elif overall >= 80:
    html += "✅ Very Good! Strong comprehension with minor gaps."
elif overall >= 70:
    html += "👍 Good! Adequate understanding, some areas need review."
elif overall >= 60:
    html += "⚠️ Fair. Basic understanding, significant review needed."
else:
    html += "📚 Needs Work. Major concepts need revision."

html += """</p>
        </div>
        
        <h2>Results by Question</h2>
"""

for r in results:
    acc = r['accuracy']
    color = "#4caf50" if acc >= 80 else "#ff9800" if acc >= 60 else "#f44336"
    
    html += f"""
        <div class="question">
            <h3>Question {r['question']}: {acc:.1f}%</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {acc}%; background: {color};"></div>
            </div>
        </div>
"""

html += """
    </div>
</body>
</html>
"""

# Save HTML
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML report generated: report.html")
print("\n🌐 Ab browser mein report.html open karo!\n")
