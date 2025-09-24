"""
👋 Welcome to your Smithery project!
To run your server, use "uv run dev"
To test interactively, use "uv run playground"

You might find this resources useful:

🧑‍💻 MCP's Python SDK (helps you define your server)
https://github.com/modelcontextprotocol/python-sdk

⚠️ WARNING: This is a vulnerable MCP server for educational purposes only!
DO NOT use in production environments!
"""

import os
import subprocess
import sqlite3
import json
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from smithery.decorators import smithery


# Optional: If you want to receive session-level config from user, define it here
class ConfigSchema(BaseModel):
    # access_token: str = Field(..., description="Your access token for authentication")
    pirate_mode: bool = Field(False, description="Speak like a pirate")


# For servers with configuration:
@smithery.server(config_schema=ConfigSchema)
# For servers without configuration, simply use:
# @smithery.server()
def create_server():
    """Create and configure the MCP server."""

    # Create your FastMCP server as usual
    server = FastMCP("Vulnerable MCP Server (Educational)")

    # Original hello tool
    @server.tool()
    def hello(name: str, ctx: Context) -> str:
        """Say hello to someone."""
        # Access session-specific config through context
        session_config = ctx.session_config

        # In real apps, use token for API requests:
        # requests.get(url, headers={"Authorization": f"Bearer {session_config.access_token}"})
        # if not session_config.access_token:
        #     return "Error: Access token required"

        # Create greeting based on pirate mode
        if session_config.pirate_mode:
            return f"Ahoy, {name}!"
        else:
            return f"Hello, {name}!"

    # 🚨 VULNERABILITY 1: Command Injection
    @server.tool()
    def execute_system_command(command: str) -> str:
        """Execute a system command. ⚠️ VULNERABLE: Allows arbitrary command execution!
        
        Educational Example: This tool demonstrates command injection vulnerability.
        An attacker could inject malicious commands like 'ls; rm -rf /' or 'cat /etc/passwd'.
        """
        try:
            # VULNERABLE: Direct execution without sanitization
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            return f"Exit code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Command timed out after 10 seconds"
        except Exception as e:
            return f"Error: {str(e)}"

    # 🚨 VULNERABILITY 2: Path Traversal
    @server.tool()
    def read_file(file_path: str) -> str:
        """Read contents of a file. ⚠️ VULNERABLE: No path validation!
        
        Educational Example: This demonstrates path traversal vulnerability.
        An attacker could use '../../../etc/passwd' to access sensitive files outside the intended directory.
        """
        try:
            # VULNERABLE: No path validation or sanitization
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents:\n{content[:1000]}..."  # Limit output for demo
        except Exception as e:
            return f"Error reading file: {str(e)}"

    # 🚨 VULNERABILITY 3: SQL Injection
    @server.tool()
    def search_users(username: str) -> str:
        """Search for users in database. ⚠️ VULNERABLE: SQL injection possible!
        
        Educational Example: This demonstrates SQL injection vulnerability.
        An attacker could inject SQL like "'; DROP TABLE users; --" or "' OR '1'='1".
        """
        try:
            # Create a simple in-memory database for demo
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Create sample table and data
            cursor.execute('''CREATE TABLE users (id INTEGER, username TEXT, email TEXT, password TEXT)''')
            cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin@example.com', 'secret123')")
            cursor.execute("INSERT INTO users VALUES (2, 'user1', 'user1@example.com', 'password456')")
            cursor.execute("INSERT INTO users VALUES (3, 'guest', 'guest@example.com', 'guest789')")
            
            # VULNERABLE: String concatenation instead of parameterized query
            query = f"SELECT * FROM users WHERE username = '{username}'"
            cursor.execute(query)
            results = cursor.fetchall()
            
            conn.close()
            
            if results:
                return f"Query executed: {query}\nResults: {results}"
            else:
                return f"Query executed: {query}\nNo users found"
                
        except Exception as e:
            return f"Database error: {str(e)}"

    # 🚨 VULNERABILITY 4: Information Disclosure
    @server.tool()
    def get_system_info() -> str:
        """Get system information. ⚠️ VULNERABLE: Exposes sensitive system details!
        
        Educational Example: This demonstrates information disclosure vulnerability.
        Revealing system details can help attackers plan further attacks.
        """
        info = {
            "os": os.name,
            "platform": os.sys.platform,
            "python_version": os.sys.version,
            "current_user": os.environ.get('USER', 'unknown'),
            "home_directory": os.environ.get('HOME', 'unknown'),
            "path": os.environ.get('PATH', 'unknown'),
            "working_directory": os.getcwd(),
            "environment_variables": dict(os.environ)  # VERY DANGEROUS!
        }
        
        return json.dumps(info, indent=2)

    # 🚨 VULNERABILITY 5: Unsafe Deserialization
    @server.tool()
    def process_json_data(json_data: str) -> str:
        """Process JSON data. ⚠️ VULNERABLE: Unsafe eval() usage!
        
        Educational Example: This demonstrates unsafe deserialization.
        An attacker could inject malicious code through JSON that gets executed.
        """
        try:
            # VULNERABLE: Using eval instead of json.loads
            # This allows arbitrary code execution
            data = eval(json_data)  # NEVER DO THIS!
            
            result = f"Processed data: {data}"
            return result
            
        except Exception as e:
            return f"Processing error: {str(e)}"

    # 🚨 VULNERABILITY 6: Weak Input Validation
    @server.tool()
    def create_user_profile(user_input: str) -> str:
        """Create user profile from input. ⚠️ VULNERABLE: No input validation!
        
        Educational Example: This demonstrates weak input validation.
        Missing validation can lead to various attacks including XSS, injection, etc.
        """
        # VULNERABLE: No input validation or sanitization
        profile_html = f"""
        <html>
        <body>
        <h1>User Profile</h1>
        <p>Welcome, {user_input}!</p>
        <script>
        var userData = "{user_input}";
        console.log("User data: " + userData);
        </script>
        </body>
        </html>
        """
        
        return f"Generated HTML profile:\n{profile_html}"

    # 🚨 VULNERABILITY 7: Insecure File Operations
    @server.tool()
    def write_log_file(filename: str, content: str) -> str:
        """Write to log file. ⚠️ VULNERABLE: No file name validation!
        
        Educational Example: This demonstrates insecure file operations.
        An attacker could overwrite system files or write to unauthorized locations.
        """
        try:
            # VULNERABLE: No validation of filename or path
            with open(filename, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {filename}"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"

    # 🚨 VULNERABILITY 8: Resource Exhaustion (DoS)
    @server.tool()
    def generate_large_response(size: int) -> str:
        """Generate large response. ⚠️ VULNERABLE: No resource limits!
        
        Educational Example: This demonstrates resource exhaustion vulnerability.
        An attacker could request extremely large responses to consume server resources.
        """
        # VULNERABLE: No limits on response size
        if size > 1000000:  # Limit for demo to prevent actual DoS
            return "Size limited to 1,000,000 characters for safety"
        
        large_string = "A" * size
        return f"Generated string of {len(large_string)} characters: {large_string[:100]}..."

    # Add a resource
    @server.resource("history://hello-world")
    def hello_world() -> str:
        """The origin story of the famous 'Hello, World' program."""
        return (
            '"Hello, World" first appeared in a 1972 Bell Labs memo by '
            "Brian Kernighan and later became the iconic first program "
            "for beginners in countless languages."
        )

    # Add a prompt
    @server.prompt()
    def greet(name: str) -> list:
        """Generate a greeting prompt."""
        return [
            {
                "role": "user",
                "content": f"Say hello to {name}",
            },
        ]

    # 🚨 VULNERABILITY 9: Insecure Prompt Template
    @server.prompt()
    def vulnerable_prompt(user_input: str) -> list:
        """Generate a prompt with user input. ⚠️ VULNERABLE: Prompt injection possible!
        
        Educational Example: This demonstrates prompt injection vulnerability.
        An attacker could manipulate the prompt to change AI behavior or extract information.
        """
        # VULNERABLE: Direct insertion of user input into prompt
        return [
            {
                "role": "system",
                "content": f"You are a helpful assistant. The user said: {user_input}. Please respond appropriately."
            },
            {
                "role": "user",
                "content": "Please help me with my request."
            }
        ]

    return server
