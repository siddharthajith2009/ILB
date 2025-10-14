# AI Explanations Setup Guide

## Overview
Your JobScope application now includes AI-powered explanations for job predictions! This feature uses OpenAI's GPT-4o Mini model to provide detailed explanations of why a prediction was made.

## Setup Instructions

### 1. Get Your OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (starts with `sk-`)

### 2. Set Environment Variable

#### Option A: Terminal (Temporary)
```bash
export OPENAI_API_KEY="your-api-key-here"
python3 app.py
```

#### Option B: Permanent Setup
Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Then restart your terminal or run:
```bash
source ~/.zshrc
```

### 3. Restart Flask Server
After setting the environment variable:
```bash
python3 app.py
```

## Features

### 🤖 AI Explanation Section
- **Location**: Results page, after probability breakdown
- **Content**: Detailed explanation of why the prediction was made
- **Style**: Matches your existing design with aqua glow effects
- **Animation**: Smooth fade-in with loading spinner

### 📊 What Gets Explained
- Current market trends for the specific role
- Impact of education level on job demand
- How experience level affects prospects
- Industry and economic factors
- Technological influences

### 🎨 Visual Design
- Consistent with your JobScope theme
- Animated loading spinner during generation
- Professional typography and spacing
- Error handling with user-friendly messages

## Testing

1. Make a prediction on your website
2. Go to results page
3. Wait for the AI explanation to generate
4. Read the detailed explanation

## Troubleshooting

### "AI explanations are currently unavailable"
- Make sure OPENAI_API_KEY is set correctly
- Restart the Flask server after setting the variable
- Check that your API key is valid

### "Failed to generate explanation"
- Check your internet connection
- Verify your OpenAI account has credits
- Check the server logs for detailed error messages

## Cost Information
- Uses GPT-4o Mini model (very cost-effective)
- Approximately $0.0015 per 1K tokens
- Each explanation uses roughly 500 tokens
- Cost per explanation: ~$0.00075

## Security Notes
- API key is stored as environment variable (secure)
- No API key is stored in code or committed to repository
- Explanations are generated server-side
