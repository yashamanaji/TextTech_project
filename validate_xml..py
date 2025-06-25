from lxml import etree
import os

def validate_all_xml(schema_path="RelaxNG Schema/book_schema.rng", xml_dir="xml_output"):
    # Load RelaxNG schema
    schema_doc = etree.parse(schema_path)
    relaxng = etree.RelaxNG(schema_doc)

    # Track validation results
    passed = 0
    failed = 0

    # Validate each XML file
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_dir, filename)
            try:
                xml_doc = etree.parse(file_path)
                if relaxng.validate(xml_doc):
                    print(f"✅ {filename} is valid.")
                    passed += 1
                else:
                    print(f"❌ {filename} is INVALID.")
                    print(relaxng.error_log)
                    failed += 1
            except Exception as e:
                print(f"❌ {filename} could not be parsed: {e}")
                failed += 1

    print("\n🔍 Validation Summary:")
    print(f"✅ Valid files  : {passed}")
    print(f"❌ Invalid files: {failed}")

if __name__ == "__main__":
    validate_all_xml()
