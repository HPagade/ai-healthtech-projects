"""
Interactive Cover Letter Generator
User-friendly interactive CLI for generating cover letters
"""

from generator import CoverLetterGenerator
from pathlib import Path
import json


def print_header():
    """Print welcome header"""
    print("\n" + "=" * 80)
    print(" " * 25 + "AI COVER LETTER GENERATOR")
    print("=" * 80 + "\n")


def get_user_input():
    """Collect user input interactively"""
    print("Let's create your personalized cover letter!\n")

    company = input("Company name: ").strip()
    position = input("Job position: ").strip()

    print("\nCompany description (press Enter twice when done):")
    company_desc_lines = []
    while True:
        line = input()
        if line == "":
            break
        company_desc_lines.append(line)
    company_desc = " ".join(company_desc_lines)

    print("\nJob description/key requirements (press Enter twice when done):")
    job_desc_lines = []
    while True:
        line = input()
        if line == "":
            break
        job_desc_lines.append(line)
    job_desc = " ".join(job_desc_lines)

    print("\nYour relevant background and experience (press Enter twice when done):")
    background_lines = []
    while True:
        line = input()
        if line == "":
            break
        background_lines.append(line)
    background = " ".join(background_lines)

    print("\nSelect tone:")
    print("1. Professional (default)")
    print("2. Enthusiastic")
    print("3. Casual")
    tone_choice = input("Choice (1-3): ").strip() or "1"

    tone_map = {
        "1": "professional",
        "2": "enthusiastic",
        "3": "casual"
    }
    tone = tone_map.get(tone_choice, "professional")

    return {
        'company': company,
        'position': position,
        'company_desc': company_desc,
        'job_desc': job_desc,
        'background': background,
        'tone': tone
    }


def save_profile(data, profile_name):
    """Save user profile for reuse"""
    profile_dir = Path("profiles")
    profile_dir.mkdir(exist_ok=True)

    profile_file = profile_dir / f"{profile_name}.json"

    # Only save background, not company-specific data
    profile_data = {
        'background': data['background']
    }

    with open(profile_file, 'w') as f:
        json.dump(profile_data, f, indent=2)

    print(f"\nProfile saved to: {profile_file}")


def load_profile(profile_name):
    """Load saved user profile"""
    profile_dir = Path("profiles")
    profile_file = profile_dir / f"{profile_name}.json"

    if profile_file.exists():
        with open(profile_file, 'r') as f:
            return json.load(f)
    return None


def main():
    """Main interactive interface"""
    print_header()

    # Check for saved profile
    use_profile = input("Do you have a saved profile? (y/n): ").strip().lower()

    background = None
    if use_profile == 'y':
        profile_name = input("Profile name: ").strip()
        profile = load_profile(profile_name)
        if profile:
            background = profile.get('background')
            print(f"Loaded profile: {profile_name}")
        else:
            print("Profile not found. Continuing without saved profile.")

    # Collect input
    data = get_user_input()

    # Use saved background if available
    if background and not data['background']:
        data['background'] = background

    # Initialize generator
    try:
        generator = CoverLetterGenerator()
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return

    # Generate cover letter
    print("\n" + "-" * 80)
    print("Generating your cover letter... This may take a moment.")
    print("-" * 80 + "\n")

    try:
        cover_letter = generator.generate_cover_letter(
            company_name=data['company'],
            position=data['position'],
            company_description=data['company_desc'],
            job_description=data['job_desc'],
            user_background=data['background'],
            tone=data['tone']
        )

        # Display result
        print("\n" + "=" * 80)
        print("GENERATED COVER LETTER")
        print("=" * 80 + "\n")
        print(cover_letter)
        print("\n" + "=" * 80 + "\n")

        # Save to file
        safe_company = data['company'].replace(" ", "_")
        safe_position = data['position'].replace(" ", "_")
        filename = f"{safe_company}_{safe_position}_cover_letter.txt"

        generator.save_cover_letter(cover_letter, filename)

        # Offer to save profile
        if use_profile != 'y':
            save_prof = input("\nWould you like to save your background as a profile for future use? (y/n): ").strip().lower()
            if save_prof == 'y':
                prof_name = input("Profile name: ").strip()
                save_profile(data, prof_name)

        print("\nThank you for using AI Cover Letter Generator!")

    except Exception as e:
        print(f"\nError generating cover letter: {e}")


if __name__ == "__main__":
    main()
