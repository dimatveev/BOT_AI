import os
import re
import subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..config import LATEX_OUTPUT_DIR, TEMPLATE_DIR

def escape_tex(value):
    """Escape special LaTeX characters."""
    if not isinstance(value, str):
        return value
    
    tex_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    pattern = '|'.join(re.escape(key) for key in tex_chars.keys())
    return re.sub(pattern, lambda m: tex_chars[m.group()], value)

class LaTeXCompiler:
    def __init__(self):
        # Get the absolute path to the base directory
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Get absolute paths for templates and output
        self.template_dir = os.path.join(self.base_dir, TEMPLATE_DIR)
        self.output_dir = os.path.join(self.base_dir, LATEX_OUTPUT_DIR)
        
        # Create directories if they don't exist
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Print debug information
        print(f"Template directory: {self.template_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Template files: {os.listdir(self.template_dir)}")
        
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['tex', 'latex']),
            block_start_string='{% ',  # Add space after {%
            block_end_string=' %}',    # Add space before %}
            variable_start_string='{{ ',  # Add space after {{
            variable_end_string=' }}',    # Add space before }}
            comment_start_string='{# ',   # Add space after {#
            comment_end_string=' #}',     # Add space before #}
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['e'] = escape_tex
        
        try:
            self.template = self.env.get_template('cv_template.tex.j2')
            print("Template loaded successfully")
        except Exception as e:
            print(f"Error loading template: {str(e)}")
            raise
    
    def _prepare_data(self, data: dict) -> dict:
        """Prepare data for the template."""
        # Convert comma-separated strings to lists if they're not already lists
        if isinstance(data.get('skills'), str):
            data['skills'] = [s.strip() for s in data['skills'].split(',')]
        if isinstance(data.get('languages'), str):
            data['languages'] = [l.strip() for l in data['languages'].split(',')]
            
        # Ensure all dictionary values are strings or have default values
        data = {k: str(v) if v is not None else '' for k, v in data.items()}
        
        # Ensure nested dictionaries exist
        if 'education' not in data:
            data['education'] = {}
        if 'experience' not in data:
            data['experience'] = {}
            
        # Ensure all nested dictionary values are strings
        for key in ['education', 'experience']:
            if isinstance(data[key], dict):
                data[key] = {k: str(v) if v is not None else '' for k, v in data[key].items()}
            
        return data
    
    async def generate_pdf(self, data: dict, user_id: int) -> str:
        """Generate PDF from the template using the provided data."""
        data = self._prepare_data(data)
        
        # Create user directory with absolute path
        user_dir = os.path.join(self.output_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # Generate LaTeX file
        tex_path = os.path.join(user_dir, 'resume.tex')
        pdf_path = os.path.join(user_dir, 'resume.pdf')
        
        try:
            # Render template
            tex_content = self.template.render(**data)
            
            # Write LaTeX file
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(tex_content)
            
            print(f"Generated LaTeX file at: {tex_path}")
            
            # Compile LaTeX to PDF
            for i in range(2):
                process = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', user_dir, tex_path],
                    cwd=user_dir,
                    capture_output=True,
                    text=True
                )
                
                if process.returncode != 0:
                    error_log = ""
                    log_file = os.path.join(user_dir, 'resume.log')
                    if os.path.exists(log_file):
                        with open(log_file, 'r', encoding='utf-8') as f:
                            error_log = f.read()
                    
                    print(f"LaTeX compilation failed (attempt {i+1}):")
                    print(f"Return code: {process.returncode}")
                    print(f"STDOUT:\n{process.stdout}")
                    print(f"STDERR:\n{process.stderr}")
                    print(f"LOG:\n{error_log}")
                    
                    raise Exception(f"LaTeX compilation failed:\nSTDERR: {process.stderr}\nLOG: {error_log}")
            
            if not os.path.exists(pdf_path):
                raise Exception("PDF file was not created")
            
            print(f"Generated PDF file at: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"Error during PDF generation: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")
        
    def cleanup(self, user_id: int):
        """Clean up temporary files."""
        user_dir = os.path.join(self.output_dir, str(user_id))
        if os.path.exists(user_dir):
            for file in os.listdir(user_dir):
                if not file.endswith('.pdf'):
                    os.remove(os.path.join(user_dir, file)) 