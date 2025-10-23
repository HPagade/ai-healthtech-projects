"""
AI Cover Letter Generator
Automates personalized cover letter creation for startup applications
"""

import os
import json
from openai import OpenAI
from pathlib import Path


class CoverLetterGenerator:
    """Generate personalized cover letters using OpenAI API"""

    def __init__(self, api_key=None):
        """
        Initialize the generator

        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY environment variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = OpenAI(api_key=self.api_key)

    def generate_cover_letter(
        self,
        company_name,
        position,
        company_description,
        job_description,
        user_background,
        tone="professional",
        max_tokens=800
    ):
        """
        Generate a cover letter

        Args:
            company_name: Name of the company
            position: Job position title
            company_description: Brief description of the company
            job_description: Key requirements and responsibilities
            user_background: User's relevant experience and skills
            tone: Tone of the letter (professional, enthusiastic, casual)
            max_tokens: Maximum length of generated letter

        Returns:
            Generated cover letter text
        """
        prompt = self._build_prompt(
            company_name=company_name,
            position=position,
            company_description=company_description,
            job_description=job_description,
            user_background=user_background,
            tone=tone
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career coach and professional writer specializing in creating compelling cover letters for startup positions in the healthcare and AI sectors."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )

            cover_letter = response.choices[0].message.content
            return cover_letter

        except Exception as e:
            raise Exception(f"Error generating cover letter: {e}")

    def _build_prompt(
        self,
        company_name,
        position,
        company_description,
        job_description,
        user_background,
        tone
    ):
        """Build the prompt for OpenAI API"""
        prompt = f"""
Generate a compelling cover letter for the following job application:

**Company:** {company_name}
**Position:** {position}

**Company Description:**
{company_description}

**Job Description:**
{job_description}

**Candidate Background:**
{user_background}

**Instructions:**
- Write a {tone} and engaging cover letter
- Highlight specific skills and experiences that match the job requirements
- Show genuine enthusiasm for the company's mission
- Keep it concise (3-4 paragraphs)
- Include specific examples where possible
- Demonstrate knowledge of the company and industry
- End with a strong call to action

Format the cover letter with proper business letter structure but without addresses (start directly with the greeting).
"""
        return prompt

    def save_cover_letter(self, content, filename):
        """Save cover letter to a file"""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(content)

        print(f"Cover letter saved to: {filepath}")
        return filepath

    def load_template(self, template_name="default"):
        """Load a cover letter template"""
        template_dir = Path("templates")
        template_file = template_dir / f"{template_name}.json"

        if template_file.exists():
            with open(template_file, 'r') as f:
                return json.load(f)
        return None


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate AI-powered cover letters")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--position", required=True, help="Job position")
    parser.add_argument("--company-desc", required=True, help="Company description")
    parser.add_argument("--job-desc", required=True, help="Job description/requirements")
    parser.add_argument("--background", required=True, help="Your background and experience")
    parser.add_argument("--tone", default="professional", choices=["professional", "enthusiastic", "casual"], help="Tone of the letter")
    parser.add_argument("--output", default=None, help="Output filename (default: auto-generated)")
    parser.add_argument("--api-key", default=None, help="OpenAI API key (or set OPENAI_API_KEY env var)")

    args = parser.parse_args()

    # Initialize generator
    try:
        generator = CoverLetterGenerator(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Generate cover letter
    print(f"Generating cover letter for {args.position} at {args.company}...")

    try:
        cover_letter = generator.generate_cover_letter(
            company_name=args.company,
            position=args.position,
            company_description=args.company_desc,
            job_description=args.job_desc,
            user_background=args.background,
            tone=args.tone
        )

        # Display cover letter
        print("\n" + "=" * 80)
        print(cover_letter)
        print("=" * 80 + "\n")

        # Save to file
        if args.output:
            filename = args.output
        else:
            safe_company = args.company.replace(" ", "_")
            safe_position = args.position.replace(" ", "_")
            filename = f"{safe_company}_{safe_position}_cover_letter.txt"

        generator.save_cover_letter(cover_letter, filename)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
