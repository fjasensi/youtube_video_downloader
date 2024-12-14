# Youtube video downloader

A command-line tool to download and organize YouTube videos efficiently. The project is designed to allow users to specify download paths and categories, making it easier to manage video collections.

---

## Features
- Download YouTube videos directly from the command line.
- Customizable download paths for different categories (e.g., Science, Technology, Math).
- Easy-to-setup configuration using YAML.
- Lightweight and flexible with a Python virtual environment.

---

## Setup (first time only)
### Python Virtual Environment
Before running the project, set up a Python virtual environment to manage dependencies:
```bash
# Create a virtual environment (if not already created)
python3 -m venv ~/.virtualenvs/pyYt

# Activate the virtual environment
source ~/.virtualenvs/pyYt/bin/activate

# Install dependencies
pip install -r requirements.txt
```


### Add alias
To simplify running the tool, create a custom alias in your .bashrc file:

Open your .bashrc file
```bash
nano ~/.bashrc
```

Adding the following alias:
```bash
# pyYt
pyyt() {
  source /home/username/.virtualenvs/pyYt/bin/activate
  python3 /home/username/repos/pyYt/main.py "$@"
  deactivate
}
```

Reload the ,bashrc file,
```
source ~/.bashrc
```

Now, you can run the tool by simply typing pyyt in your terminal.

---

## Config
### Overview
The tool uses a YAML configuration file to define:
- The base download directory.
- Subdirectories for organizing videos into categories like Science, Technology, Math, etc.

### Default Configuration
The configuration file is located at config/config.yaml. Below is an example of the default structure:

```yaml
general:
  downloads: /mnt/f/PyYt

paths:
  sci: science
  tech: technology
  math: maths
  bd: big_data
  df: default

```

### Customizing the Configuration
1. Go to the configuration file
2. Modify the downloads path to set the base directory where videos will be saved.
3. Update the paths section to add or rename categories as needed.

### Behavior
- When a video is downloaded, it will be saved in the corresponding subdirectory under general.downloads.
- If a subdirectory does not exist, the program will automatically create it.

## Usage
### Downloading Videos
Once the alias is set up and the configuration is complete, you can start downloading videos:
```bash
pyyt <YouTube URL> [<category>]
```

Example
```bash
pyyt https://www.youtube.com/watch?v=example123
```
```bash
pyyt "https://www.youtube.com/watch?v=example123" sci
```

## Command-Line Optins
- url: Specify youtube video url
- category: Specify the category to save the video. If omitted, the default category is used.
- help: Display available options and usage.

## Dependencies
The project uses the following Python libraries:
- yt_dlp: For downloading YouTube videos.
- pyyaml: For handling YAML configuration files.

## Important
To download in maximum quality you need ffmpeg installed in your system.