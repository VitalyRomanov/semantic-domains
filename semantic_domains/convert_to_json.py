import argparse

from semantic_domains.rwc_parser import convert_rwc_domains_to_json


def main(args):
    convert_rwc_domains_to_json(args.domains_doc, args.domains_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains_doc", help="Path to the domains document docx file")
    parser.add_argument("domains_json", help="Path to the output domains json file")
    args = parser.parse_args()

    main(args)
