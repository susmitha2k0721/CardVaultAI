import re


def extract_email(text):

    import re

    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )

    return emails[0] if emails else ""


def extract_phone(text):

    phones = re.findall(
        r'(\+?\d[\d\-\s]{8,}\d)',
        text
    )

    return phones[0] if phones else ""


def extract_website(text):

    import re

    websites = re.findall(
        r'(www\.[A-Za-z0-9.-]+\.[A-Za-z]{2,})',
        text
    )

    return websites[0] if websites else ""


def extract_name(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines:

        if (
            len(line.split()) >= 2
            and not any(char.isdigit() for char in line)
            and "@" not in line
            and "www" not in line.lower()
            and len(line) < 40
        ):
            return line

    return ""


def extract_designation(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    keywords = [
        "designer",
        "developer",
        "engineer",
        "manager",
        "director",
        "ceo",
        "founder",
        "analyst",
        "consultant",
        "architect",
        "lead"
    ]

    for line in lines:

        for keyword in keywords:

            if keyword.lower() in line.lower():
                return line

    return ""
def extract_company(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    company_parts = []

    keywords = [
        "Real Estate",
        "Technologies",
        "Solutions",
        "Company",
        "& Co",
        "& Co."
    ]

    for line in lines:

        for keyword in keywords:

            if keyword.lower() in line.lower():

                cleaned = line.replace("@", "")
                cleaned = cleaned.replace('"', "")

                if "www." in cleaned:
                    cleaned = cleaned.split("www.")[-1]

                if "@" in cleaned:
                    continue

                company_parts.append(cleaned.strip())

    return " ".join(company_parts)
def extract_address(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    address = []

    for line in lines:

        if (
            ("St" in line or "Street" in line or "Road" in line or "City" in line)
            and "@" not in line
            and "www" not in line.lower()
        ):
            address.append(line)

    return " ".join(address)