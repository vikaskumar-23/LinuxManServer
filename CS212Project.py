#!/usr/bin/env python3
import subprocess
import html
import os
from flask import Flask, request, render_template_string
from markupsafe import Markup

app = Flask(__name__)

# HTML template with enhanced hacker style
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Linux Man Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #0a0a0a;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #00ff00;
            text-align: center;
            text-shadow: 0 0 10px #00ff00;
            margin-bottom: 30px;
            letter-spacing: 2px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .search-container {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        input[type="text"] {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 12px;
            width: 60%;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
            outline: none;
        }
        input[type="text"]:focus {
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.4);
        }
        button {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 12px 20px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            margin-left: 10px;
            transition: all 0.3s;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
            text-transform: uppercase;
        }
        button:hover {
            background-color: #00ff00;
            color: #1e1e1e;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
        }
        .result-container {
            background-color: #1e1e1e;
            border: 1px solid #00ff00;
            padding: 10;
            border-radius: 5px;
            margin-bottom: 40px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }
        .section-heading {
            color: #00ff00;
            border-bottom: 1px solid #00ff00;
            padding-bottom: 5px;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .output-section {
            margin-bottom: 30px;
        }
        .tab-container {
            display: flex;
            margin-bottom: 0;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background-color: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
            transition: all 0.2s;
        }
        .tab:hover {
            background-color: #444;
        }
        .tab.active {
            background-color: #1e1e1e;
            border-bottom: 1px solid #1e1e1e;
            box-shadow: 0 -5px 10px rgba(0, 255, 0, 0.1);
        }
        .content {
            padding: 15px;
            border: 1px solid #00ff00;
            border-top: 2px solid #00ff00;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
            color: #c0c0c0;
        }
        .content pre {
            white-space: pre-wrap;
            margin: 0px;
            padding: 0;
        }
        .content-container {
            margin-bottom: 30px;
        }
        .popular-commands {
            margin-top: 40px;
            margin-bottom: 40px;
            text-align: center;
            padding: 22px;
            border: 1px solid #333;
            background-color: rgba(30, 30, 30, 0.7);
            border-radius: 5px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        }
        .popular-commands h3 {
            margin-top: 0;
            color: #00ff00;
            text-shadow: 0 0 5px #00ff00;
        }
        .command-btn {
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background-color: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 5px rgba(0, 255, 0, 0.2);
            text-decoration: none;
        }
        .command-btn:hover {
            background-color: #00ff00;
            color: #1e1e1e;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.4);
            transform: translateY(-2px);
        }
        .hidden {
            display: none;
        }
        .header-animation {
            font-size: 60px;
            overflow: hidden;
            white-space: nowrap;
            border-right: .15em solid #00ff00;
            animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
            margin: 0 auto;
            text-align: center;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #00ff00; }
        }
        .error {
            color: #ff4242;
            text-align: center;
            font-weight: bold;
        }
        .not-found {
            color: #ffcc00;
            text-align: center;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .terminal-header {
            padding: 5px 10px;
            background-color: #333;
            color: #00ff00;
            border-radius: 5px 5px 0 0;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .terminal-body {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 0 0 5px 5px;
            border: 1px solid #444;
            border-top: none;
        }
        .terminal-btn {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .terminal-btn.red { background-color: #ff5f56; }
        .terminal-btn.yellow { background-color: #ffbd2e; }
        .terminal-btn.green { background-color: #27c93f; }
        .terminal-title {
            flex-grow: 1;
            text-align: center;
        }
        .blinking-cursor {
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            from, to { opacity: 1; }
            50% { opacity: 0; }
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #1e1e1e;
        }
        ::-webkit-scrollbar-thumb {
            background: #333;
            border: 1px solid #00ff00;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #444;
        }
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.1;
        }
    </style>
</head>
<body>
    <canvas id="matrix" class="matrix-bg"></canvas>
    <div class="container">
    <br><br><br>
        <h1 class="header-animation">Linux Man Server</h1>
        <br><br><br>
        <div class="search-container">
            <form action="/" method="get" style="display: flex; width: 100%;">
                <input type="text" name="cmd" placeholder="Enter a Linux command..." value="{{ command }}" autocomplete="off">
                <button type="submit">Execute</button>
            </form>
        </div>
        
        {% if command %}
        <div class="result-container">
            <div class="terminal-header">
                <div>
                    <span class="terminal-btn red"></span>
                    <span class="terminal-btn yellow"></span>
                    <span class="terminal-btn green"></span>    
                </div>
                <div class="terminal-title">{{ command }} - Command Info</div>
                <div></div>
            </div>
            
            <div class="terminal-body">
                <div class="content-container">
                    <div class="tab-container">
                        <div class="tab active" onclick="switchTab('man')">man {{ command }}</div>
                        <div class="tab" onclick="switchTab('tldr')">tldr {{ command }}</div>
                    </div>
                    
                    <div id="man-content" class="content">
                        {% if man_output %}
                        <pre>{{ man_output }}</pre>
                        {% else %}
                        <p class="not-found">Man page not found for '{{ command }}'</p>
                        {% endif %}
                    </div>
                    
                    <div id="tldr-content" class="content hidden">
                        {% if tldr_output %}
                        <pre>{{ tldr_output|safe }}</pre>
                        {% else %}
                        <p class="not-found">TLDR page not found for '{{ command }}'</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
        
        <div class="popular-commands">
            <h3>Popular Commands</h3>
            <div>
                {% for cmd in popular_commands %}
                <a href="/?cmd={{ cmd }}" class="command-btn">{{ cmd }}</a>
                {% endfor %}
            </div>
        </div>
        
        <div class="footer">
            <p>Linux Man Server - Access man pages with style <span class="blinking-cursor">_</span></p>
        </div>
    </div>
    
    <script>
        function switchTab(tab) {
            // Hide all content
            document.getElementById('man-content').classList.add('hidden');
            document.getElementById('tldr-content').classList.add('hidden');
            
            // Show selected content
            document.getElementById(tab + '-content').classList.remove('hidden');
            
            // Update active tab
            var tabs = document.querySelectorAll('.tab');
            tabs.forEach(function(t) {
                t.classList.remove('active');
            });
            
            // Set active tab
            event.target.classList.add('active');
        }
        
        // Matrix rain animation
        document.addEventListener('DOMContentLoaded', function() {
            var canvas = document.getElementById('matrix');
            var ctx = canvas.getContext('2d');
            
            // Set canvas size
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            // Characters to display
            var characters = '01'.split('');
            var fontSize = 12;
            var columns = canvas.width / fontSize;
            
            // Create drops array
            var drops = [];
            for (var i = 0; i < columns; i++) {
                drops[i] = 1;
            }
            
            function draw() {
                // Semi-transparent black background to create trail effect
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#00ff00'; // Matrix green
                ctx.font = fontSize + 'px monospace';
                
                for (var i = 0; i < drops.length; i++) {
                    // Random character
                    var text = characters[Math.floor(Math.random() * characters.length)];
                    
                    // Draw character
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    
                    // Reset drop if it reaches bottom or randomly to create randomness
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    
                    // Increment y coordinate
                    drops[i]++;
                }
            }
            
            setInterval(draw, 33);
            
            // Resize canvas on window resize
            window.addEventListener('resize', function() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                columns = canvas.width / fontSize;
                drops = [];
                for (var i = 0; i < columns; i++) {
                    drops[i] = 1;
                }
            });
        });
    </script>
</body>
</html>
"""

# List of popular commands
POPULAR_COMMANDS = [
    "ls", "grep", "find", "ps", "netstat", 
    "chmod", "chown", "tar", "ssh", "awk",
    "sed", "curl", "wget", "top", "git",
    "ping", "ifconfig", "systemctl", "df", "du"
]

def get_man_page(command):
    """Get the man page for a command."""
    try:
        # Sanitize the command to prevent command injection
        if not is_safe_command(command):
            return "Invalid command requested."
            
        # Run man command and capture output
        result = subprocess.run(
            ["man", command], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            return None
            
        # Format the output
        return html.escape(result.stdout)
    except Exception as e:
        return f"Error retrieving man page: {str(e)}"

def strip_ansi_codes(text):
    """Strip ANSI color codes from text."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def get_tldr_page(command):
    """Get the tldr page for a command."""
    try:
        # Sanitize the command to prevent command injection
        if not is_safe_command(command):
            return "Invalid command requested."
            
        # Check if tldr is installed
        if subprocess.run(["which", "tldr"], capture_output=True).returncode != 0:
            return "TLDR command not installed. Install with 'npm install -g tldr' or your package manager."
            
        # Run tldr command and capture output
        result = subprocess.run(
            ["tldr", command], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            return None
        
        # Strip ANSI color codes and don't escape HTML (will be rendered as Markup)
        cleaned_output = strip_ansi_codes(result.stdout)
        return cleaned_output
    except Exception as e:
        return f"Error retrieving TLDR page: {str(e)}"

def is_safe_command(command):
    """Simple validation to prevent command injection."""
    # Check if command contains only alphanumeric characters, dash, and underscore
    return all(c.isalnum() or c in ['-', '_'] for c in command) and command != ""

@app.route('/')
def index():
    """Main route handler."""
    command = request.args.get('cmd', '')
    
    if command:
        # Ensure command is safe
        if not is_safe_command(command):
            return render_template_string(
                HTML_TEMPLATE,
                command="",
                man_output="Invalid command requested.",
                tldr_output="Invalid command requested.",
                popular_commands=POPULAR_COMMANDS
            )
            
        man_output = get_man_page(command)
        tldr_output = get_tldr_page(command)
    else:
        man_output = None
        tldr_output = None
    
    return render_template_string(
        HTML_TEMPLATE,
        command=command,
        man_output=man_output,
        tldr_output=tldr_output,
        popular_commands=POPULAR_COMMANDS
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Linux Man Server on port {port}...")
    print(f"Open http://localhost:{port} in your browser")
    app.run(host='0.0.0.0', port=port, debug=True)