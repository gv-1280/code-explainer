# CodeMorph – AI-Powered Code Explainer & Converter

![CodeMorph Image]("https://github.com/user-attachments/assets/63e988aa-1997-46a3-ac03-589710b08817" />)

## 🚀 Overview

CodeMorph is a powerful web-based application that helps developers, students, and educators understand and manipulate code efficiently. It leverages AI to provide two core functionalities:

- **🔍 Code Explanation** – Converts programming code into plain language explanations
- **🔄 Code Conversion** – Translates code between multiple programming languages

## ✨ Features

- **Real-time code explanation** in plain language
- **Multi-language code conversion** (Python ↔ Java ↔ C++ ↔ JavaScript and more)
- **Interactive frontend** with intuitive input/output interface
- **Modular backend API** architecture for efficient request handling
- **AI model fallback routing** for consistent performance
- **Docker containerization** for easy deployment and reproducibility

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **AI Models**: OpenRouter API (DeepSeek Coder 6.7B Instruct)
- **Containerization**: Docker
- **Environment Management**: Python dotenv

## 📋 Prerequisites

Before running CodeMorph locally, ensure you have:

- **Python 3.8+** installed
- **Docker** (optional, for containerized deployment)
- **OpenRouter API Key** (sign up at [OpenRouter](https://openrouter.ai/))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/gv-1280/codemorph.git
cd codemorph
```

### 2. Set Up Environment

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root directory:

```bash
touch .env
```

Add your OpenRouter API key to the `.env` file:

```
API_KEY=your_api_key_here
```

> **⚠️ Important**: Replace `your_api_key_here` with your actual OpenRouter API key. You can get one from [OpenRouter](https://openrouter.ai/).

### 4. Run the Application

#### Option A: Run with Python (Recommended for Development)

1. **Start the FastAPI backend**:
```bash
uvicorn backend.server:app --reload --port 8000
```

2. **In a new terminal, start the Streamlit frontend**:
```bash
streamlit run app.py
```

The application will be available at:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000

## 🎯 Usage

1. **Open the application** in your browser at `http://localhost:8501`
2. **Choose your action**: Code Explanation or Code Conversion
3. **Input your code** in the text area
4. **Select source/target languages** (for conversion)
5. **Click the explain button** to get results
6. **View the output** in real-time

## 🔧 API Endpoints

The FastAPI backend provides the following endpoints:

- `POST /explain` - Explains code in plain language
- `POST /convert` - Converts code between programming languages
- `GET /health` - Health check endpoint

## 🐳 Docker Support

CodeMorph comes with full Docker support for easy containerization:

```bash
# Build image
docker build -t codemorph .

# Run container
docker run -p 8501:8501 -p 8000:8000 --env-file .env codemorph

# Run with docker-compose (if available)
docker-compose up
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Issue**: "Module not found" error
- **Solution**: Ensure you've activated your virtual environment and installed all dependencies

**Issue**: API key not working
- **Solution**: Double-check your `.env` file format and ensure the API key is valid

**Issue**: Port already in use
- **Solution**: Kill existing processes or change ports in the run commands

**Issue**: Docker container won't start
- **Solution**: Ensure Docker is running and the `.env` file exists

### Getting Help

If you encounter any issues:
1. Check the [Issues](https://github.com/gv-1280/codemorph/issues) page
2. Create a new issue with detailed error information
3. Include your system information and steps to reproduce

## 🙏 Acknowledgments

- Built with AI assistance from GitHub Copilot
- Powered by OpenRouter API and DeepSeek Coder models
- Thanks to the open-source community for the amazing tools and libraries

---

**⭐ If you find CodeMorph helpful, please consider giving it a star!**