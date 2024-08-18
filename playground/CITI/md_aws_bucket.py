#md_aws_bucket.py
import markdown
import subprocess
import pyperclip

class MarkdownS3Processor:
    def __init__(self, md_source="clipboard", bucket_name="sean-site-bucket"):
        """Initialize the processor with the markdown source and S3 bucket name."""
        self.md_source = md_source
        self.bucket_name = bucket_name
        self.html_file_path = "index.html"

    def convert_md_to_html(self, md_content):
        """Convert Markdown content to an HTML file."""
        try:
            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content)

            # Save the HTML to a file with basic styling for code blocks
            with open(self.html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write("""
                <!DOCTYPE html>
                <html lang='en'>
                <head>
                    <meta charset='UTF-8'>
                    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                    <title>My AWS S3 Website</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; }
                        pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
                        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
                    </style>
                </head>
                <body>
                """)
                html_file.write(html_content)
                html_file.write("</body></html>")

            print(f"Successfully generated {self.html_file_path} from Markdown content")
            return True

        except Exception as e:
            print(f"Error converting Markdown to HTML: {e}")
            return False

    def upload_html_to_s3(self):
        """Upload the HTML file to the specified S3 bucket."""
        try:
            # Run the AWS CLI command to upload the file
            command = f"aws s3 cp {self.html_file_path} s3://{self.bucket_name}/index.html"
            subprocess.run(command, check=True, shell=True)
            print(f"Successfully uploaded {self.html_file_path} to s3://{self.bucket_name}/index.html")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error uploading file to S3: {e}")
            return False
        
    def test_proess_clipboard(self):
        md_content = ""
        if self.md_source.lower() == "clipboard":
            try:
                md_content = pyperclip.paste()
                if not md_content.strip():
                    raise ValueError("No content found in clipboard.")
                print("Markdown content read from clipboard.")
                print(md_content)
            except Exception as e:
                print(f"Error reading from clipboard: {e}")
                return False
        # Convert the Markdown content to HTML
        if not self.convert_md_to_html(md_content):
            return False

        # Upload the HTML file to the specified S3 bucket
        if not self.upload_html_to_s3():
            return False

        return True


    def process(self):
        """Process the conversion and upload."""
        # Read Markdown content
        if self.md_source.lower() == "clipboard":
            try:
                md_content = pyperclip.paste()
                if not md_content.strip():
                    raise ValueError("No content found in clipboard.")
                print("Markdown content read from clipboard.")
            except Exception as e:
                print(f"Error reading from clipboard: {e}")
                return False
        else:
            try:
                with open(self.md_source, 'r', encoding='utf-8') as md_file:
                    md_content = md_file.read()
                print(f"Markdown content read from file: {self.md_source}")
            except Exception as e:
                print(f"Error reading Markdown file: {e}")
                return False

        # Convert the Markdown content to HTML
        if not self.convert_md_to_html(md_content):
            return False

        # Upload the HTML file to the specified S3 bucket
        if not self.upload_html_to_s3():
            return False

        return True

def main():
    process = MarkdownS3Processor()
    process.test_proess_clipboard()

if __name__ == "__main__":
    # Check for correct usage
    main()