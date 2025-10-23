# AI Cover Letter Generator

Automate personalized cover letter creation for startup applications using OpenAI's GPT-4.

## Features

- AI-powered cover letter generation
- Customizable tone (professional, enthusiastic, casual)
- CLI interface (command-line and interactive)
- Profile saving for reusable background information
- Automated output file management
- Support for healthcare and AI startup applications

## Tech Stack

- **Python** - Core programming language
- **OpenAI API** - GPT-4 for letter generation
- **CLI** - Command-line interface

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

3. Create necessary directories:
```bash
mkdir -p output profiles templates
```

## Usage

### Interactive Mode (Recommended)

```bash
python interactive.py
```

Follow the prompts to:
1. Enter company and position details
2. Provide company and job descriptions
3. Share your background and experience
4. Select the tone for your letter
5. Save profiles for future use

### Command-Line Mode

```bash
python generator.py \
  --company "HealthTech AI" \
  --position "Product Manager" \
  --company-desc "AI-powered healthcare platform revolutionizing patient care" \
  --job-desc "Looking for PM with healthcare experience, AI knowledge, and strong communication skills" \
  --background "5 years in healthcare tech, launched 2 AI products, MBA from Stanford" \
  --tone professional \
  --output my_cover_letter.txt
```

### Command-Line Options

- `--company`: Company name (required)
- `--position`: Job position (required)
- `--company-desc`: Brief company description (required)
- `--job-desc`: Job requirements and responsibilities (required)
- `--background`: Your relevant experience (required)
- `--tone`: Letter tone - professional, enthusiastic, or casual (default: professional)
- `--output`: Output filename (default: auto-generated)
- `--api-key`: OpenAI API key (optional if set in environment)

## Examples

### Example 1: Product Manager at Healthcare Startup

```bash
python generator.py \
  --company "Vital AI" \
  --position "Senior Product Manager" \
  --company-desc "Series B healthtech startup building AI diagnostic tools for primary care physicians" \
  --job-desc "Seeking PM with 5+ years experience in healthcare software, strong technical background, and proven ability to ship products. Experience with AI/ML products preferred." \
  --background "7 years product management experience, 4 years in healthcare tech. Shipped AI-powered patient triage system at previous company. Strong SQL and data analysis skills. Passionate about improving healthcare access." \
  --tone enthusiastic
```

### Example 2: Using Saved Profile

First time:
```bash
python interactive.py
# Save your background as "healthcare_pm"
```

Future applications:
```bash
python interactive.py
# Enter 'y' when asked about saved profile
# Enter 'healthcare_pm' as profile name
# Only enter company-specific details
```

## Project Structure

```
03-ai-cover-letter/
├── generator.py           # Main generator with CLI
├── interactive.py         # Interactive user interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── README.md             # This file
├── output/               # Generated cover letters (created at runtime)
├── profiles/             # Saved user profiles (created at runtime)
└── templates/            # Letter templates (optional)
```

## Tips for Best Results

1. **Be Specific**: Provide detailed job descriptions and background information
2. **Match Keywords**: Include relevant keywords from the job posting in your background
3. **Show Enthusiasm**: Mention specific things you admire about the company
4. **Quantify**: Include numbers and metrics when describing your experience
5. **Customize**: Review and edit the generated letter before sending

## API Costs

- Uses OpenAI GPT-4 API
- Average cost: $0.03-0.06 per cover letter (depending on length)
- Set `MAX_TOKENS` environment variable to control length and cost

## Customization

### Changing the AI Model

Edit `generator.py` line 64:
```python
model="gpt-4",  # Change to "gpt-3.5-turbo" for lower cost
```

### Adjusting Tone

Modify the system prompt in `generator.py` line 60-62 to customize the writing style.

### Creating Templates

Save JSON templates in `templates/` directory:
```json
{
  "industry": "Healthcare AI",
  "common_requirements": "AI/ML experience, healthcare knowledge, startup mentality"
}
```

## Future Enhancements

- [ ] Support for multiple letter formats (email, traditional, LinkedIn)
- [ ] Integration with job boards to auto-fill job descriptions
- [ ] A/B testing different letter styles
- [ ] Browser extension for one-click generation
- [ ] Analytics on which letters get responses
- [ ] Resume integration and matching
