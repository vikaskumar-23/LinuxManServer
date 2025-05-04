
# Linux Man Server

A web-based Linux manual page viewer with hacker-style interface.

## Features

- View `man` pages in your browser
- See simplified `tldr` examples
- Quick access to common commands
- Terminal-style design with animations

## Installation

1. **Install dependencies**:
   ```bash
   sudo apt install man-db groff-base npm
   sudo npm install -g tldr
   tldr --update
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/yourusername/linux-man-server.git
   cd linux-man-server
   python3 -m venv venv
   source venv/bin/activate
   pip install flask
   ```

## Usage

**Start the server**:
```bash
python3 app.py
```

Access in your browser at:  
`http://localhost:5000`

**Search for commands**:
1. Type a command in the search box (e.g. `ls`)
2. Switch between tabs:
   - **man**: Full manual page
   - **tldr**: Practical examples

