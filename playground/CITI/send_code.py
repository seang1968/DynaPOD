import subprocess
import pyperclip

class CodeS3Processor:
    def __init__(self, code_source="clipboard", bucket_name="sean-site-bucket"):
        """Initialize the processor with the code source and S3 bucket name."""
        self.code_source = code_source
        self.bucket_name = bucket_name
        self.html_file_path = "index.html"

    def convert_code_to_html(self, code_content):
        """Convert code content to an HTML file."""
        try:
            # Basic HTML template with styling for code blocks
            html_content = f"""
            <!DOCTYPE html>
            <html lang='en'>
            <head>
                <meta charset='UTF-8'>
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <title>Code Snippet</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    pre {{ background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; border-radius: 5px; overflow-x: auto; }}
                    code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                </style>
            </head>
            <body>
            <pre><code>{code_content}</code></pre>
            </body></html>
            """

            # Save the HTML to a file
            with open(self.html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            print(f"Successfully generated {self.html_file_path} from code content")
            return True

        except Exception as e:
            print(f"Error converting code to HTML: {e}")
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

    def process_clipboard(self):
        code_content = ""
        if self.code_source.lower() == "clipboard":
            try:
                code_content = pyperclip.paste()
                if not code_content.strip():
                    raise ValueError("No content found in clipboard.")
                print("Code content read from clipboard.")
                print(code_content)
            except Exception as e:
                print(f"Error reading from clipboard: {e}")
                return False
        # Convert the code content to HTML
        if not self.convert_code_to_html(code_content):
            return False

        # Upload the HTML file to the specified S3 bucket
        if not self.upload_html_to_s3():
            return False

        return True

def main():
    process = CodeS3Processor()
    process.process_clipboard()

if __name__ == "__main__":
    main()
